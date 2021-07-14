class CompoundRule:
    def __init__(self, name, parent_rules, init_states, actions, other_compound_rules):
        self.name = name
        self.parent_rules = parent_rules
        self.init_states = init_states
        self.actions = actions
        self.other_compound_rules = other_compound_rules

    def to_model_string(self):
        res = ""
        res += "MODULE " + self.name + "("
        for rule in self.other_compound_rules:
            res += rule + ","
        res += ")\n"

        # Var section
        res += "VAR" + "\n"
        res += "\t" + "active1:boolean;" + "\n"
        res += "\t" + "active2:boolean;" + "\n"

        # Assign section
        res += "ASSIGN\n"
        i = 0
        for state in self.init_states:
            res += "\tinit(" + "active" + str(i)
            i += 1
