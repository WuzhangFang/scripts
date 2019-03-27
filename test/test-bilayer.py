# Author: Wuzhang Fang
# Email: wfang@huskers.unl.edu
# Purpose: generate a POSCAR file of a bilayer FCC system
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
# | layer 2 |
# +---------+
# | layer 1 |
# +---------+
# | vaccum  |
# +---------+
#
from collections import OrderedDict

class Bilayer:
    """
    Purpose: generate a POSCAR file of a bilayer FCC system
    """
    def __init__(self, a=1.0, d1=1.0, d2=1.0):
        self.n1 = 1
        self.n2 = 1
        self.a = a
        self.d1 = d1
        self.d2 = d2
        # here assuming interface distance is the average of layer spacings
        # this can be served as an initial guess
        # after relaxation, modify here using a better value
        self.d = (self.d1 + self.d2)/2
        self.a = a
        self.coordinates = []
        self.thickness = 0.0
        self.atom_counter = []
    def add_atom(self, atom):
        self.atom_counter.append([atom,0])
    def add_layers(self, n1=1, n2=1):
        self.n1 = n1
        self.n2 = n2
        # add one vacuum layer of 20 angstrom
        thickness = (n1-1) * self.d1 + (n2-1) * self.d2 + self.d + 20.00
        self.thickness = thickness
        print("The thickness including vacuum layer is {} angstrom.".format(thickness))
        # store the odd coordinates in layer 1
        for i in range(n1):
            z1 = (thickness/2.00 - (self.d)/2.00 - i*self.d1)/thickness
            if (i+1)%2 == 1:
                # odd layer
                self.coordinates.append([0,0,z1])
                self.atom_counter[0][1] += 1
                self.coordinates.append([0.5,0.5,z1])
                self.atom_counter[0][1] += 1
        # store the even coordinates in layer 1
        for i in range(n1):
            z1 = (thickness/2.00 - (self.d)/2.00 - i*self.d1)/thickness
            if (i+1)%2 == 0:                
                # even layer
                self.coordinates.append([0.5,0,z1])
                self.atom_counter[1][1] += 1
                self.coordinates.append([0,0.5,z1])
                self.atom_counter[1][1] += 1
        # store the odd coordinates in layer 2
        for i in range(n2):
            z2 = (thickness/2.00 + (self.d)/2.00 + i*self.d2)/thickness
            if (i+1)%2 == 1:
                # odd layer
                self.coordinates.append([0,0,z2])
                self.atom_counter[2][1] += 1
                self.coordinates.append([0.5,0.5,z2])
                self.atom_counter[2][1] += 1
        # store the even coordinates in layer 2
        for i in range(n2):
            z2 = (thickness/2.00 + (self.d)/2.00 + i*self.d2)/thickness
            if (i+1)%2 == 0:                
                # even layer
                self.coordinates.append([0.5,0,z2])
                self.atom_counter[3][1] += 1
                self.coordinates.append([0,0.5,z2])
                self.atom_counter[3][1] += 1

# generate Mn2Au with alpha-W
# lattice constant of Mn2Au: a = 3.328 angstrom, c = 8.539 angstrom
# (http://scripts.iucr.org/cgi-bin/paper?S056773947000092X)
a = 3.328
d1 = 1.42
d2 = 1.58
test = Bilayer(a, d1, d2)
# add atoms
test.add_atom('Mn') # layer 1 odd layer
test.add_atom('Au') # layer 1 even layer
test.add_atom('W')  # layer 2 odd layer
test.add_atom('W')  # layer 2 even layer
# add layers
test.add_layers(4,2)
# generate POSCAR
output_file = open('POSCAR', 'w')
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