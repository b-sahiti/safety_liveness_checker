import os
import json
from decompose.slc.src.log_module import log
from collections import namedtuple

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))


def get_relative_to_working_directory(file: str):
    return os.path.abspath(os.path.join(os.getcwd(), file))

Rule=namedtuple('Rule','active, prio, match, action')

def InputParser(input_file: str): 
    #Check if file exists
    if not os.path.exists(input_file):
        log.error("could not open input file '%s'", input_file)
        exit(1)
    Table={}
    #Open and read file line by line.
    #Skip first line as it is column names
    infile = open(input_file, 'r')
    log.debug(input_file)
    lines=infile.readlines()
    for line in lines[1:]:
        line=line.strip()
        row=line.split(" ")
        log.debug(row[1:5])
        curr_rule=Rule._make(row[1:5])
        Table[row[0]]=curr_rule
    print(json.dumps(Table, indent=4))
    return Table