



import csv
import re

#pymol load
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI loading of pymol
import sys, time, os
import pymol
pymol.finish_launching()

PDBlist.append((PDB, chain, extrName, row1[0]))
class StructureTable(object):
    """creates a table of PDBnames and their chains which have to be aligned"""
    items = {}
    pymol.cmd.set("fetch_path", "/Volumes/Home/Users/mehdi/Downloads/peptides_modeling/PDB_for_modelling/NR")
    def __init__(self, pdb_list):
        """list the content of the file"""
        self.pdb_list = pdb_list

pymol.cmd.set("fetch_path", "/Volumes/Home/Users/mehdi/Downloads/peptides_modeling/PDB_for_modelling/NR")
rmsd_matrix = []
for item1 in PDBlist:
    pymol.cmd.fetch(item1[0], path='PDB_for_modelling/NR')
    rmsd_row = []
    for item2 in PDBlist:
        pymol.cmd.fetch(item2[0], path='PDB_for_modelling/NR')
        selection1 = item1[0] + " and chain " + item1[1]
        selection2 = item2[0] + " and chain " + item2[1]
        pymol.cmd.extract(item1[2], selection1)
        pymol.cmd.extract(item2[2], selection2)
        test = pymol.cmd.align(item1[2], item2[2])
	#print item1[3], item2[3]
	rmsd_row.append(test[0])

    rmsd_matrix.append(rmsd_row)

file = open('rmsd_matrix.txt', 'w')
for row in rmsd_matrix:
  file.write("%s\n" % row)

file.close()

"""
	    #first look if the pdb i already available before downloading 
	    pymol.cmd.set("fetch_path", "/Volumes/Home/Users/mehdi/Downloads/peptides_modeling/PDB_for_modelling/NR")
	    pymol.cmd.fetch(PDB, path='PDB_for_modelling/NR')
	    
            selection = PDB + " and chain " + chain 
	    cmd.extract(extrName, selection)
	    next(csvreader1) 

"""
