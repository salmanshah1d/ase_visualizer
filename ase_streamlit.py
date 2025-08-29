import streamlit as st
from ase import io
import py3Dmol
from stmol import showmol

# Format formula with subscripts using st.markdown and LaTeX
def formula_to_latex(formula):
    import re
    # Replace numbers with LaTeX subscripts
    return re.sub(r'(\d+)', r'$_{\1}$', formula)

st.title("ASE Visualizer")

uploaded_file = st.file_uploader("Upload a file", type=["cif", "pdb", "sdf", "xyz"])


if uploaded_file:
    atoms = io.read(uploaded_file)
    xyz = atoms.get_positions()

    # Convert ASE atoms → XYZ string
    xyz_str = f"{len(atoms)}\n\n"
    for atom, pos in zip(atoms, atoms.positions):
        xyz_str += f"{atom.symbol} {pos[0]} {pos[1]} {pos[2]}\n"

    st.title(formula_to_latex(atoms.get_chemical_formula()))
    st.write("Cell parameters:", atoms.cell.lengths().tolist())
    st.write("Number of atoms:", len(atoms))

    viewer = py3Dmol.view(width=500, height=500)
    viewer.addModel(xyz_str, "xyz")
    viewer.setStyle({"stick":{}})
    viewer.zoomTo()
    showmol(viewer)
