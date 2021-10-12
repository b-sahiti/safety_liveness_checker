import os, json
from slc.src.utility import InputParser
from slc.src.combine_tables import combTables
if __name__ == "__main__":
    fw=InputParser("slc/data/firewalls.txt")
    idps = InputParser("slc/data/idps.txt")
    monitor = InputParser("slc/data/monitor.txt")
    fw_IDPS=combTables(fw,idps,"fw","IDPS")
    com2=combTables(fw_IDPS,monitor,"fw_IDPS","monitor")
    print("fw_IDPS_monitor")
    print(com2)