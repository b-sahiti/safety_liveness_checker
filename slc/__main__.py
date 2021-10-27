import os, json
from slc.src.utility import InputParser
from slc.src.combine_tables import combTables
import time


def data_generation_fw_idps():
    for i in [5,10,20,50,100]:
        fw=InputParser("slc/data/sahiti_data_fw_idps/fw{}.txt".format(str(i)))
        idps=InputParser("slc/data/sahiti_data_fw_idps/idps{}.txt".format(str(i)))
        start = time.time()
        fw_idps=combTables(fw,idps,"fw","IDPS")
        end=time.time()
        print(f"fw{len(fw)} idps{len(idps)} fw_idps{len(fw_idps)} {(end-start)*1000} milliseconds")

if __name__ == "__main__":
   data_generation_fw_idps() 
    