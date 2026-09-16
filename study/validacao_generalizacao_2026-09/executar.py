"""Bounded stages: isolated -> network -> numerical verification. Resume by IDs."""
import os,sys
sys.dont_write_bytecode=True
import datetime,json,platform,traceback
from pathlib import Path
import numpy as np
import scipy
from modelo import *

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def log_failure(stage,c,exc):
    with (ROOT/'falhas_execucao.jsonl').open('a') as f:f.write(json.dumps(dict(utc=now(),stage=stage,id=c.get('id'),error=repr(exc),traceback=traceback.format_exc()))+'\n')

def isolated():
    assert not (ROOT/'mecanismo_alternativo.json').exists(),'Preserve isolated results'
    # Algebra and finite-difference Jacobian checks before any network trajectory.
    cell=dict(model='cubic',gd=0.)
    polynomial=np.poly1d([-1.,L+U+H,-(L*U+L*H+U*H),L*U*H])/DEN
    assert np.max(abs(polynomial(np.array([L,U,H]))))<1e-10
    folds=np.sort(np.roots(np.polyder(polynomial))); currents=-old.C*cubic(folds)
    rlo,rhi=float(currents.min()-.005),float(currents.max()+.005)
    jacchecks=[]
    adjacency=np.array([[0.,1.,0.],[1.,0.,.1],[0.,.1,0.]])
    for name,gd in [('bistable',4.),('kv',0.),('cubic',0.),('leak',0.)]:
        c=dict(model=name,gd=gd); y=state(c,3,np.array([-.049,-.034,.008])); rhs,jac=funcs(c,adjacency,np.zeros(3));eye=np.eye(len(y));eps=1e-7
        fd=np.column_stack([(rhs(0,y+eps*e)-rhs(0,y-eps*e))/(2*eps) for e in eye]);error=float(abs(fd-jac(0,y).toarray()).max())
        jacchecks.append(dict(model=name,max_error_s_inv=error,passed=error<1e-4))
    assert all(r['passed'] for r in jacchecks)
    eig=cubic_prime(np.array([L,U,H]));assert eig[0]<0 and eig[1]>0 and eig[2]<0
    definitions=[]
    for i,v in enumerate(P['isolated_tests']['holds_initial_V']):definitions.append(dict(id=f'hold{i}',initial_V=v,kind='hold',end=1.))
    for leg in P['isolated_tests']['ramp_legs_s']:definitions.append(dict(id=f'ramp{leg:g}',kind='ramp',leg=leg,end=2*leg))
    out=[];folder=ROOT/'isolada';folder.mkdir(exist_ok=True)
    for d in definitions:
        if d['kind']=='hold':y0=np.array([d['initial_V']]);segments=[(1.,np.zeros((1,1)),np.zeros(1))]
        else:
            leg=d['leg'];coeff=polynomial.c.copy();coeff[-1]+=rlo/old.C; rr=np.roots(coeff);v=float(min(z.real for z in rr if abs(z.imag)<1e-9));y0=np.array([v]);rate=(rhi-rlo)/leg
            drive=lambda t:np.array([rlo+rate*t if t<=leg else rhi-rate*(t-leg)])
            segments=[(leg,np.zeros((1,1)),drive),(2*leg,np.zeros((1,1)),drive)]
        solutions=[]
        for label,solver in [('primary',P['primary_solver']),('refined',P['refined_solver']),('radau',P['radau_solver'])]:
            t,y,info=integrate(cell,segments,solver,y0=y0);np.savez_compressed(folder/(d['id']+'_'+label+'.npz'),t=t,y=y);solutions.append(y)
        er=float(abs(solutions[0]-solutions[1]).max());erref=float(abs(solutions[1]-solutions[2]).max());accepted=er<P['voltage_tolerance_V'] and erref<P['voltage_tolerance_V']
        extra={}
        if d['kind']=='hold':expected=L if d['initial_V']<U else H;extra=dict(expected_V=expected,final_error_V=float(abs(solutions[1][0,-1]-expected)));accepted=accepted and extra['final_error_V']<1e-6
        else:
            extra=dict(crossed_up=bool((solutions[1][0,t<=leg]>U).any()),returned_low=bool(solutions[1][0,-1]<U),final_V=float(solutions[1][0,-1]))
        out.append(dict(**d,primary_vs_refined_V=er,radau_vs_refined_V=erref,passed=bool(accepted),**extra))
    result=dict(completed_utc=now(),model=P['alternative'],equilibria=[dict(voltage_V=float(v),eigenvalue_s_inv=float(e),stable=bool(e<0)) for v,e in zip([L,U,H],eig)],folds=[dict(voltage_V=float(v),current_A_m2=float(i)) for v,i in zip(folds,currents)],ramp_current_range_A_m2=[rlo,rhi],jacobian_checks=jacchecks,isolated_protocols=out,isolated_passed=all(x['passed'] for x in out),network_test_started=False,interpretation='Analytical coexistence at I=0 and local slopes demonstrate bistability. Network outcomes not used in parameter selection.')
    write('mecanismo_alternativo.json',result);print('ISOLATED',json.dumps(result),flush=True)
    assert result['isolated_passed'],'Do not test network before isolated validation'

