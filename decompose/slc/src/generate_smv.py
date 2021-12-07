import argparse
import slc.src.compound_rule_object as compound_rule_object
import json


def read_compound_table_as_dict(table):
    res = list()
    order = table['order']
    table.pop("order", None)
    main_mod = ""
    for key in table:
        name = key
        init_states = table[key]["active"]
        actions = table[key]["action"]
        other_compound_rules = list(table.keys())
        other_compound_rules.remove(key)
        res.append(
            compound_rule_object.CompoundRule(key, init_states, actions, other_compound_rules, order))
    for compoundRule in res:
        main_mod += compoundRule.to_model_string()

    main_mod += "MODULE main" + "\n"
    main_mod += "VAR\n"
    for key in table.keys():
        main_mod += "\t" + key + " : process "
        main_mod += key + "("
        other_rules = list(table.keys())
        other_rules.remove(key)
        for i, rule in enumerate(other_rules):
            main_mod += rule
            if i != len(other_rules) - 1:
                main_mod += ","

        main_mod += ");\n"
    print(main_mod)
    return main_mod


# input: file input stream handler
# output: list of table object
def read_compound_table(f):
    json_object = json.load(f)
    return read_compound_table_as_dict(json_object)


def main():
    parser = argparse.ArgumentParser(description='converts compound table to a NuSMV file')
    parser.add_argument('-f', '--filename', help='specifies the file location', required=True)
    args = parser.parse_args()
    with open(args.filename) as f:
        read_compound_table(f)


if __name__ == '__main__':
    main()
