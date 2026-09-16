"""Conductance models on archived graphs; SI units, synthetic inward current.

This is an independent reduced ODE implementation, not native BETSE execution.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import expit
from scipy.sparse import csr_matrix, diags, bmat

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
Q = json.loads((BASE/'primeiro_parametro_publicado/plano.json').read_text())
ARCHIVE = np.load(BASE/'sorteio_independente_32/topologias.npz')
N = 226
RIGHT = ARCHIVE['right']
CENTER = int(ARCHIVE['center'])
XY = ARCHIVE['xy']
ORIGINAL = ARCHIVE['original']
CUT = ORIGINAL.copy()
CUT[RIGHT[:, None] != RIGHT[None, :]] = 0
GRAPHS = {k: ARCHIVE[k] for k in ['original', 'interface_10pct', 'independent32_seed11', 'independent32_seed22', 'independent32_seed33']}
GRAPHS['cut'] = CUT
C = Q['cm_F_m2']
GL = Q['G_leak_S_m2']
EL = Q['E_leak_V']
EK = Q['E_channel_V']
GK = 2.
ED = .05


def f(v):
    return expit((v-Q['V_half_V'])/Q['slope_V'])


def a(v):
    return expit((v+.025)/.004)


def h_inf(v):
    return expit(-(v+.040)/.004)


@dataclass(frozen=True)
class Model:
    name: str
    gd: float = 0.
    tau: float = .0148
    tauh: float = .1

    @property
    def excitable(self):
        return self.name == 'excitable'

    def steady_current(self, v):
        h = h_inf(v) if self.excitable else 1.
        return GL*(v-EL)+GK*f(v)*(v-EK)-self.gd*a(v)*h*(ED-v)

    def roots(self, current=0.):
        x = np.linspace(-.5, .15, 10001)
        y = self.steady_current(x)-current
        rr = [brentq(lambda v: self.steady_current(v)-current, x[i], x[i+1], xtol=1e-14)
              for i in range(len(x)-1) if y[i]*y[i+1]<0]
        return np.array(rr)

    def state(self, n, voltage=None):
        v = np.full(n, self.roots()[0]) if voltage is None else np.broadcast_to(voltage, (n,)).copy()
        return np.r_[v, f(v), h_inf(v)] if self.excitable else np.r_[v, f(v)]


MODELS = {'kv':Model('kv'), 'bistable':Model('bistable',4.), 'excitable':Model('excitable',4.)}


def lap(adj):
    return diags(adj.sum(1))-csr_matrix(adj)


def functions(model, adj, gap, current):
    n = len(adj)
    L = lap(adj)
    def rhs(t, y):
        v, m = y[:n], y[n:2*n]
        h = y[2*n:] if model.excitable else 1.
        drive = current(t) if callable(current) else current
        dv = (-gap*(L@v)-GL*(v-EL)-GK*m*(v-EK)+model.gd*a(v)*h*(ED-v)+drive)/C
        dm = (f(v)-m)/model.tau
        return np.r_[dv, dm, (h_inf(v)-h)/model.tauh] if model.excitable else np.r_[dv,dm]
    def jac(t, y):
        v, m = y[:n], y[n:2*n]
        h = y[2*n:] if model.excitable else 1.
        av, fv, hv = a(v), f(v), h_inf(v)
        diagonal = (-GL-GK*m+model.gd*h*(av*(1-av)/.004*(ED-v)-av))/C
        vv = -gap*L+diags(C*diagonal)
        vv = vv/C
        vm = diags(-GK*(v-EK)/C)
        mv = diags(fv*(1-fv)/Q['slope_V']/model.tau)
        mm = diags(np.full(n,-1/model.tau))
        if not model.excitable:
            return bmat([[vv,vm],[mv,mm]],format='csr')
        vh = diags(model.gd*av*(ED-v)/C)
        hvj = diags(-hv*(1-hv)/.004/model.tauh)
        hh = diags(np.full(n,-1/model.tauh))
        return bmat([[vv,vm,vh],[mv,mm,None],[hvj,None,hh]],format='csr')
    return rhs, jac


def simulate(model, segments, gap=1., y0=None, sample=.001, method='DOP853',
             rtol=1e-8, atol=1e-10, max_step=.005):
    """segments=[(end_time, adjacency, inward_current_vector_or_callable), ...]."""
    n = len(segments[0][1]); y = model.state(n) if y0 is None else y0.copy()
    start = 0.; ts = [np.array([0.])]; ys = [y[:,None]]; nfev = 0
    for end, adj, current in segments:
        if end<=start+1e-13:
            continue
        rhs, jac = functions(model,adj,gap,current)
        # Global grid plus exact event times. No integration step crosses a switch.
        tt = np.arange(np.floor(start/sample)+1, np.ceil(end/sample)+1)*sample
        tt = np.unique(np.r_[tt[(tt>start+1e-12)&(tt<end-1e-12)],end])
        opts = {'jac':jac} if method in ['Radau','BDF'] else {}
        sol = solve_ivp(rhs,(start,end),y,method=method,t_eval=tt,rtol=rtol,atol=atol,max_step=max_step,**opts)
        if not sol.success:
            raise RuntimeError(sol.message)
        ts.append(sol.t); ys.append(sol.y); y=sol.y[:,-1]; start=end; nfev+=sol.nfev
    t=np.concatenate(ts); state=np.concatenate(ys,axis=1)
    if not np.isfinite(state).all() or state[n:].min() < -1e-7 or state[n:].max()>1+1e-7:
        raise ValueError('Nonfinite state or gate outside [0,1]')
    return t,state,dict(nfev=nfev,method=method,rtol=rtol,atol=atol,
                         gate_min=float(state[n:].min()),gate_max=float(state[n:].max()))


def protocol_segments(graph, amplitude, mask, pulse=.02, restore=None, end=2., repair=None, repair_at=None):
    events=sorted(set([0.,pulse,end]+([restore] if restore is not None else [])+([repair_at] if repair_at is not None else [])))
    result=[]
    for t0,t1 in zip(events[:-1],events[1:]):
        if t0>=end or t1<=0:
            continue
        adj=ORIGINAL if restore is not None and t0>=restore-1e-12 else graph
        if repair is not None and repair_at is not None and t0>=repair_at-1e-12:
            adj=repair
        current=amplitude*mask if t0<pulse-1e-12 else np.zeros(N)
        result.append((min(t1,end),adj,current))
    return result


def metrics(model,t,y,segments,gap=1.,threshold=None):
    n=len(segments[0][1]); v=y[:n]; rest=model.roots()[0]
    right=RIGHT if n==N else np.ones(n,dtype=bool)
    mean=(v[right].mean(0)-rest)*1000
    positive=np.maximum(mean,0.)
    area=float(np.trapz(positive,t))
    peak=int(np.argmax(mean))
    thr=threshold if threshold is not None else (MODELS['bistable'].roots()[1] if model.gd else rest+.01)
    ever=(v>thr).any(1)
    hits=np.where((v[right]>thr).any(0))[0]
    rhs,_=functions(model,segments[-1][1],gap,segments[-1][2])
    final_rhs=rhs(t[-1],y[:,-1])
    # Integrated positive current from source side to the fixed target region.
    flux=np.zeros(len(t)); cancellation=0.
    if n==N:
        start=0.
        for end,adj,_ in segments:
            idx=(t>=start)&(t<end if end<t[-1] else t<=end)
            j=-gap*(lap(adj)@v[:,idx]); cancellation=max(cancellation,float(np.max(abs(j.sum(0)))))
            flux[idx]=j[RIGHT].sum(0); start=end
    return dict(peak_mV=float(mean[peak]),time_peak_s=float(t[peak]),positive_area_mV_s=area,
                positive_centroid_s=float(np.trapz(t*positive,t)/area) if area>1e-14 else None,
                final_mean_mV=float(mean[-1]),final_max_departure_mV=float(abs(v[:,-1]-rest).max()*1000),
                target_ever_fraction=float(ever[right].mean()),target_final_fraction=float((v[right,-1]>thr).mean()),
                first_target_crossing_s=float(t[hits[0]]) if len(hits) else None,
                final_dv_max_V_s=float(abs(final_rhs[:n]).max()),final_gate_derivative_max_s_inv=float(abs(final_rhs[n:]).max()),
                net_cut_charge_effective_C_m2=float(np.trapz(flux,t)),positive_cut_charge_effective_C_m2=float(np.trapz(np.maximum(flux,0),t)),
                junction_sum_max_A_m2=cancellation)


def compact(model,t,y,threshold):
    v=y[:N]; rest=model.roots()[0]
    return np.column_stack([t,1000*(v[RIGHT].mean(0)-rest),1000*v[CENTER],(v[RIGHT]>threshold).mean(0)])
