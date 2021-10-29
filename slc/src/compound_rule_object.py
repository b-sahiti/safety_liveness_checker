import distutils.util
import re


class CompoundRule:
    """
    name: compound rule name
    init_states: list of string version of boolean of parent rule initial states
    actions: a string representing actions
    other_compound_rules: list of names of all other compound rules
    """

    def __init__(self, name, init_states, actions,impacted_rules_including_self):
        self.name = name
        self.num_tables = len(str.split(name, "_"))
        self.init_states = str.split(init_states, ",")
        self.actions = str.split(actions, ",")
        self.impacted_rules_including_self=impacted_rules_including_self
        self.other_impacted_rules=[r for r in self.impacted_rules_including_self if r[1] is not self.name]

    def to_model_string(self):
        res = ""
        res += "MODULE " + self.name + "("
        for i, (_,rule,_) in enumerate(self.other_impacted_rules):
            res += rule
            if i != len(self.other_impacted_rules) - 1:
                res += ","
        res += ")\n"

        # Var section
        res += "VAR" + "\n"
        # condition on all self variables
        join_condition = ""
        #for i in range(self.num_tables):
        for i in range(len(self.init_states)):
            res += "\t" + "active" + str(i + 1) + ":boolean;" + "\n"
            join_condition += "self.active" + str(i + 1)
            if i != len(self.init_states) - 1:
                join_condition += " & "
        #print(res,join_condition)


        # Assign section
        res += "ASSIGN\n"
        # init
        for i in range(len(self.init_states)):
            res += "\tinit(" + "active" + str(i + 1) + ") := "
            res += self.init_states[i].upper() + ";" + "\n"

        # Next
        # Find if we manipulate ourself and add next for our actives accordingly
        for a in self.impacted_rules_including_self:
            (action,rule,position)=a
            if rule==self.name:
                #print(action,rule,position)
                if not (action.startswith("delete") or action.startswith("add")): continue
                res += "\tnext(" + "self.active" + str(position + 1) + ") := case\n"
                res += "\t\t" + join_condition + " : "
                if action.startswith("delete"):
                    res += "FALSE"
                else:
                    res += "TRUE"
                res += ";\n"
                res += "\t\tTRUE : " + "self.active" + str(position + 1) + ";\n\t\tesac;\n"
                self.impacted_rules_including_self.remove(a)

        #Find other rules/processes we manipulate and change their actives
        #for idx, action in enumerate(self.actions):
        for idx, (action,rule,position) in enumerate(self.impacted_rules_including_self):
            # search for tableName-ruleName
            if not (action.startswith("delete") or action.startswith("add")): continue

            #target_table = re.search(r'\((.*?)\)', action).group(1).split("-")[0]
            #target_rule = re.search(r'\((.*?)\)', action).group(1).split("-")[1]
            #target_rule = rule
            #nth = self.table_order.index(target_table)
            #nth = position
            """
            other_rules_to_change = list()
            for r in self.other_compound_rules:
                if str.split(r, "_")[nth] == target_rule:
                    other_rules_to_change.append(r)

            if str.split(self.name, "_")[nth] == target_rule:
                res += "\tnext(" + "self.active" + str(nth + 1) + ") := case\n"
                res += "\t\t" + join_condition + " : "
                if action.startswith("delete"):
                    res += "FALSE"
                else:
                    res += "TRUE"
                res += ";\n"
                res += "\t\tTRUE : " + "self.active" + str(nth + 1) + ";\n\t\tesac;\n"
            """
            # add next section for other rules
            #for r in other_rules_to_change:
            res += "\tnext(" + rule + ".active" + str(position + 1) + ") := case\n"
            res += "\t\t" + join_condition + " : "
            if action.startswith("delete"):
                    res += "FALSE"
            else:
                res += "TRUE"
            res += ";\n"
            res += "\t\tTRUE : " + rule + ".active" + str(position + 1) + ";\n\t\tesac;\n"
        #print(res)

        return res
