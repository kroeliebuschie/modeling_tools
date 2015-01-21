modeling_tools
==============

##MODELLING 101
1. Query your sequence at HHPRED
2. Follow steps under 'HHPRED_to_PIR.py'
3. Follow steps 'modeller_script.py'
4. Done


#####HHPRED_to_PIR.py
First copy your HHPRED alignment (http://i.imgur.com/qnV3kNA.png) to a file.
This script uses a file containing a HHPRED alignment as input and gives an ALI file as output.
use: 
```bash
HHPRED_to_PIR.py [INPUT FILE] [OUTPUT FILE NAME]
```

#####modeller_script.py
Download the template pdb file and put it in the same directory as the `modeller_script.py` and the `.ALI` file.
Run the following line of code, it will run modeller which automatically checks if it should use automodel or loop model

```bash
modeller_script.py alignment.ALI >& modeller.out

## or submit this script to a cluster
cd /dir/to/modeller_files
python modeller_script.py alignment.ALI >& modeller.out
```

