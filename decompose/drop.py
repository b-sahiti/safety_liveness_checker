import decompose.network_function as nf
import decompose.topology as topo
import re


def global_drop(match_fields, topology):
    paths = list()
    dst_id = re.search('(?<=dst=)\w+', match_fields).group(0)
    for edge_id in topology:
        paths.append(topo.get_paths(topology, edge_id, dst_id))
    for path in paths:
        for device_id in path:
            device = topology[device_id]
            if not device.local_drop(match_fields):
                return False
    return True


if __name__ == '__main__':
    f = open("topo_sample.json")
    global_drop("src=I;dst=E;", topo.load_graph(f))
