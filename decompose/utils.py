import uuid
import subprocess


def write_smv_to_file(smv, filename=None):
    if filename is None:
        filename = str(uuid.uuid4()) + ".smv"
    f = open("./models/" + filename, "w")
    f.write(smv)
    f.close()
    return "./models/" + filename


def run_nusmv_on_file(filename):
    s = subprocess.run(["../NuSMV-2.6.0-win64/bin/NuSMV.exe", filename], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    return s.stdout.decode("utf-8")
