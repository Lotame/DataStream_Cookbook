# Recipe 1.1
#### ...After we unzip and process the data stream file, we need to see what it means...

So I've downloaded some LDX DataStream files. In this recipe, specifically, they go into a CSV file. 
However, I see a bunch of behavior ids in the data, but don't know what any of them mean! We need a lookup file to check the meaning of the behaviors. In this task, we try to transform multiple mapping.json.gz files got from recipe 0
to one single CSV File for behavior lookup.


## Unzip the mapping.json.gz file

First, we need to unzip the mapping file.
Similar to the introduction for recipe 1, I can just do this
```bash
python GzipExtractor.py /directory/containing/my/mapping_files/
```
... and all that `.gz` goodness is now `.json` grandeur.

## Transform the mapping file to csv

Now, after getting the unzipped mapping file, it is in JSON format, which is fine for python but maybe we want to load this data into Excel or into a database as a table. We can easily do that using the JsonToCsvConverter.py script:

```bash
# The result is not technically a csv file - because some behavior paths include ",", we use special char \x01 as a delimiter instead of ",". However you 
# are able to set to others. But don't suggest to set to "," or "\t", it may break the file format.
# If you don't specify the csv_name, the name will be mapping.csv, if you don't specify csv_dir, the default will be identical to your mapping_path.
python3 JsonToCsvConverter.py --mapping_path /directory/containing/my/unzip_mapping_files/ --csv_name mapping.csv --csv_dir /directory/containing/my/target_lookup_dir/  --delimiter "###"
```

## Check the output result
Now we can check out the tabular-formatted file:

```bash
head -n 6 mapping.csv
```

```bash
behavior_id###hierarchy_path###hierarchy_id
40429###Lotame Age Hierarchy^65+^Declared 65+^82###523648
648419###Lotame Data Selling Network - Location Hierarchy^Countries^South Africa###677728
990937###Lotame Data Selling Network - Location Hierarchy^Timezones^Africa^Bissau###3616352
2296547###Lotame Category Hierarchy^Technographics^Browser^Safari###523998
42524185###*Lotame B2B^Industry^Consumer Services###1049476
```

Now after we generate the mapping.csv file, though is not a real CSV due to the delimiter, we can view the result now!

```bash
# Assume the dilimiter is ###, if you want to look up what behavior ids 42524185, 6465533, 42524230 , 25723899 mean, you can simply do this
behavior="42524185,6465533,42524230,25723899"
IFS=','
awk -v behavior="$behavior" 'BEGIN { FS = "###"; split(behavior, arr, ","); for (i in arr) valuesAsKeys[arr[i]] = ""}; {if ($1 in valuesAsKeys) print $0}' mapping.csv
```

This is what the result looks like 

```bash
42524185###*Lotame B2B^Industry^Consumer Services###1049476
6465533###Lotame Action Hierarchy^Past Purchases###52767
25723899###Lotame Category Hierarchy^Entertainment^Television^Television Networks^ESPN###52728
25723899###Lotame Category Hierarchy^Sports & Recreation^Ice Hockey^College Ice Hockey###52643
25723899###Lotame Category Hierarchy^Sports & Recreation^Basketball^College Basketball###52618
25723899###Lotame Category Hierarchy^Sports & Recreation^Baseball^College Baseball###52615
25723899###Lotame Category Hierarchy^Sports & Recreation^Football (American)^College Football###52634
42524230###*Lotame B2B^Company Revenue^Less than $500K###1049474
```

Now you can start to enjoy the fun from data stream!!
