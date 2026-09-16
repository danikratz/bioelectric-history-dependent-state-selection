"""Prepare a new sibling output folder using the exact frozen network protocol.
Default prepares only. --run repeats the bounded 142 initial conditions and checks.
Original archived dependency folders remain read-only.
"""
import argparse,os,shutil,subprocess,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('destination',help='New simple sibling folder name');parser.add_argument('--run',action='store_true');args=parser.parse_args()
    if Path(args.destination).name!=args.destination:parser.error('Use a simple new sibling folder name')
    target=ROOT.parent/args.destination
    if target.exists():parser.error('Destination exists; refusing to overwrite')
    frozen=json.loads((ROOT/'congelamento.json').read_text())
    assert hashlib.sha256((ROOT/'protocolo_validacao.json').read_bytes()).hexdigest()==frozen['protocol_sha256']
    target.mkdir()
    files=['modelo.py','executar.py','analisar_validacao.py','auditar_validacao.py','protocolo_validacao.json','congelamento.json','geometrias.npz','originais_sha256.json','PLANO_VALIDACAO.md','auditoria_previa.json']
    for name in files:shutil.copyfile(ROOT/name,target/name)
    print('Prepared',target,flush=True)
    if args.run:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
        commands=[['executar.py','isolated'],['executar.py','run'],['executar.py','verify'],['analisar_validacao.py'],['auditar_validacao.py']]
        for command in commands:subprocess.run([sys.executable,str(target/command[0]),*command[1:]],env=env,check=True)
        print('Numerical outputs and figures regenerated. The interpretive report and visual inspection are not automatically certified.',flush=True)
if __name__=='__main__':main()
