"""Compare reproduced numerical artists and PNG pixels against the frozen release."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'figure_data/REFERENCE_PNG_SHA256.json').read_text())
bad=[]
for name,digest in expected.items():
 f=root/('figures' if name.startswith(('fig1_','fig2_')) else 'figures/english')/name
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:bad.append(name)
a=json.loads((root/'figure_data/REFERENCE_NUMERIC_ARTISTS.json').read_text())['figures']
b=json.loads((root/'figures/english/ENGLISH_FIGURE_AUDIT.json').read_text())['figures']
num={r['figure']:r['numeric_artists_after_sha256'] for r in a};actual={r['figure']:r['numeric_artists_after_sha256'] for r in b}
assert num==actual,'Numerical artists differ from frozen figures'
print('PASS: numerical artists match for all eight reexports')
if bad:
 print('PNG byte differences (may reflect renderer/font/platform differences; inspect): '+', '.join(bad));sys.exit(1)
print('PASS: all ten PNG files match the frozen release byte for byte')
