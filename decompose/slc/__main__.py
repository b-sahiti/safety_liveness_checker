import json
from decompose.slc.src.utility import InputParser
from decompose.slc.src.combine_tables import combTables
if __name__ == "__main__":
    fw=InputParser("../rules/eventual_reachability/clos_firewall_1.txt")
    s1 = InputParser("../rules/eventual_reachability/clos_spine_1.txt")
    s2 = InputParser("../rules/eventual_reachability/clos_tor_1.txt")
    order = ["fw", "sp1", "s1"]
    com=combTables(fw,s1,order[0],order[1])
    print("Combined fw s1\n")
    print(json.dumps(com, indent=4))
    # print(com)
    com2 = combTables(com, s2, "comb1", order[2])
    res = {"order": order}
    for k in com2.keys():
        res[k] = {"action": com2[k].action, "active": com2[k].active, "match": com2[k].match, "prio": com2[k].prio}
    print("Combine all three\n")
    print(json.dumps(res, indent=4))