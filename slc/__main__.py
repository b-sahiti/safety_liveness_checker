import os, json
from slc.src.utility import InputParser
from slc.src.combine_tables import combTables
if __name__ == "__main__":
    fw=InputParser("slc/data/firewalls.txt")
    idps = InputParser("slc/data/idps.txt")
    monitor = InputParser("slc/data/monitor.txt")
    #fw = InputParser("data/firewalls1.txt")
    #idps=InputParser("data/idps.txt")
    #monitor = InputParser("data/monitor.txt")
    com=combTables(fw,idps,"fw","IDPS")
    print("Combine fw idps\n")
    print(json.dumps(com, indent=4))
    print(com)
    com2 = combTables(com, monitor, "IDPS", "MONITOR")
    comres={}

    for k in com2.keys():
        comres[k] = com2[k]._asdict()
    print("Combine fw idps monitor\n")
    print(json.dumps(comres, indent=4))