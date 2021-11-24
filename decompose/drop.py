import decompose.network_function as nf
import decompose.topology as topo
import re

k = 2


# prop: src=E,dst=I;drop()
def global_drop(prop, topology):
    paths = list()
    dst_id = re.search('(?<=dst=)\w+', prop).group(0)
    src_id = re.search('(?<=src=)\w+', prop).group(0)
    src_ids = list()

    if src_id == "E":
        for device_id in topology:
            device = topology[device_id]
            if device.is_edge:
                src_ids.append(device_id)
    else:
        src_ids.append(src_id)

    for edge_id in src_ids:
        curr_paths = topo.get_k_shortest_paths(topology, edge_id, dst_id, k)
        for path in curr_paths:
            paths.append(path)

    for path in paths:
        dropping = False
        for device_id in path:
            dropping = False
            device = topology[device_id]
            if device.local_drop(prop):
                dropping = True
                break
        # if reach here, then none of the device along the path always drops the packet
        if not dropping:
            return False
    return True


if __name__ == '__main__':
    f = open("topo_sample.json")
    graph = topo.load_graph(f)
    print(global_drop("src=E,dst=I;drop()", graph))
    paths = topo.get_paths(graph, "fw1", "switch2")
    print(paths)
