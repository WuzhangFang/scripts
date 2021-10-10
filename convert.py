# convert CONTCAR to OMX
# python/3.7
# Author: Wuzhang FANG
# 5/5/2021

import numpy as np
import os

# read CONTCAR
file_input = open('CONTCAR')
data = file_input.readlines()
file_input.close()

# store the lattice vectors
va = np.fromstring(data[2], sep=' ')
vb = np.fromstring(data[3], sep=' ')
vc = np.fromstring(data[4], sep=' ')

# store the type and number of each element
elements_label = data[5].split()
num_elements = np.fromstring(data[6], dtype=int, sep=' ')
total_num = np.sum(num_elements)
elements = []

for i in range(len(num_elements)):
    l = [elements_label[i] for j in range(num_elements[i])]
    elements += l

# !!!!!!!! important
# based on the basis set () and initial magnetic state
# spins 
#                Nb      Se    Co
spin_label = [[6.5, 6.5], [3, 3], [9, 6]]
spins = []
for i in range(len(num_elements)):
    s = [spin_label[i] for j in range(num_elements[i])]
    spins += s

# store the coordinates of each atom
coordinates = []
for i in range(total_num):
    c = np.fromstring(data[8 + i], dtype=float, sep=' ')
    coordinates.append(c)

# saved to a file 
output_file = open('openmx.dat', 'w')

# please modify the parameters accordingly
front = """
System.CurrentDirectory ./
System.Name NbSe

level.of.stdout 1
level.of.fileout 0

HS.fileout          on      # on|off, default=off
#######  please change the path accordingly
DATA.PATH  /home/belashchenko/wfang/openmx3.9/DFT_DATA19

Species.Number 3
<Definition.of.Atomic.Species
Nb Nb7.0-s3p2d2 Nb_PBE19
Se Se7.0-s3p2d2 Se_PBE19
Co Co6.0S-s3p2d2 Co_PBE19S
Definition.of.Atomic.Species>
"""

print(front, file=output_file)
print('Atoms.UnitVectors.Unit Ang', file=output_file)
print('<Atoms.UnitVectors', file=output_file)
print('{:7.5f}  {:7.5f}  {:7.5f}'.format(va[0], va[1], va[2]), file=output_file)
print('{:7.5f}  {:7.5f}  {:7.5f}'.format(vb[0], vb[1], vb[2]), file=output_file)
print('{:7.5f}  {:7.5f}  {:7.5f}'.format(vc[0], vc[1], vc[2]), file=output_file)
print('Atoms.UnitVectors>', file=output_file)
print('\n', file=output_file)
print('Atoms.SpeciesAndCoordinates.Unit Frac', file=output_file)
print('Atoms.Number {}'.format(total_num), file=output_file)
print('<Atoms.SpeciesAndCoordinates', file=output_file)
for i in range(total_num):
    print('{:2d}  {}  {:8.6f}  {:8.6f}  {:8.6f}  {:3.1f}  {:3.1f}  on'.format(i + 1, elements[i],
                                                                              coordinates[i][0], coordinates[i][1],
                                                                              coordinates[i][2],
                                                                              spins[i][0], spins[i][1]),
          file=output_file)
print('Atoms.SpeciesAndCoordinates>', file=output_file)
print('\n', file=output_file)

# plese modify the parameters accordingly
end = """
<Hubbard.U.values                 #  eV
 Nb 1s 0.0 2s 0.0 3s 0.0 1p 0.0 2p 0.0 1d 0.0 2d 0.0
 Se 1s 0.0 2s 0.0 3s 0.0 1p 0.0 2p 0.0 1d 0.0 2d 0.0
 Co 1s 0.0 2s 0.0 3s 0.0 1p 0.0 2p 0.0 1d 2.0 2d 0.0
Hubbard.U.values>

scf.Hubbard.U on
scf.XcType GGA-PBE #  LDA|LSDA-CA|LSDA-PW|GGA-PBE
scf.SpinPolarization on # On|Off|NC
scf.ElectronicTemperature 300.0 # default=300 (K)
scf.energycutoff 200.0 # default=150 (Ry)
scf.maxIter 200  # default=40
scf.EigenvalueSolver band # DC|GDC|Cluster|Band
scf.Kgrid 4 4 4 # means n1 x n2 x n3
scf.Mixing.Type rmm-diisk # Simple|Rmm-Diis|Gr-Pulay|Kerker|Rmm-Diisk
scf.Init.Mixing.Weight 0.3 #default=0.30
scf.Min.Mixing.Weight 0.001  # default=0.001
scf.Max.Mixing.Weight 0.3 # default=0.40
scf.Mixing.StartPulay  5
scf.Mixing.EveryPulay  1
scf.Mixing.History 10 # default=5
scf.criterion 1.0e-8 # default=1.0e-6 (Hartree)
#scf.ProExpn.VNA       off
scf.spinorbit.coupling off

scf.restart.filename                  NbSe
scf.restart                           on
"""

print(end, file=output_file)

output_file.close()
