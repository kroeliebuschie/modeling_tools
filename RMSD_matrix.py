



import csv
import re

#pymol load
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI loading of pymol
import sys, time, os
import pymol
pymol.finish_launching()


#initiate list
PDBlist = []


with open('NR_complexes.csv', 'rU') as csvfile1:
    csvreader1 = csv.reader(csvfile1, dialect='excel')   #the file is made in excel so it has to be opened this way
    
    # this loop will get the sequence information of every row in the CSV file
    # These sequences are from the peptides which have to be modelled, they will 
    # be refered to as query the rest of the document
    next(csvreader1)                                   #skip the header, it conains no info
    for row1 in csvreader1:
	if row1[1] != "":
	    #structuur 
            chain = re.split('\W+', row1[2])[0]
            PDB = row1[1] 
            extrName = PDB + "_" + chain
	    PDBlist.append((PDB, chain, extrName, row1[0]))


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
