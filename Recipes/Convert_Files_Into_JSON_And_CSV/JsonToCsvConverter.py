#!/usr/bin/python
#
# Filename: 
#
#     JsonToCsvConverter.py
#
#
# Basic Usage:
#
#     python JsonToCsvConverter.py /directory/containing/datastream/json/files
#

# Utilities
import sys, os, re, glob, json


def writeCsvHeader(csv_file=None):
    csv_file.write("id,type,region,country,client_id,behavior_id,timestamp,action")
    csv_file.write("\n")


def writeCsvLine(csv_file=None, wrote_header=False, profile_id="", profile_type="", region="", country="", client="",
                 behavior="", timestamp="", add=True):
    if not wrote_header:
        writeCsvHeader(csv_file)
    add_string = "add" if add is True else "remove"
    csv_file.write(str(profile_id) + "," + str(profile_type) + "," + str(region) + "," + str(country) + "," + str(
        client) + "," + str(behavior) + "," + str(timestamp) + "," + add_string)
    csv_file.write("\n")
    return True


def main():
    path = sys.argv[1]
    for json_file in glob.glob(os.path.join(path, '*.json')):
        csv_file = re.sub('.json$', '.csv', json_file)
        with open(json_file, 'rb') as jf:
            with open(csv_file, 'a') as cf:
                wrote_header = False
                for line in jf:
                    json_line = json.loads(line)
                    profile_id = json_line['id']['val']
                    profile_type = json_line['id']['type']
                    country = json_line['country']
                    region = json_line['region']
                    for event in json_line['events']:
                        client = event.get('subSrc', '')
                        timestamp = event['ts']
                        if 'add' in event:
                            for behavior in event['add']:
                                wrote_header = writeCsvLine(csv_file=cf, wrote_header=wrote_header,
                                                            profile_id=profile_id, profile_type=profile_type,
                                                            region=region, country=country, client=client,
                                                            behavior=behavior, timestamp=timestamp, add=True)
                        if 'remove' in event:
                            for behavior in event['remove']:
                                wrote_header = writeCsvLine(csv_file=cf, wrote_header=wrote_header,
                                                            profile_id=profile_id, profile_type=profile_type,
                                                            region=region, country=country, client=client,
                                                            behavior=behavior, timestamp=timestamp, add=False)


if __name__ == '__main__':
    sys.exit(main())
