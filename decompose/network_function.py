from liveness import pysmvc

"""
Example: 
{
    "graph": [
        {
            "name": "Firewall",
            "id": "fw1",
            "rule_file": "./Firewall.txt",
            "children_ids": [
                "switch1",
                "switch2"
            ]
        },
        {
            "name":"Switch 1",
            "id": "switch1",
            "rule_file": "./switch_1.txt",
            "children_ids": [
            ]
        },
        {
            "name":"Switch 2",
            "id": "switch2",
            "rule_file": "./switch_2.txt",
            "children_ids": [
            ]
        }
    ]
}
"""


class NetworkFunction:
    """
    name: network function name
    children_ids[]: network function ids which it can send packets to
    rule_file: NF rule file that that serves as input to liveness verifier
    smv: address of smv file | string of smv file, etc.
    """

    def __init__(self, name, id, children_ids, rule_file, smv=None):
        self.name = name
        self.id = id
        self.children_ids = children_ids
        self.rule_file = rule_file
        self.smv = smv

    # TODO: verify the LTL property directly on the generated smv model
    def generate_smv(self, property):
        ltl = pysmvc.helper(rule_filename, property, name + ".smv")
        # Then verify the LTL property generated on the generated smv file
