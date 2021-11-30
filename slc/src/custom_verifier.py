import os, json
from collections import namedtuple
from time import time


Rule=namedtuple('Rule','active, prio, match, action')

def InputParser(input_file: str): 
    Table={}
    #Open and read file line by line.
    #Skip first line as it is column names
    infile = open(input_file, 'r')
    print("Reading from ", input_file)
    lines=infile.readlines()
    print("Rules: ")
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
        # self.visited = [0] * (2**self.num_rules)
        self.visited = set()
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
    
    def get_num_rules(self): 
        return self.num_rules

    # find mutable states
    def find_mutable(self): 
        mutable = [0] * self.num_rules
        queue = []
        for i in range(self.num_rules): 
            if self.init_state[i]: 
                queue.append(i)

        # print("Initial queue is ", queue)
        while(len(queue)): 
            rule = "R" + str(queue.pop())
            active = self.table[rule].active
            for action in self.table[rule].action.split(","):
                if ("add" in action):
                        target = action[4:-1]
                        if (self.table[target].active == "false"):
                            target_idx = int(target.strip("R"))
                            if not mutable[target_idx]: 
                                queue.append(target_idx)
                            mutable[target_idx] = 1
                elif("delete" in action):
                    target = action[7:-1]
                    if(self.table[target].active == "true"): 
                        target_idx = int(target.strip("R"))
                        mutable[target_idx] = 1
        return mutable
                    

    # returns an array containing all possible states
    def explore_states(self): 
        # mark init state as visited
        self.visited.add(self.state_to_decimal(self.init_state))
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
                if self.state_to_decimal(child) in self.visited: 
                    continue 
                else:
                    self.visited.add(self.state_to_decimal(child))
                    self.explore_child(child)

    def state_to_decimal(self, state): 
        sum = 0
        l = len(state)
        for i in range(l): 
            e = state[i]
            if e == 1: 
                sum += (2**(l-i-1))
        return sum
    def decimal_to_state(self, num): 
        return [ "true" if int(i) else "false" for i in list('{0:0{len}b}'.format(num, len=self.num_rules))]
    

if __name__ == "__main__":
    idps = InputParser("../data/sahiti_data_fw_idps/fw100.txt")
    start = time()
    verifier = CustomVerifier(idps)
    possible_states = verifier.explore_states()
    end = time()
    print("Time used: ", '{:.4f} ms'.format((end - start) * 1000))
    num_all_states = 2**verifier.get_num_rules()
    # print("All states (num={}):".format(num_all_states), possible_states)
    num_visited_states = len(possible_states)
    print("Explored (num={}/{}={}%)".format(num_visited_states, num_all_states, num_visited_states / num_all_states * 100))
    for i, e in enumerate(possible_states): 
        if e == 1: # state visited
            print("decimal: {}".format(i), verifier.decimal_to_state(i))

    print("Mutable states:")
    start = time()
    mutable = verifier.find_mutable()
    end = time()
    print(mutable)
    upper_bound = pow(2, sum(mutable))
    print("Upper bound of possible states: {} (num={}/{}={}%)".format(upper_bound, upper_bound, num_all_states, upper_bound / num_all_states * 100))
    print("Time used: ", '{:.4f} ms'.format((end - start) * 1000))
