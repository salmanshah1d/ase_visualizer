import streamlit as st
from ase import io as ase_io
import py3Dmol
from stmol import showmol
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI()

# Format formula with subscripts using st.markdown and LaTeX
def formula_to_latex(formula):
    import re
    # Replace numbers with LaTeX subscripts
    return re.sub(r'(\d+)', r'$_{\1}$', formula)

st.title("ASE Visualizer")

uploaded_file = st.file_uploader("Upload a file", type=["cif", "pdb", "sdf", "xyz"])

if uploaded_file:
    atoms = ase_io.read(uploaded_file)
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
    viewer.setStyle({
        "stick":{},
        "sphere": {"radius": 0.5},
        # "scale": 0.3,
    })
    viewer.zoomTo()
    showmol(viewer)

    uploaded_file.seek(0)
    inmem_file_content = uploaded_file.read()

    with st.spinner("Generating molecule description..."):
        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can help me visualize a molecule."},
                {"role": "user", "content": f"What is the structure of the molecule? {inmem_file_content}"}
            ]
        )

    st.write(response.choices[0].message.content)
