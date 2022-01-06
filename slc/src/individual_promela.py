import os
from slc.src.utility import InputParser

def build_individual_table_prom(input,output_file):
    table=InputParser(input)
    output=""
    main_modules={}

    for rule,value in table.items():
        output+="bool " +rule.lower()
        if (value.active).lower()=="true":
            output+="=1;\n"
        else:
            output+="=0;\n"
    run_proctype=[]
    for rule,value in table.items():
        manipulated_actions=get_other_rules(value.action)
        if manipulated_actions:
            run_proctype.append(rule.upper())
            output+="proctype "+rule.upper()+"(){"+"\n\t"
            output+="("+rule.lower()+"==1) -> "
            for k,v in manipulated_actions.items():
                output+=k.lower()+"="
                if v=="delete":
                    output+="0;"
                else:
                    output+="1;"
            output+="\n"+"}\n"
    if run_proctype:
        output+="\n"+"init"+"\n"+"{"
        for proc  in run_proctype:
            output+="\t run "+proc+"();\n"
    output+="}"
    
    o_fp=open(output_file,"w")
    o_fp.write(output)
    o_fp.close()

    print (output)

    

def get_other_rules(actions):
    other_rules={}
    actions=actions.split(",")
    for action in actions:
        if "add" in action:
           other_rule=action[action.find('(')+1:action.find(')')]
           other_rules[other_rule]=action[:action.find('(')]
        elif "delete" in action:
           other_rule=action[action.find('(')+1:action.find(')')]
           other_rules[other_rule]=action[:action.find('(')]
        else:
            continue
    return other_rules 