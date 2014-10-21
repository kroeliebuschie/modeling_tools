#!/usr/bin/env python
## This script checks the interface of the PDBs for 
## Histidines. This is important because of the protonation state.
## The script can only be used when the pymol api can be loaded.
##
## Author: Mehdi Nellen, Utrecht 2014

#pymol load
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI loading of pymol
import sys, time, os
import pymol
pymol.finish_launching()

# This is the dir with NRs which have to be modeled
os.chdir("/Volumes/alcazar.science.uu.nl/peptides_modeling/final_NR/with_compound")

# This list can be replaced by any pdb list
list=["CAR_pdb_renum.pdb" ,"ERRa_pdb_renum.pdb" ,"ERRb_pdb_renum.pdb" ,"ERRg_pdb_renum.pdb" ,"ERa_pdb_renum.pdb" ,"ERb_pdb_renum.pdb" ,"FXR_pdb_renum.pdb" ,"GR_pdb_renum.pdb" ,"LXRa_pdb_renum.pdb" ,"LXRb_pdb_renum.pdb" ,"MR_pdb_renum.pdb" ,"PPARd_pdb_renum.pdb" ,"PPARg_pdb_renum.pdb" ,"PR_pdb_renum.pdb" ,"PXR_pdb_renum.pdb" ,"RARa_pdb_renum.pdb" ,"RARb_pdb_renum.pdb" ,"RARg_pdb_renum.pdb" ,"RORg_pdb_renum.pdb" ,"RXRa_pdb_renum.pdb" ,"RXRb_pdb_renum.pdb" ,"TRa_pdb_renum.pdb" ,"TRb_pdb_renum.pdb" ,"VDR_pdb_renum.pdb"]

for item in list:
    pymol.cmd.load(item)
    pymol.cmd.select("interface_" +item[:-4] + ", byres((" + item[:-4] + " and chain A) within 5A of (" + item[:-4] + " and chain X))") # change chain ID if you like
    myspace ={"reslist" : []}
    pymol.cmd.iterate("byres((" + item[:-4] + " and chain A) within 5A of (" + item[:-4] + " and chain X))", "reslist.append(resn)", space=myspace)
    # this part counts the number of Histidines in the interface and prints a message
    hiscount = 0
    for res in myspace["reslist"]:
        if res == "HIS":
            hiscount += 1
    if hiscount != 0:
        hiscount = hiscount/10
        print item + " contains " + str(hiscount) + " histidine(s) in the interface!"

