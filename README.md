# safety_liveness_checker

Work Flow:

Generate Tables

Express tables as State Machines

Express Property

Verify with Model Checkers (NuSMV and SPIN)


===================================================================================

1. Individual NF table generation

    In slc/data/ there are generator script. It can generate tables of desired sizes.
    Each will have final rule * with default action and priority 1.
    These in turn are input for generating combined tables also.

    For IDPS Tables : python IDPS_table_generator.py <rules count in multiples of 4> > sahiti_data_fw_idps/idps.txt

    For FW (firewalls) Table python Firewall_table_generator.py <count in multiples of 5> > sahiti_data_fw_idps/fw.txt
                        

2. Combine tables Generator

    From top level run python -m slc --combine=1

    It saves combined table to slc/data/<individaul tables folder>/<indiviualsize>/table1_table2

    Generation times and table sizes will be printed.

3. Generate individual NF State Machines.

3.1 For NuSMV
        
        Pranav repo: Original SMV generator but has bug, reachable states error (more than correct)

            Go to slc/src/original_liveness/

            Run python pysmvc.py InividualTableFile PropertyFile

        New: 
            From top level directory.
            
            python -m slc --ind_smv=1 --input_file <absolute path from slc folder>  --output_smv_file  <absolute path from slc folder>

            E.g. : python -m slc --ind_smv=1 --input_file slc/data/sahiti_data_fw_idps/fw5.txt --output_smv_file slc/data/smv_files/fw5.smv


3.2 For SPIN
            From top level directory.
            
            python -m slc --ind_prom=1 --input_file <absolute path from slc folder>  --output_prom_file  <absolute path from slc folder>

            E.g. : python -m slc --ind_prom=1 --input_file slc/data/sahiti_data_fw_idps/fw5.txt --output_prom_file slc/data/prom_files/fw5.smv



4. Generate combined NF State Machines

4.1 For NuSMV

        Go to slc/src/  

        Run python generate_smv.py -f <input> -o <output>

        Eg:python generate_smv.py -f ../data/sahiti_data_fw_idps/100/fw_IDPS -o ../data/sahiti_data_fw_idps/100/fw_IDPS.smv

        Time will be printed per generation

4.2 For SPIN

     Work in progress (Manually done, writing auto-generator)

5. LTL Property Generator

Step - 1 : Both NuSMV and SPIN will need take property of text format (e.g., src=I;send()) and will first need to express it in terms of rules

        For Individual Tables: 

            E.g., python -m slc --ind_prop=1 --input_file slc/data/sahiti_data_fw_idps/fw5.txt --property="src=1000;send()"

        For Compound Tables:
            E.g., python -m slc --compound_prop=1 --input_file slc/data/sahiti_data_fw_idps/5/fw_IDPS --property="src=1000;send()"



Step - 2: Then the rule need to be in standard LTL format

Step - 3: Property format needed for Model Checkers 

5.1 With NuSMV

    Can consume raw ltl 

5.2 With SPIN

    Can consume raw ltl

    But for decomposer, in spot transform ltl to BA, split two BAs, BA to neverclaims, the format needed for SPIN 


Note : Decomposer also takes Step 2 LTL as input, decomposes and generates neverclaims from SPOT, so they can be used in SPIN.

6. Verification

6.1 NuSMV

        NuSMV -int

        read_model -i myfile.smv (this was generated)

        flatten_hierarchy

        encode_variables

        build_model

        go

        process_model

        check_ltlspec -p "<property_from_step2 of 5>"

        compute_reachable [-h]

        print_reachable_states -v



6.2 SPIN

    Work in progress
