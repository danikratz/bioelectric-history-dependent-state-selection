"""Prepare an isolated sibling copy, optionally run the frozen main experiment.

Usage: python reproduzir.py NAME [--run]
NAME must be a new sibling directory name. Archived data are never overwritten.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser();parser.add_argument('name');parser.add_argument('--run',action='store_true');args=parser.parse_args()
    source=Path(__file__).resolve().parent
    if args.name in ['.','..'] or Path(args.name).name!=args.name:parser.error('Use a new sibling directory name')
    dest=source.parent/args.name
    if dest.exists():parser.error('Destination already exists; nothing overwritten')
    protocol=json.loads((source/'protocolo.json').read_text())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    for name,value in protocol['source_sha256'].items():
        if sha(source.parent/name)!=value:raise ValueError('Frozen input changed: '+name)
    dest.mkdir()
    inputs=['protocolo.json','desenvolvimento.json','reparos.npz','selecao_reparos.json','PLANO.md',
            'CONTROLES_ADICIONAIS.md','verificacao_mecanismos.json','equilibrios.json']
    for p in list(source.glob('*.py'))+[source/name for name in inputs]:
        shutil.copy2(p,dest/p.name)
        assert sha(p)==sha(dest/p.name)
    if args.run:
        for command in [['experimento.py','run'],['experimento.py','verify'],['refinar_falhas.py']]:
            with (dest/('reproduction_'+command[0]+('_'+command[1] if len(command)>1 else '')+'.log')).open('w') as log:
                subprocess.run([sys.executable,str(dest/command[0])]+command[1:],stdout=log,stderr=subprocess.STDOUT,check=True)
        assert json.loads((dest/'correcao_numerica.json').read_text())['passed']
    print(dest)


if __name__=='__main__':main()
