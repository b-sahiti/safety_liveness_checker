import distutils.util
import re


class CompoundRule:
    """
    name: compound rule name
    init_states: list of string version of boolean of parent rule initial states
    actions: a string representing actions
    other_compound_rules: list of names of all other compound rules
    """

    def __init__(self, name, init_states, actions, other_compound_rules, table_order):
        self.name = name
        self.num_tables = len(str.split(name, "_"))
        self.init_states = str.split(init_states, ",")
        self.actions = str.split(actions, ",")
        self.other_compound_rules = other_compound_rules
        self.table_order = table_order

    def to_model_string(self):
        res = ""
        res += "MODULE " + self.name + "("
        for i, rule in enumerate(self.other_compound_rules):
            res += rule
            if i != len(self.other_compound_rules) - 1:
                res += ","
        res += ")\n"

        # Var section
        res += "VAR" + "\n"
        # condition on all self variables
        join_condition = ""
        for i in range(self.num_tables):
            res += "\t" + "active" + str(i + 1) + ":boolean;" + "\n"
            join_condition += "self.active" + str(i + 1)
            if i != self.num_tables - 1:
                join_condition += " & "

        # Assign section
        res += "ASSIGN\n"
        # init
        for i in range(len(self.init_states)):
            res += "\tinit(" + "active" + str(i + 1) + ") := "
            res += self.init_states[i].upper() + ";" + "\n"

        # Next
        for idx, action in enumerate(self.actions):
            # search for tableName-ruleName
            if not (action.startswith("delete") or action.startswith("add")): continue

            target_table = re.search(r'\((.*?)\)', action).group(1).split("-")[0]
            target_rule = re.search(r'\((.*?)\)', action).group(1).split("-")[1]
            nth = self.table_order.index(target_table)

            other_rules_to_change = list()
            for r in self.other_compound_rules:
                if len(str.split(r, "_")) > nth and str.split(r, "_")[nth] == target_rule:
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

            # add next section for other rules
            for r in other_rules_to_change:
                res += "\tnext(" + r + ".active" + str(nth + 1) + ") := case\n"
                res += "\t\t" + join_condition + " : "
                if action.startswith("delete"):
                    res += "FALSE"
                else:
                    res += "TRUE"
                res += ";\n"
                res += "\t\tTRUE : " + r + ".active" + str(nth + 1) + ";\n\t\tesac;\n"

        return res
