import argparse


# input: file input stream handler
# output: table object
def read_compound_table(f):
    return


def main():
    parser = argparse.ArgumentParser(description='converts compound table to a NuSMV file')
    parser.add_argument('-f', '--filename', help='specifies the file location', required=True)
    args = parser.parse_args()
    with open(args.filename) as f:
        smv = read_compound_table(f)

if __name__ == '__main__':
    main()
