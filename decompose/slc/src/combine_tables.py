from decompose.slc.src.log_module import log
from decompose.slc.src.utility import Rule
import re


def is_first_table(T1):
    for k in T1.keys():
        for act in T1[k].action.split(","):
            if "drop" not in act and "send" not in act:
                if len(re.search(r'\((.*?)\)', act).group(1).split("-")) != 1:
                    return False
    return True


def add_table_name_to_action(actions, table_name):
    new_action = []
    for act in actions.split(","):
        if "send" not in act and "drop" not in act:
            act_arr = act.split("(")
            if '-' in act_arr[1]:
                new_action.append(act)
                new_action.append(',')
            else:
                new_action.append(act_arr[0])
                new_action.append('(' + table_name + '-')
                new_action.append(act_arr[1])
                new_action.append(',')
        else:
            new_action.append(act)
            new_action.append(',')

    if len(new_action) > 0:
        new_action.pop()
    return ''.join(new_action)


def combTables(T1, T2, T1_name, T2_name):
    merged_table = {}
    for k1 in T1.keys():

        if "drop" in T1[k1].action or "stop" in T1[k1].action:
            if is_first_table(T1):
                merged_table[k1] = Rule._make(
                    [T1[k1].active, int(T1[k1].prio), T1[k1].match, add_table_name_to_action(T1[k1].action, T1_name)])
            else:
                merged_table[k1] = Rule._make([T1[k1].active, int(T1[k1].prio), T1[k1].match, T1[k1].action])
            continue

        for k2 in T2.keys():
            # print(" Combining: \n T1[{}]: {} \n T2[{}]: {} ".format(k1, T1[k1], k2, T2[k2]))
            new_match = combMatch(T1[k1].match, T2[k2].match)
            new_action = combAction(T1[k1].action, T1_name, T2_name, T1_name)
            if new_action is None:
                continue
            if len(new_action) > 0:
                new_action += ","
            new_action += combAction(T2[k2].action, T1_name, T2_name, T2_name)
            if new_match is not None and new_action is not None:
                m_name = k1 + "_" + k2
                m_active = [T1[k1].active, ',', T2[k2].active]
                m_prio = int(T1[k1].prio) * int(T2[k2].prio)

                merged_table[m_name] = Rule._make([''.join(m_active), m_prio, new_match, new_action])
                log.debug(merged_table[m_name])
    return merged_table


def combAction(a1, T1_name, T2_name, curr_name):
    new_action = []
    for act in a1.split(","):
        if "drop" in act:
            new_action.append(act)
            new_action.append(',')
        elif "send" not in act:
            act_arr = act.split("(")
            if ('-' in act_arr[1]):
                new_action.append(act)
                new_action.append(',')
            else:
                new_action.append(act_arr[0])
                new_action.append('(' + curr_name + '-')
                new_action.append(act_arr[1])
                new_action.append(',')
        elif "send" in act:
            next = act.split("(")[1].split(")")[0]
            if (curr_name == T2_name):
                new_action.append(act)
                new_action.append(',')
            elif (next != T2_name):
                return None

    if len(new_action) > 0:
        new_action.pop()
    return ''.join(new_action)


def combMatch(ma1, ma2):
    m1 = ma1.split(",")
    m2 = ma2.split(",")
    wildcard = ['*']
    if (m1 == wildcard):
        if (m2 == wildcard):
            return '*'
        else:
            return ma2
    elif (m2 == wildcard):
        return ma1
    else:
        d1 = m2d(m1)
        d2 = m2d(m2)
        if (checkClash(d1, d2)):
            return None
        else:
            ma = merge_actions(d1, d2)
            return ma

    return None


def checkClash(d1, d2):
    for k1 in d1.keys():
        if k1 in d2:
            if (d1[k1] != d2[k1]):
                return True
    return False


def merge_actions(d1, d2):
    for k in d2.keys():
        if k not in d1:
            d1[k] = d2[k]
    ma = []
    for k, v in d1.items():
        ma.append(k)
        ma.append("=")
        ma.append(v)
        ma.append(",")
    ma.pop()
    return ''.join(ma)


def m2d(m):
    d = {}
    for item in m:
        if ("=" in item):
            item_s = item.split("=")
            d[item_s[0]] = item_s[1]
    return d
