import os, json
from collections import namedtuple


Rule=namedtuple('Rule','active, prio, match, action')

def InputParser(input_file: str): 
    Table={}
    #Open and read file line by line.
    #Skip first line as it is column names
    infile = open(input_file, 'r')
    print(input_file)
    lines=infile.readlines()
    for line in lines[1:]:
        line=line.strip()
        row=line.split(" ")
        print(row[1:5])
        curr_rule=Rule._make(row[1:5])
        Table[row[0]]=curr_rule
    #print(json.dumps(Table, indent=4))
    return Table

class CustomVerifier: 
    def __init__(self, table): 
        self.num_rules = len(table.keys())
        self.visited = [0] * (2**self.num_rules)
        self.init_state = [1 if table[k].active == "true" else 0 for k in table.keys()]
        self.table = table
        # only keep add and delete in actions
        for k in self.table.keys():
            new_actions = ""
            for i, action in enumerate(self.table[k].action.split(",")):
                if "add" in action or "delete" in action: 
                    new_actions += action + ","
            if new_actions: # not empty
                new_actions = new_actions[:-1]
                self.table[k]._replace(action = new_actions) 

    # returns an array containing all possible states
    def explore_states(self): 
        # mark init state as visited
        self.visited[self.state_to_decimal(self.init_state)]
        self.explore_child(self.init_state)
        return self.visited

    def explore_child(self, cur_state): 
        for i, e in enumerate(cur_state): 
            if e == 1: # rule is true
                child = cur_state.copy()
                # iterate through actions 
                rule_name = "R" + str(i)
                for action in self.table[rule_name].action.split(","):
                    if "add" in action: 
                        target = action[4:-1]
                        target_idx = int(target.strip("R"))
                        child[target_idx] = 1
                    elif "delete" in action: 
                        target = action[7:-1]
                        target_idx = int(target.strip("R"))
                        child[target_idx] = 0
                
                # if visited, stop
                if self.visited[self.state_to_decimal(child)]: 
                    return 
                else:
                    self.visited[self.state_to_decimal(child)] = 1
                    self.explore_child(child)

    def state_to_decimal(self, state): 
        sum = 0
        for i, e in enumerate(state): 
            if e == 1: 
                sum += (2**i) * e
        return sum
    def decimal_to_state(self, num): 
        return [ "true" if int(i) else "false" for i in list('{0:0b}'.format(num))]
    

if __name__ == "__main__":
    idps = InputParser("../data/idps.txt")
    verifier = CustomVerifier(idps)
    possible_states = verifier.explore_states()
    print("possible states are: ", possible_states)
    for i, e in enumerate(possible_states): 
        if e == 1: # state visited
            print(verifier.decimal_to_state(i))
