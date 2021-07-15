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
        res.append(compound_rule_object.CompoundRule(key, init_states, actions, json_object.keys()))


def main():
    parser = argparse.ArgumentParser(description='converts compound table to a NuSMV file')
    parser.add_argument('-f', '--filename', help='specifies the file location', required=True)
    args = parser.parse_args()
    with open(args.filename) as f:
        smv = read_compound_table(f)


if __name__ == '__main__':
    main()
