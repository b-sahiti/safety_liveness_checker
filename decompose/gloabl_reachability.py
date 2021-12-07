import json

from slc.src import combine_tables, utility, generate_smv
import utils
import topology as topo
import re


# returns a dict representing the compound table for inputted devices
def combine_all_devices(devices):
    if len(devices) < 2:
        raise Exception("devices length less than two")
    combined = combine_tables.combTables(utility.InputParser(devices[0].rule_file),
                                         utility.InputParser(devices[1].rule_file), devices[0].id, devices[1].id)
    for device in devices[2:]:
        combined = combine_tables.combTables(combined, utility.InputParser(device.rule_file), "comb", device.id)

    res = {"order": [device.id for device in devices]}
    for k in combined.keys():
        res[k] = {"action": combined[k].action, "active": combined[k].active, "match": combined[k].match,
                  "prio": combined[k].prio}

    return res


# return smv string of given compound table
def combined_table_to_smv(table, dst):
    rules_working = list()
    for rule_name in table.keys():
        if rule_name == "order":
            continue
        action = table[rule_name]["action"]
        if "send(" + dst + ")" in action or "send()" in action:
            rules_working.append(rule_name)
    smv = generate_smv.read_compound_table_as_dict(table)
    smv += "LTLSPEC G ("
    for i, rule_name in enumerate(rules_working):
        rule = table[rule_name]
        var_num = len(rule["active"].split(","))
        smv += "("
        for j in range(var_num):
            smv += rule_name + ".active" + str(j + 1) + " = TRUE"
            if j < var_num - 1:
                smv += " & "
        smv += ")"
        if i < len(rules_working) - 1:
            smv += " | "
    smv += ")"
    return smv


# prop: F(src=E,dst=s2;send(s2))
def eventual_reachability(prop, topology):
    paths = list()
    dst_id = re.search('(?<=dst=)\w+', prop).group(0)
    src_id = re.search('(?<=src=)\w+', prop).group(0)
    src_ids = list()

    if src_id == "E":
        for device_id in topology:
            device = topology[device_id]
            if device.is_edge:
                src_ids.append(device_id)
    else:
        src_ids.append(src_id)

    for edge_id in src_ids:
        curr_paths = topo.get_k_shortest_paths(topology, edge_id, dst_id, 2)
        for path in curr_paths:
            paths.append(path)

    for path in paths:
        devices = list()
        for device_id in path:
            devices.append(topology[device_id])
        combined_table = combine_all_devices(devices[:-1])
        print(json.dumps(combined_table, indent=2))
        combined_smv = combined_table_to_smv(combined_table, dst_id)
        smv_file_name = utils.write_smv_to_file(combined_smv)
        print(utils.run_nusmv_on_file(smv_file_name))


if __name__ == '__main__':
    f = open("topo_clos.json")
    graph = topo.load_graph(f)
    eventual_reachability("F(src=E,dst=h1;send(h1))", graph)
