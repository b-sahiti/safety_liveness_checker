from liveness import pysmvc
import subprocess
import re

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

    def __init__(self, name, id, is_edge, children_ids, rule_file, smv=None):
        self.name = name
        self.id = id
        self.is_edge = is_edge
        self.children_ids = children_ids
        self.rule_file = rule_file
        self.smv = smv

    # TODO: verify the LTL property directly on the generated smv model
    def verify_property(self, property):
        ltl = pysmvc.helper(self.rule_filename, property, self.name + ".smv")
        # TODO: verify the LTL property generated on the generated smv file

    # return false if device doesn't always drop packets with given condition
    def local_drop(self, match_condition):
        self.smv = "./models" + self.name + ".smv"
        pysmvc.helper(rule_file=self.rule_filename, prop=match_condition + "drop()", smv_filename=self.smv)
        s = subprocess.run(["../NuSMV-2.6.0-win64/bin/NuSMV.exe", self.name + ".smv"], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        res = re.search("(?<=\)\s\sis\s).*(?=\\r)", s.stdout.decode("utf-8")).group(0)
        if res is None:
            raise Exception("LTL result not found")
        elif res == "false":
            return False
        elif res == "true":
            return True
        else:
            raise Exception("unidentifiable LTL result")
