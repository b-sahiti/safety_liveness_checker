import os
import argparse
import compound_rule_object
import copy
import json
import time

# input: file input stream handler
# output: list of table object
def read_compound_table(f,f_name):
    f_name=f_name.split("/")
    T_name=f_name[-1]
    json_object = json.load(f)
    output = ""
    res = list()
    for key in json_object:
        name = key
        init_states = json_object[key]["active"]
        actions = json_object[key]["action"]
        other_compound_rules = list(json_object.keys())
        impacted_rules_including_self=get_manipulated_rules(key,T_name,actions,other_compound_rules)
        other_compound_rules.remove(key)
        #print(key,impacted_rules_including_self)
        res.append(compound_rule_object.CompoundRule(key, init_states, actions,impacted_rules_including_self ))
    for compoundRule in res:
        output += compoundRule.to_model_string()

    
    processes={}
    for r in res:
        processes[r.name]=[rt[1] for rt in r.set_impacted]
        #processes[r.name]=[rt[1] for rt in r.other_impacted_rules]

    main_mod = "MODULE main" + "\n" + "VAR" + "\n"


    for key in json_object.keys():
        main_mod += "\t" + key + " : process "
        main_mod += key + "("

        for i, rule in enumerate(processes[key]):
            main_mod += rule
            if i != len(processes[key]) - 1:
               main_mod += ","

        main_mod += ");\n"
    output += main_mod
    return output

def get_manipulated_rules(key,T_name,actions,other_rules):
    T_name=T_name.split("_")
    actions=actions.split(',')
    original_actions=list(actions)
    actions=[s[s.find("(")+1:s.find(")")] for s in actions ]
    if '' in actions:
        actions.remove('')
    impacted_rules=[]
    if len(actions)==0:
        return impacted_rules

    for original_action in original_actions:
        action = original_action[original_action.find("(")+1:original_action.find(")")]
        if(action == ''):
            continue
        #TODO: Need to generalize this beyong 2 position
        position = 0;
        for y in range(len(T_name)):
            if '-' not in action:
                position=0
                break 
            if action.split('-')[0]==T_name[y]:
                position=y
                action=action.split('-')[1]
                break;

        for rule in other_rules:
            split_rule=rule.split("_")
            if len(split_rule)>position:
                if action in split_rule[position]:
                    impacted_rules.append((original_action,rule,position))
    return impacted_rules


def main():
    parser = argparse.ArgumentParser(description='converts compound table to a NuSMV file')
    parser.add_argument('-f', '--filename', help='specifies the file location', required=True)
    parser.add_argument('-o', '--output', help='specifies the file location to output', required=True)
    args = parser.parse_args()
    T_name=args.filename

    start1=time.time()
    with open(args.filename) as f_input:
        with open(args.output, "w") as f_output:
            start2=time.time()
            smv = read_compound_table(f_input,T_name)
            end=time.time()
            print(f"Time for generating {args.output} without io = {(end-start2)*1000} milliseconds")
            f_output.write(smv)
            f_output.close()
            end=time.time()
            print(f"Time for generating {args.output} with io = {(end-start1)*1000} milliseconds")


if __name__ == '__main__':
    main()
