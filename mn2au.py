# Author: Wuzhang Fang
# Email: wfang@huskers.unl.edu
# Purpose: generate a POSCAR file of a bilayer BCC system
# Input: 1. number of layers of first compound (n1)
#        2. number of layers of second compound (n2)
#        3. layer spacing of first compound (d1)
#        4. layer spacing of second compound (d2)
#        5. in-plane lattice constant (a)
# Output: POSCAR
#
# +---------+
# | vacuum  |
# +---------+
# | alpha-W |
# +---------+
# | Mn2Au   |
# +---------+
# | vaccum  |
# +---------+
#
# Mn2Au with alpha-W
# lattice constant of Mn2Au: a = 3.328 angstrom, c = 8.539 angstrom
# (http://scripts.iucr.org/cgi-bin/paper?S056773947000092X)
#
# import class
from bilayer import Bilayer
from collections import OrderedDict
# initialize the parameters
a = 3.328
d1 = 1.42
d2 = 1.58
test = Bilayer(a, d1, d2)
# add atoms
test.add_atom('Au') # layer 1 odd layer
test.add_atom('Mn') # layer 1 even layer
test.add_atom('W')  # layer 2 odd layer
test.add_atom('W')  # layer 2 even layer
# add_layers(#Mn2Au, #W)
test.add_layers(7,6)
# generate POSCAR
output_file = open('POSCAR-preliminary', 'w')
print('bilayer', file=output_file)
print('1.0', file=output_file)
print('{}    0.000    0.000'.format(test.a), file=output_file)
print('0.000    {}    0.000'.format(test.a), file=output_file)
print('0.000    0.000    {}'.format(test.thickness), file=output_file)
# use a ordered dictionary to store the species and numbers of each atom
# species
atom_counter = OrderedDict()
for atom in test.atom_counter:
    if atom[0] not in atom_counter.keys():
        atom_counter[atom[0]] = atom[1]
    else:
        atom_counter[atom[0]] += atom[1]
print('  '.join([k for k,v in atom_counter.items()]))        
print('  '.join([k for k,v in atom_counter.items()]), file=output_file)
# numbers
print('  '.join([str(v) for k,v in atom_counter.items()]))
print('  '.join([str(v) for k,v in atom_counter.items()]), file=output_file)
print('Direct', file=output_file)
# coordinate of each atom
for coordinate in test.coordinates:
    print('{}    {}    {}'.format(coordinate[0],coordinate[1],coordinate[2]), file=output_file)
output_file.close()
print('done -> POSCAR')