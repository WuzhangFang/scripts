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
test.add_layers(12,6)
# generate POSCAR
test.printfile()