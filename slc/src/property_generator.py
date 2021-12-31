import json
from slc.src.utility import Rule

def indTables(T,prop):
    action = prop.split(";")[1]
    match = prop.split(";")[0]

    if "drop" in action:
        action = "drop"
    elif "send" in action:
        action = "send"
    else:
        return "Incorrect action"

    match = m2d(match.split(","))

    rowDict = {}
    num = 0

    for key in T.keys():
        rowDict[num] = key
        num = num+1

    #print(rowDict)

    res = []

    currres = []
    currres.append("(")

    checkRule(T,0,currres,res,match,action,rowDict)

    if len(res) > 0:
        res.pop()
        return ''.join(res)
    else:
        return ""






def checkRule(T,curr,currres,res,match,action,rowDict):
    if curr >= len(rowDict):
        return
    d2 = m2d(T[rowDict[curr]].match.split(","))
    if "*" not in T[rowDict[curr]].match and checkClash(match, d2):
        #print(curr, " ::: No Match")
        checkRule(T, curr+1, currres, res, match, action, rowDict)
    else:
        if action in T[rowDict[curr]].action:
            #print(curr," ::: cond1")
            currres.append(rowDict[curr])
            currres.append("=")
            currres.append("TRUE")
            currres.append(")")
            res.append(''.join(currres))
            res.append("V")
            currres = currres[:-4]
            currres.append(rowDict[curr])
            currres.append("=")
            currres.append("FALSE")
            #currres.append("^")
            currres.append("&")
            checkRule(T, curr + 1, currres, res, match, action, rowDict)
            currres = currres[:-4]
        elif action == "drop" and curr == len(rowDict)-1 and "send" in T[rowDict[curr]].action:
            #print(curr, " ::: cond2")
            currres.append(rowDict[curr])
            currres.append("=")
            currres.append("FALSE")
            currres.append(")")
            res.append(''.join(currres))
            res.append("V")
            currres = currres[:-4]

        else:
            #print(curr, " ::: cond3")
            currres.append(rowDict[curr])
            currres.append("=")
            currres.append("FALSE")
            #currres.append("^")
            currres.append("&")
            checkRule(T, curr + 1, currres, res, match, action, rowDict)
            currres = currres[:-4]



def checkClash(d1,d2):
    for k1 in d1.keys():
        if k1 in d2:
            if (k1 == "src" or k1 == "dst" or k1 == "port"):
                if(d1[k1] != d2[k1]):
                    return True
        else:
            return True
    return False

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

def compoundTableConverter(file, property):
    f = open(file, )
    T = json.load(f)
    T = dict(sorted(T.items(), key=lambda x: x[1]['prio'], reverse=True))
    for key in T.keys():
        #print(key,":::",T[key]['prio'],":::",T[key]['match'],":::",T[key]['action'])
        createRule(T,key)

    #print(T['R0_R0'].match)
    return indTables(T,property)

def createRule(T,key):
    T[key] = Rule._make([T[key]['active'],T[key]['prio'],T[key]['match'],T[key]['action']])