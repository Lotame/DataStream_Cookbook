#!/usr/bin/python
#
# Write in Python3.6
# Filename:
#
#     Mapping_JsonToCsvExtractor.py
#
#
# Basic Usage:
#
#     python Mapping_JsonToCsvExtractor.py /directory/containing/datastream/mapping/json/files
#

# Utilities
import sys
import os
import json
import argparse


def writeCsvHeader(delimiter, csv_file, *args):
    csv_file.write(delimiter.join(args))
    csv_file.write("\n")

# write a line to the target file
def writeCsvLine(delimiter, csv_file, *args):
    csv_file.write(delimiter.join([str(i) for i in args]))
    csv_file.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Parse the mapping json file to CSV format')
    parser.add_argument('--mapping_path', dest='mapping_path', required=True,
                        help='the path for the mapping json file')
    parser.add_argument('--csv_name', dest='csv_name', required=False, default='mapping.csv',
                        help='specify the file name to write the csv file')
    parser.add_argument('--csv_dir', dest='csv_dir', required=False, default='',
                        help='specify the dir to write the output file')
    parser.add_argument('--delimiter', dest='delimiter', required=False, default='\001',
                        help='specify the delimiter to write the output file')
    args = parser.parse_args()
    mapping_path = args.mapping_path
    csv_dir = args.csv_dir if args.csv_dir else mapping_path
    csv_name = args.csv_name
    delimiter = args.delimiter
    if not os.path.isdir(mapping_path):
        print("The mapping file path does not exist, confirm it again")
        sys.exit()
    if not os.path.isdir(csv_dir):
        print("the specific csv_dir path %s does not exist, create it now" % csv_dir)
        os.system("mkdir -p %s" % csv_dir)
    output_path = os.path.join(csv_dir, csv_name)
    output = open(output_path, 'w')
    writeCsvHeader(delimiter, output, "behavior_id", "hierarchy_path", "hierarchy_id")
    for file in os.listdir(mapping_path):
        if not file.endswith("json"):
            print("%s is not a json file, skip it" % file)
            continue
        file_path = os.path.join(mapping_path, file)
        with open(file_path, 'r') as f:
            for line in f:
                js = json.loads(line.strip())
                behid = js.get('behavior_id')
                # if behavior id smaller than 0, it should be illegal skip
                if behid < 0:
                    continue
                # for each hierarchy, write a line
                for hierpath in js.get('hierarchy_nodes', []):
                    writeCsvHeader(delimiter, output, str(behid), str(hierpath.get("path", "")), str(hierpath.get("id", -1)))

    output.close()




if __name__ == '__main__':
    sys.exit(main())
