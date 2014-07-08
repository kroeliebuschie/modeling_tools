#!/usr/bin/env python

############################
#                          #
#   This script converts   #
#   an input file into a   #
#  PIR formated ALI file.  #
#                          #
#  author: Mehdi Nellen    #
#       Utrecht 2014       #
############################


import sys
import re

if len(sys.argv) < 2:
    print "This script uses a file containing a HHPRED alignment as input and gives an ALI file as output."
    print "\n     use: HHPRED_to_PIR.py [INPUT FILE] [OUTPUT FILE NAME]"
elif len(sys.argv) < 3:
    print "please specify an output file name. Eg. Target90.ali"
else:
    file = open(sys.argv[1], "rU")
    first_time_Q  = 0
    first_time_T  = 0
    query_seq     = []
    template_seq  = []
    for line in file:
    #this first part only looks at the query sequence
        if line.startswith("  Q") and not line.startswith("  Q Consensus") and not line.startswith("  Q ss_pred"):
            query_seq.extend(re.findall(r'(?<=[0-9] ).*?(?= +[0-9]+ \()', line))
            query_name = re.findall(r'(?<=  Q ).*?(?=:)', line)
            query_end  = re.findall(r'(?<=[0-9] \().*?(?=\))', line)[0]
        #This 'if' is for figuring out the startsite of the query sequence and is only done at the first encounter
        elif line.startswith("  Q Consensus") and first_time_Q == 0:
                first_time_Q = 1
                query_start  = int(re.findall(r'(?<=  Q Consensus).*?(?= [a-zA-Z~])', line)[0])

    #this second part only looks at the template sequence
        if line.startswith("  T") and not line.startswith("  T Consensus") and not line.startswith("  T ss_pred") and not line.startswith("  T ss_dssp"):
            template_seq.extend(re.findall(r'(?<=[0-9] ).*?(?= +[0-9]+ \()', line))
            template_name = re.findall(r'(?<=  T ).*?(?= +[0-9])', line)
            template_end  = re.findall(r'(?<=[0-9] \().*?(?=\))', line)[0]
        #This 'if' is for figuring out the startsite of the template sequence
        elif line.startswith("  T Consensus") and first_time_T == 0:
                first_time_T = 1
                template_start = int(re.findall(r'(?<=  T Consensus).*?(?= [a-zA-Z~])', line)[0])

    #generate the ALI header and sequence for query and subject
    queryALI = ">P1;query\nsequence::%s::%s:::::\n%s*" % (query_start,
                                                          query_end,
                                                          "\n".join(query_seq)
                                                          )
    templateALI = ">P1;subject\nstructure:%s:%s:%s:%s:%s::::\n%s*" % (template_name[0][0:4],      #PDB
                                                                      template_start,             #template start
                                                                      template_name[0][-1],       #chain 
                                                                      template_end,               #template end
                                                                      template_name[0][-1],       #chain
                                                                      "\n".join(template_seq)     #template sequence
                                                                      )
    #write ali to file
    out_file = open(sys.argv[2], 'w')
    out_file.write(queryALI + "\n\n" + templateALI)
    out_file.close()


