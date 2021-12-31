import os
import json
from slc.src.utility import Rule
from slc.src.log_module import log
from slc.src.utility import Rule

def combTables(T1,T2,T1_name,T2_name):
    merged_table={}
    for k1 in T1.keys():
        if("drop" in T1[k1].action or "stop" in T1[k1].action):
            merged_table[k1] = Rule._make([T1[k1].active,int(T1[k1].prio),T1[k1].match,T1[k1].action])
            continue

        for k2 in T2.keys():
            log.debug(" Combining: \n T1[{}]: {} \n T2[{}]: {} ".format(k1,T1[k1],k2,T2[k2]))
            new_match = combMatch(T1[k1].match,T2[k2].match)
            new_action = combAction(T1[k1].action,T1_name,T2_name,T1_name)
            #print(k1, k2, new_match, new_action)
            """print(new_match, new_action)
            for i in range(1000000):
                a = 1""" 
            if(new_action == None):
                continue
            if(len(new_action) > 0):
                new_action += ","
            new_action += combAction(T2[k2].action,T1_name,T2_name,T2_name)
            if new_match is not None and new_action is not None:
                m_name = k1+"_"+k2
                m_active = []
                m_active.append(T1[k1].active)
                m_active.append(',')
                m_active.append(T2[k2].active)
                m_prio = int(T1[k1].prio)*int(T2[k2].prio)

                merged_table[m_name]=Rule._make([''.join(m_active),m_prio,new_match,new_action])
                log.debug(merged_table[m_name])

    comres={}

    for k in merged_table.keys():
        comres[k] = merged_table[k]._asdict() 
    path="slc/data/sahiti_data_fw_idps/"+str(len(T1)-1)+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    json.dump(comres,open(path+T1_name+"_"+T2_name,'w'),indent=4)
    #print(json.dumps(comres,indent=4))
    return merged_table

def combAction(a1,T1_name,T2_name,curr_name):
    new_action = []
    for act in a1.split(","):
        if "drop" in act:
            new_action.append(act)
            new_action.append(',')
        elif "send" not in act:
            act_arr = act.split("(")
            if('-' in act_arr[1]):
                new_action.append(act)
                new_action.append(',')
            else:
                new_action.append(act_arr[0])
                new_action.append('('+curr_name+'-')
                new_action.append(act_arr[1])
                new_action.append(',')
        elif "send" in act:
            next = act.split("(")[1].split(")")[0]
            if(curr_name == T2_name):
                new_action.append(act)
                new_action.append(',')
            elif (next != T2_name):
                return None

    if len(new_action) > 0:
        new_action.pop()
    return ''.join(new_action)



def combMatch(ma1,ma2):
    m1 = ma1.split(",")
    m2 = ma2.split(",")
    wildcard = ['*']
    """print(ma1,ma2)
    for i in range(1000000):
        a=1"""
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
        if (checkClash(d1,d2)):
            return None
        else:
            ma = merge_actions(d1,d2)
            return ma

    return None

def checkClash(d1,d2):
    for k1 in d1.keys():
        if k1 in d2:
            if (k1 == "src" or k1 == "dst" or k1 == "port"):
                if(d1[k1] != d2[k1]):
                    return True
    return False

def merge_actions(d1,d2):
    for k in d2.keys():
        if (k == "src" or k == "dst" or k == "port"):
            if k not in d1:
                d1[k] = d2[k]
    ma = []
    for k, v in d1.items():
        if (k == "src" or k == "dst" or k == "port"):
            ma.append(k)
            ma.append("=")
            ma.append(v)
            ma.append(",")
    if "c" in d1:
        ma.append(d1["c"])
        ma.append(",")
    if "c" in d2:
        ma.append(d2["c"])
        ma.append(",")
    ma.pop()    
    return ''.join(ma)




def m2d(m):
    d = {}
    for item in m:
        if (item.startswith("src") or item.startswith("dst") or item.startswith("port")):
            if("=" in item):
                item_s = item.split("=")
                d[item_s[0]] = item_s[1]
        else:
            d["c"] = item
    return d

"""
def parseC(s):
    item_s = s.split("c")
    res = []
    res.append(parseInt(item_s[0]))
    res.append(parseInt(item_s[1]))
    print(res)
    for i in range(1000000):
        a=1
    return res

def parseInt(s):
    i = 0
    for c in s:
        if c.isdigit():
            i *= 10
            i += ord(c)-ord('0')
            print(c,i)
            for x in range(1000000):
                a = 1
    return i
"""