import argparse
import compound_rule_object

import json


# input: file input stream handler
# output: list of table object
def read_compound_table(f):
    json_object = json.load(f)
    res = list()
    for key in json_object:
        name = key
        init_states = json_object[key]["active"]
        actions = json_object[key]["action"]
        other_compound_rules = list(json_object.keys())
        other_compound_rules.remove(key)
        res.append(compound_rule_object.CompoundRule(key, init_states, actions, other_compound_rules, ["fw", "IDPS"]))
    for compoundRule in res:
        print(compoundRule.to_model_string())

    main_mod = "MODULE main" + "\n"


    for key in json_object.keys():
        main_mod += "\t" + key + " : process "
        main_mod += key + "("

        other_rules = list(json_object.keys())
        other_rules.remove(key)
        for i, rule in enumerate(other_rules):
            main_mod += rule
            if i != len(other_rules) - 1:
               main_mod += ","

        main_mod += ")\n"
    print(main_mod)

def main():
    parser = argparse.ArgumentParser(description='converts compound table to a NuSMV file')
    parser.add_argument('-f', '--filename', help='specifies the file location', required=True)
    args = parser.parse_args()
    with open(args.filename) as f:
        smv = read_compound_table(f)


if __name__ == '__main__':
    main()
