from ase import io

# Load the CIF file
atoms = io.read("1000023.cif")

# Print some basic info
print(atoms)
print("Atomic positions:\n", atoms.positions)
print("Cell parameters:\n", atoms.cell)
