# module for graph operations
import network_function as nf
import json


def load_graph(f):
    json_object = json.load(f)
    res = dict()
    for nwfunc in json_object["graph"]:
        id = nwfunc["id"]
        res[id] = nf.NetworkFunction(nwfunc["name"], nwfunc["id"], nwfunc["children_ids"], nwfunc["rule_file"])
    return res


# return list of paths; each path is a list of nwfunc ids
def get_paths(graph, src_id, dst_id):
    return dfs(graph, src_id, dst_id, list(), list(), dict())


def dfs(graph, src_id, dst_id, paths, curr_path, visited):
    if src_id == dst_id:
        paths.append(curr_path)

    curr_nwfunc = graph[src_id]
    for child_id in curr_nwfunc.children_ids:
        if (not visited.has_key(child_id)) or (not visited[child_id]):
            visited[child_id] = True
            dfs(graph, child_id, dst_id, paths, curr_path.append(child_id), visited)
            visited[child_id] = False


# filter: "src=I;dst=E;"
# path: ["fw1", "switch1"]
def verify_path_reachability(path, filter, graph):
    for idx, nwfunc_id in enumerate(path):
        if idx == len(path) - 1:
            break
        nwfunc = graph[nwfunc_id]
        next_nwfunc = graph[path[idx + 1]]
        prop = filter + "send(" + next_nwfunc.id + ");"
        if not nwfunc.verify_property(prop):
            return False


if __name__ == '__main__':
    print("import succeeful")