def run():
    mechanism=json.loads((ROOT/'mecanismo_alternativo.json').read_text());assert mechanism['isolated_passed']
    (ROOT/'primarias').mkdir(exist_ok=True)
    path=ROOT/'resultados_validacao.jsonl';rows=[json.loads(s) for s in path.read_text().splitlines()] if path.exists() else [];done={r['id'] for r in rows}
    recordpath=ROOT/'execucao_validacao.json'
    record=json.loads(recordpath.read_text()) if recordpath.exists() else dict(started_utc=now(),protocol_sha256=digest(ROOT/'protocolo_validacao.json'),environment=P['environment'],code_sha256={p.name:digest(p) for p in ROOT.glob('*.py')},planned_network_conditions=136,planned_isolated_conditions=6)
    write('execucao_validacao.json',record)
    with path.open('a') as f:
        for idx,c in enumerate(P['conditions']):
            if c['id'] in done:continue
            try:
                t,y,row=execute(c,P['primary_solver']);np.savez_compressed(ROOT/'primarias'/(c['id']+'.npz'),t=t,y=y)
                f.write(json.dumps(row,allow_nan=False)+'\n');f.flush();rows.append(row)
                print('PRIMARY',idx+1,136,c['id'],c['geometry'],c['model'],c['history'],row['category'],row['target_high'],flush=True)
            except Exception as exc:log_failure('primary',c,exc);raise
    record.update(primary_completed_utc=now(),completed_network_conditions=len(rows),isolated_conditions=6);write('execucao_validacao.json',record)

def verify():
    rows=[json.loads(s) for s in (ROOT/'resultados_validacao.jsonl').read_text().splitlines()];assert len(rows)==136
    byid={r['id']:r for r in rows};outpath=ROOT/'verificacao_linhas.jsonl';records=[json.loads(s) for s in outpath.read_text().splitlines()] if outpath.exists() else [];done={r['id'] for r in records}
    for name in ['refinadas','radau','correcoes']: (ROOT/name).mkdir(exist_ok=True)
    with outpath.open('a') as f:
        for idx,c in enumerate(P['conditions']):
            if c['id'] in done:continue
            try:
                t,y,r=execute(c,P['refined_solver']);np.savez_compressed(ROOT/'refinadas'/(c['id']+'.npz'),t=t,y=y)
                with np.load(ROOT/'primarias'/(c['id']+'.npz')) as z:
                    assert np.array_equal(t,z['t']);error=float(abs(y[:226]-z['y'][:226]).max())
                matched=agree(r,byid[c['id']]); passed=error<P['voltage_tolerance_V'] and matched
                rec=dict(id=c['id'],primary_vs_refined_V=error,primary_classification_agrees=matched,primary_passed=bool(passed),radau_required=c['id'] in P['radau_fixed_ids'] or not passed,refined_metrics=r,effective_source='refinadas',corrected=False)
                if rec['radau_required']:
                    tr,yr,rr=execute(c,P['radau_solver']);assert np.array_equal(t,tr);np.savez_compressed(ROOT/'radau'/(c['id']+'.npz'),t=tr,y=yr)
                    errorr=float(abs(y[:226]-yr[:226]).max());matchedr=agree(r,rr);rec.update(radau_vs_refined_V=errorr,radau_classification_agrees=matchedr,radau_passed=bool(errorr<P['voltage_tolerance_V'] and matchedr));passed=passed and rec['radau_passed']
                rec['initial_passed']=bool(passed)
                if not passed:
                    th,yh,rh=execute(c,dict(method='DOP853',rtol=3e-14,atol=3e-16,max_step=.0005));tr,yr,rr=execute(c,dict(method='Radau',rtol=1e-12,atol=1e-14,max_step=.001))
                    errh=float(abs(yh[:226]-y[:226]).max());errr=float(abs(yh[:226]-yr[:226]).max());matchedh=agree(rh,r) and agree(rh,rr)
                    passed=errh<P['voltage_tolerance_V'] and errr<P['voltage_tolerance_V'] and matchedh
                    np.savez_compressed(ROOT/'correcoes'/(c['id']+'.npz'),t=th,y=yh,radau=yr)
                    rec.update(corrected=True,correction=dict(fine_vs_high_V=errh,radau_vs_high_V=errr,classification_agrees=matchedh,passed=bool(passed)),effective_source='correcoes',refined_metrics=rh)
                rec['passed']=bool(passed)
                if not passed: rec['refined_metrics']['category']='indeterminada'
                records.append(rec);f.write(json.dumps(rec,allow_nan=False)+'\n');f.flush()
                print('VERIFY',idx+1,136,c['id'],passed,'max_mV',error*1000,'Radau',rec['radau_required'],flush=True)
            except Exception as exc:log_failure('verify',c,exc);raise
    effective=[]
    for rec in records:
        r=dict(rec['refined_metrics'],numerically_accepted=rec['passed'],effective_source=rec['effective_source'],numerical_correction=rec['corrected']);effective.append(r)
    (ROOT/'resultados_conferidos_validacao.jsonl').write_text(''.join(json.dumps(r,allow_nan=False)+'\n' for r in effective))
    output=dict(completed_utc=now(),network_conditions=136,all_refined=True,radau_count=sum(r['radau_required'] for r in records),original_failed_ids=[r['id'] for r in records if not r['initial_passed']],corrected_ids=[r['id'] for r in records if r['corrected']],unresolved_ids=[r['id'] for r in records if not r['passed']],maximum_primary_refined_V=max(r['primary_vs_refined_V'] for r in records),maximum_radau_refined_V=max(r.get('radau_vs_refined_V',0) for r in records),classification_changes=[r['id'] for r in records if not r['primary_classification_agrees']],passed=all(r['passed'] for r in records),records_file='verificacao_linhas.jsonl')
    write('verificacao_numerica.json',output);print('VERIFIED',json.dumps(output),flush=True)
    record=json.loads((ROOT/'execucao_validacao.json').read_text());record.update(verification_completed_utc=now(),verified_conditions=136,radau_conditions=output['radau_count']);write('execucao_validacao.json',record)
if __name__=='__main__':{'isolated':isolated,'run':run,'verify':verify}[sys.argv[1]]()
