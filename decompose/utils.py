import uuid


def write_smv_to_file(smv, filename=None):
    if filename is None:
        filename = str(uuid.uuid4()) + ".smv"
    f = open("./models/" + filename, "w")
    f.write(smv)
    f.close()
    return "./models/" + filename