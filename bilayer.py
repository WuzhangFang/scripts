from collections import OrderedDict
class Bilayer:
    """
    Purpose: generate coordinates for a BCC bilayer system
    Input: 1. number of layers of first compound (n1)
           2. number of layers of second compound (n2)
           3. layer spacing of first compound (d1)
           4. layer spacing of second compound (d2)
           5. in-plane lattice constant (a)
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
        self.d = 1.658 # from previous relaxation
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
        # store the even coordinates in layer 1
        for i in range(n1):
            z1 = (thickness/2.00 - (self.d)/2.00 - i*self.d1)/thickness
            if (i+1)%2 == 0:                
                # even layer
                self.coordinates.append([0.5,0.5,z1])
                self.atom_counter[1][1] += 1
        # store the odd coordinates in layer 2
        for i in range(n2):
            z2 = (thickness/2.00 + (self.d)/2.00 + i*self.d2)/thickness
            if (i+1)%2 == 1:
                # odd layer
                self.coordinates.append([0.5,0.5,z2])
                self.atom_counter[2][1] += 1
        # store the even coordinates in layer 2
        for i in range(n2):
            z2 = (thickness/2.00 + (self.d)/2.00 + i*self.d2)/thickness
            if (i+1)%2 == 0:                
                # even layer
                self.coordinates.append([0,0,z2])
                self.atom_counter[3][1] += 1

    def printfile(self, file='POSCAR-preliminary'):
        output_file = open(file, 'w')
        print('bilayer', file=output_file)
        print('1.0', file=output_file)
        print('{}    0.000    0.000'.format(self.a), file=output_file)
        print('0.000    {}    0.000'.format(self.a), file=output_file)
        print('0.000    0.000    {}'.format(self.thickness), file=output_file)
        atom_counter = OrderedDict()
        for atom in self.atom_counter:
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
        for coordinate in self.coordinates:
            print('{}    {}    {}'.format(coordinate[0],coordinate[1],coordinate[2]), file=output_file)
        output_file.close()
        print('done -> POSCAR')

