import decompose.network_function as nf
import decompose.topology as topo
import re


def global_drop(match_fields, topology):
    paths = list()
    dst_id = re.search('(?<=dst=)\w+', match_fields).group(0)
    edge_devices_ids = list()
    indegrees = set()

    # count devices indegree
    for device_id in topology:
        device = topology[device_id]
        for child_id in device.children_ids:
            indegrees.add(child_id)

    for device_id in topology:
        # indegree = 0
        if not (device_id in indegrees):
            edge_devices_ids.append(device_id)

    for edge_id in edge_devices_ids:
        paths.append(topo.get_paths(topology, edge_id, dst_id))
    for path in paths:
        for device_id in path:
            device = topology[device_id]
            if device.local_drop(match_fields):
                break
        # if reach here, then none of the device along the path always drops the packet
        return False
    return True


if __name__ == '__main__':
    f = open("topo_sample.json")
    global_drop("src=I;dst=E;", topo.load_graph(f))
