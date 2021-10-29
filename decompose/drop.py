import decompose.network_function as nf
import decompose.topology as topo
import re


# prop: src=E;dst=I;drop()
def global_drop(prop, topology):
    paths = list()
    dst_id = re.search('(?<=dst=)\w+', prop).group(0)
    edge_devices_ids = list()
    indegrees = set()

    for device_id in topology:
        device = topology[device_id]
        if device.is_edge:
            edge_devices_ids.append(device_id)

    for edge_id in edge_devices_ids:
        curr_paths = topo.get_paths(topology, edge_id, dst_id)
        for path in curr_paths:
            paths.append(path)

    for path in paths:
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
