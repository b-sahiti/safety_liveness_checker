from slc.src.utility import Rule
from slc.src.log_module import log

def combTables(T1,T2):
    merged_table={}
    for k1 in T1.keys():
        for k2 in T2.keys():
            log.debug(" Combining: \n T1[{}]: {} \n T2[{}]: {} ".format(k1,T1[k1],k2,T2[k2]))
            new_match,new_action=combMatch(T1[k1].match,T2[k2].match,T1[k1].action,T2[k2].action)
            if new_match is not None:
                m_name=k1+k2
                m_active=[]
                m_active.append(T1[k1].active)
                m_active.append(T2[k2].active)
                m_prio=int(T1[k1].prio) * int(T2[k2].prio)
                merged_table[m_name]={"active":m_active,"prio":m_prio,"match":new_match,"action":new_action}
                log.debug(merged_table[m_name])
    return merged_table
            

def combMatch(ma1,ma2,a1,a2):
    m1=ma1.split(",")
    m2=ma2.split(",")
    wildcard=['*']
    if (m1==wildcard):
        if(m2==wildcard):
            return '*',a1 + "," + a2
        else:
            return ma2, a1+","+a2 
    elif(m2==wildcard):
        return ma1, a1+","+a1
    else:
        d1=m2d(m1)
        d2=m2d(m2)
        if(checkClash(d1,d2)):
            return [None,None]
        else:
            ma=merge_actions(d1,d2)
            return [ma,a1+","+a2]

    return [None, None]

def checkClash(d1,d2):
    for k1 in d1.keys():
        if k1 in d2:
            if(d1[k1]!=d2[k1]):
                return True
    return False

def merge_actions(d1,d2):
    for k in d2.keys():
        if k not in d1:
            d1[k]=d2[k]
    ma=[]
    for k,v in d1.items():
        ma.append(k)
        ma.append("=")
        ma.append(v)
        ma.append(",")
    ma.pop()    
    return ''.join(ma)




def m2d(m):
    d={}
    for item in m:
        if ("=" in item):
            item_s=item.split("=")
            d[item_s[0]]=item_s[1]
    return d

