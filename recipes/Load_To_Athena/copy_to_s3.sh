#!/usr/bin/env bash

"""
download the data
python DataStreamDownloader.py data/

in our example
python3 GzipExtractor.py ../0/data # unzip the data gz file
python GzipExtractor.py ../0/mapping # unzip the mapping gz file

# the to csv for data stream file may run a long time, the data size if too huge
python3 JsonToCsvConverter.py ../0/data # transform each datastream file to a csv file with the same name in the same directory
python3 Mapping_JsonToCsvConverter.py --mapping_path /directory/containing/my/unzip_mapping_files/ --csv_name mapping.csv --csv_dir /directory/containing/my/target_lookup_dir/  --delimiter "###"

# some files are too hugh to transform to CSV, for example, e15381df-6859-4cb0-b3c1-910ba3e7d77f.json from client 13927
#
"""

# Now assuming you have run all prepare step and we already have the mapping CSV file and the data stream file CSV file.
# Assume you have correctly configure your AWS credential in your command line(https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html)
# This command take very long time to run because the CSV data is too huge

aws s3 cp $PATH_TO_YOUR_LOCAL_MAPPING_CSV_FILE $PATH_TO_YOUR_S3_TARGET_MAPPING_CSV_DIRECTORY
aws s3 cp $PATH_TO_YOUR_LOCAL_DATASTREAM_DIRECTORY/ $PATH_TO_YOUR_S3_TARGET_DATASTREAM_DIRECTORY --exclude "*" --include "*.csv"