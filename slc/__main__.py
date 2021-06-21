import os, json
from slc.src.utility import InputParser
from slc.src.combine_tables import combTables
if __name__ == "__main__":
    fw=InputParser("slc/data/firewalls.txt")
    idps=InputParser("slc/data/idps.txt")
    com=combTables(fw,idps)

    print(json.dumps(com,indent=4))