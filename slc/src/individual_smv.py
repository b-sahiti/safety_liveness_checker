import os
from slc.src.utility import InputParser

def build_individual_table_smv(input,output_file):
    table=InputParser(input)
    output=""
    main_modules={}
    for rule,value in table.items():
        #print(value)
        main_module=""
        manipulated_rules=get_other_rules(value.action)
        other_rules=list(manipulated_rules.keys())
        if rule.upper() in other_rules:
            other_rules.remove(rule.upper())
        output+="MODULE "+rule + "("
        main_module+= rule+"("
        if len(other_rules)>0:
            for index,key in enumerate(other_rules):
                output+= key.lower()
                main_module+=key.lower()
                if(index < len(other_rules)-1):
                    output+= ","
                    main_module+=","
        output += ")"+"\n"
        main_module+=")"
        main_modules[rule]=main_module
        output += "VAR" + "\n" +"\t"+"active:boolean;" + "\n" + "ASSIGN"+"\n"+"\t"+"init(active) := "+ (value.active).upper()+";"+"\n"
        if len(manipulated_rules.keys())>0:
            #output+= str(manipulated_rules.keys())
            for key,value in manipulated_rules.items():
                output+="\tnext("
                if rule==key:
                    next_key="self.active"
                else:
                    next_key=key.lower()+".active"
                output+=next_key
                output+=") := case"+"\n" +"\t\t" + "self.active : "
                if "add" in value:
                    output+="TRUE;"
                else:
                    output+="FALSE;"
                output+="\n"+"\t\t"+"TRUE : " +next_key+";"+"\n\t\t"+"esac;"+"\n"



        else:
            next_key="self.active"
            output+="\tnext("+next_key+") := case"+"\n\t\t"+"TRUE : "+next_key+";"+"\n"+"esac;"+"\n"

            
        output += "\n"

    output+="MODULE main"+"\n"+"VAR"+"\n\t"
    for main_module,process_name in main_modules.items():
        output+=main_module.lower() + " : process "+process_name+";\n\t"
    
    o_fp=open(output_file,"w")
    o_fp.write(output)
    o_fp.close()
    
    print(output)




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