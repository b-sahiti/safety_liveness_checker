# module for graph operations
import network_function as nf


def load_graph(f):
    json_object = json.load(f)
    res = dict()
    for nwfunc in json_object["graph"]:
        id = nwfunc["id"]
        res[id] = nf.NetworkFunction(nwfunc["name"], nwfunc["id"], nwfunc["children_ids"], nwfunc["rule_file"], nwfunc)


# let path be a list of nwfunc ids
def get_paths(graph):
    return []


