import argparse
import compound_rule_object

import json


# input: file input stream handler
# output: list of table object
def read_compound_table(f,T_name):
    json_object = json.load(f)
    output = ""
    res = list()
    for key in json_object:
        name = key
        init_states = json_object[key]["active"]
        actions = json_object[key]["action"]
        other_compound_rules = list(json_object.keys())
        other_compound_rules.remove(key)
        other_impacted_rules=get_manipulated_rules(T_name,actions,other_compound_rules)
        print(name,actions,other_impacted_rules,sep='\t')
        continue
        res.append(compound_rule_object.CompoundRule(key, init_states, actions, other_compound_rules, ["fw", "IDPS"]))
    exit(0)
    for compoundRule in res:
        output += compoundRule.to_model_string()

    main_mod = "MODULE main" + "\n" + "VAR" + "\n"


    for key in json_object.keys():
        main_mod += "\t" + key + " : process "
        main_mod += key + "("

        other_rules = list(json_object.keys())
        other_rules.remove(key)
        for i, rule in enumerate(other_rules):
            main_mod += rule
            if i != len(other_rules) - 1:
               main_mod += ","

        main_mod += ");\n"
    output += main_mod
    return output

def get_manipulated_rules(T_name,actions,other_rules):
    T_name=T_name.split("_")
    actions=actions.split(',')
    actions=[s[s.find("(")+1:s.find(")")] for s in actions ]
    actions.remove('')
    impacted_rules=[]
    if len(actions)==0:
        return impacted_rules
    for action in actions:
        #TODO: Need to generalize this beyong 2 position
        for i in range(len(T_name)):
            if '-' not in action:
                position=0
                break 
            if action.split('-')[0]==T_name[i]:
                position=i
                action=action.split('-')[1]
                break;

        for rule in other_rules:
            split_rule=rule.split("_")
            if len(split_rule)>position:
                if action in split_rule[position]:
                    impacted_rules.append((rule,position))
    return impacted_rules


def main():
    parser = argparse.ArgumentParser(description='converts compound table to a NuSMV file')
    parser.add_argument('-f', '--filename', help='specifies the file location', required=True)
    parser.add_argument('-o', '--output', help='specifies the file location to output', required=True)
    args = parser.parse_args()
    T_name=args.filename
    with open(args.filename) as f_input:
        with open(args.output, "w") as f_output:
            smv = read_compound_table(f_input,T_name)
            f_output.write(smv)
            f_output.close()


if __name__ == '__main__':
    main()
