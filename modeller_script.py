#!/usr/bin/env python
########################################
#                                      #
#                                      #
#      This script will generate       #
#      models of the NRs from the      #
#     PIR formated alignment files     #
#       using modeller scripts         #
#                                      #
#                                      #
#     Author: Mehdi Nellen, 2014       #
#                                      #
#                                      #
########################################


# please change this variable:
# env.io.atom_files_directory




# Homology modeling by the automodel class
import sys
import re
from modeller import *                       # Load standard Modeller classes
from modeller.automodel import *             # Load the automodel class
from modeller.parallel import *              # Load the parallel class, to use multiple processors


if len(sys.argv) != 2:
    print "use:\n\tmodeller_script.py alignment.ALI\n\nDon't forget to change variable 'env.io.atom_files_directory'"
else:
    def modeller_fun(ALI_file, loop):
        """This is the function that does the modeling, it needs the argument loop to tell it to use loopmodel or automodel"""

        # Use 8 CPUs in a parallel job on this machine
        j = job(modeller_path="/home/software/science/modeller/bin/modslave.py")
        j.append(local_slave())
        j.append(local_slave())
        j.append(local_slave())
        j.append(local_slave())
        j.append(local_slave())
        j.append(local_slave())
        j.append(local_slave())
        j.append(local_slave())
        
        log.verbose()                                # request verbose output
        env = environ()                              # create a new MODELLER environment to build this model in
        
        # directories for input atom files
        env.io.atom_files_directory = '/home/mnellen/pamgene/modeled_NRs/'
        
        # Read in HETATM records from template PDBs
        env.io.hetatm = True
        
        # Loop Optimization
        # Use dope_loopmodel or dopehr_loopmodel in place of loopmodel to obtain better quality loops (but slower)
        if loop:
            a = loopmodel(env,
                      alnfile  = ALI_file,               # alignment filename
                      knowns   = ('subject',),           # codes of the templates
                      sequence = 'query')                # code of the target
        else:
           
            a = automodel(env,
                      alnfile  = ALI_file,               # alignment filename
                      knowns   = ('subject',),           # codes of the templates
                      sequence = 'query')                # code of the target

        a.starting_model= 1                              # index of the first model
        if loop:
            a.ending_model  = 10                             # index of the last model
        else:
            a.ending_model  = 100                            # index of the last model
       
        # Optimization
        # CG
        if loop:
            a.library_schedule = autosched.fast           # Very thorough VTFM optimization
        else:
            
            a.library_schedule = autosched.slow          # Very thorough VTFM optimization
        a.max_var_iterations = 300                    # Select length of optimizations
        a.max_molpdf = 1e6                            # do not stop unless obj.func. > 1E6
        
        # Loop Modelling
        if loop:
            a.loop.starting_model = 1           # First loop model
            a.loop.ending_model   = 10          # Last loop model
            a.loop.md_level       = refine.slow # Loop model refinement level
        
        #MD
        #a.md_level = refine.slow                      # model refinement level
        
        # Repeat the whole cycle 2 times 
        #a.repeat_optimization = 2
        
        a.use_parallel_job(j)                        # Use the job for model building
        a.make()                                     # do the actual homology modeling     


    def loop_searcher(file):
        """This function goes through the file and looks for gaps flanked by amino acids"""
        ALI = open(file, "rU")
        bool = False
        for line in ALI:
            if line.startswith(">"):
               a =re.search('[A-Z]-+[A-Z]',  next(ALI))   #any AAADADA---DSFDSF gaps present?
               if a:
                  bool = True
        return bool



    ## script starts here
    for x in  sys.argv[1:]:       #do modeling for all given files
        loop = loop_searcher(x)   # check for gaps
        modeller_fun(x, loop)     # model




                                                                                      
