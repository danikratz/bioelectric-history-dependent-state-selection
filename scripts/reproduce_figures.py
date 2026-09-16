"""Reexport the ten frozen figures; no ODE integration or parameter search."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'source_code/figuras_publicacao.py')],cwd=root,check=True)
subprocess.run([sys.executable,str(root/'source_code/render_english_figures.py'),'--study-root',str(root/'study'),'--output',str(root/'figures/english'),'--endpoint-cache',str(root/'figure_data/validation_final_voltages.npz')],cwd=root,check=True)
print('Completed: two main figures in figures/ and eight English reexports in figures/english/.')
