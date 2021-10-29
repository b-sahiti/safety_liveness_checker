# safety_liveness_checker

1. Individual NF table generation
In slc/data/ there are folders. Each folder will have generator script. It can generate tables of sizes in multiples of 5.
Eg:slc/data/sahiti_data_fw_idps , has generators for idps and fw. These inturm are input for generating combined table

2. Combine tables
from top level run python -m slc
It saves combined table to slc/data/<individaul tables folder>/<indiviualsize>/table1_table2
Times needed will be printed

3. Generate individual NF smv

Currently done in pranav's repo. Need to integrate

4. Generate combined NF smv
In slc/src/ run python generate_smv.py -f <input> -o <output>
Eg:python generate_smv.py -f ../data/sahiti_data_fw_idps/100/fw_IDPS -o ../data/sahiti_data_fw_idps/100/fw_IDPS.smv
Time will be printed per generation

5. property Verification
