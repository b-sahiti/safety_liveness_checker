import os, json, argparse
from slc.src.utility import InputParser
from slc.src.combine_tables import combTables
import time
from slc.src.property_generator import *
from slc.src.individual_smv import read_individual_table


parser = argparse.ArgumentParser()
parser.add_argument('--combine', action='store', type=int,default=0)
parser.add_argument('--compound_prop', action='store', type=int,default=0)
parser.add_argument('--ind_smv', action='store', type=int,default=0)
parser.add_argument('--ind_prop', action='store', type=int,default=0)
parser.add_argument('--input_file', dest="input_file")
parser.add_argument('--property', dest="property")
parser.add_argument('--output_smv_file', dest="output_smv_file")

args=parser.parse_args()


def data_generation_fw_idps():
    for i in [5,10,20,50,100]:
        fw=InputParser("slc/data/sahiti_data_fw_idps/fw{}.txt".format(str(i)))
        idps=InputParser("slc/data/sahiti_data_fw_idps/idps{}.txt".format(str(i)))
        start = time.time()
        fw_idps=combTables(fw,idps,"fw","IDPS")
        end=time.time()
        print(f"fw{len(fw)} idps{len(idps)} fw_idps{len(fw_idps)} {(end-start)*1000} milliseconds")

if __name__ == "__main__":
    if(args.combine):
        data_generation_fw_idps()
    if(args.ind_prop):
        print(args.property)
        t = InputParser(args.input_file)
        print(indTables(t,args.property))
    if(args.compound_prop):
        print(compoundTableConverter('slc/data/fw_IDPS',"src=I;drop"))
    if(args.ind_smv):
        if (args.input_file):
            print(args.output_smv_file)
            #read_individual_table('slc/data/sahiti_data_fw_idps/fw5.txt')
            read_individual_table(args.input_file,args.output_smv_file)
    