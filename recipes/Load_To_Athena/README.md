# Recipe Athena
#### ...After I have the csv file for behavior mapping and data stream CSV file...

Assume we have already finished transforming all nested data into an handsome format, like CSV, we can start
to analyze the data.

In this Recipe, we will use AWS Athena to read this data, and do some trivial data analysis.

## Step 1, Copy required data to your S3

```bash

# Now assuming you have run all prepare step and we already have the mapping CSV file and the data stream file CSV file.
# Assume you have correctly configure your AWS credential in your command line(https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html)
# This command take very long time to run because the CSV data is too huge

aws s3 cp $PATH_TO_YOUR_LOCAL_MAPPING_CSV_FILE $PATH_TO_YOUR_S3_TARGET_MAPPING_CSV_DIRECTORY
aws s3 cp $PATH_TO_YOUR_LOCAL_DATASTREAM_DIRECTORY/ $PATH_TO_YOUR_S3_TARGET_DATASTREAM_DIRECTORY --exclude "*" --include "*.csv"
```

## Step 2, Get AWS Athena access and create the External table there refer to a S3 location

In this step, you may have some delimiter problem, here I assume you use "," as the delimiter for the 
data stream sample data, and use a special charactor \001 as the mapping delimiter. You can change them if you want.

```odpsql
-- Assume you have copied all the data to s3 bucket correctly
-- Assume you have access to Athena UI to run the query

CREATE EXTERNAL TABLE DataStream_Sample
(profile_id string, type string, region string, country string, client_source_id string, behavior_id bigint, ts bigint, action string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY  ',' LINES TERMINATED BY '\n'
STORED AS TEXTFILE
location "PATH_TO_YOUR_S3_TARGET_DATASTREAM_DIRECTORY";

CREATE EXTERNAL TABLE Mapping_Sample
(behavior_id bigint, behavior_path string, hierarchy_id int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY  '\001' LINES TERMINATED BY '\n'
STORED AS TEXTFILE
location "$PATH_TO_YOUR_S3_TARGET_MAPPING_CSV_DIRECTORY"
tblproperties ("skip.header.line.count"="1");
```

## Step 3, Analyze the result

Behavior id is annoying, I want to see what kind of interesting behavior I can use in data stream.

```odpsql
select distinct behavior_path from Mapping_Sample limit 200 ;
```

```bash
# Just take a sample here to look at
	Lotame Category Hierarchy^Food & Beverages^Recipes & Cooking
	Lotame Category Hierarchy^Food & Beverages
	Lotame Action Hierarchy^Passive Actions^Watched Video
	Lotame Category Hierarchy^Shopping^Discount Shopping^Black Friday / Cyber Monday
	Lotame Category Hierarchy^Shopping^Discount Shopping
	Lotame Category Hierarchy^Social Media^Facebook
	Lotame Demographic Hierarchy^Languages Spoken^Spanish
	Lotame Category Hierarchy^Careers^Seeking Employment
	Lotame Category Hierarchy^Sports & Recreation^Wrestling
	Lotame Category Hierarchy^Sports & Recreation^Soccer^Premier League
	Lotame Category Hierarchy^Sports & Recreation^Soccer^Premier League^Arsenal
	Lotame Action Hierarchy^Passive Actions^Viewed Photo
	Lotame Action Hierarchy^Influencer Actions^Uploaded Photo
	Lotame Action Hierarchy^Influencer Actions^Uploaded Video
	Lotame Category Hierarchy^Relationships^Dating
```

Oh Man, many interesting behavior names. As a sport fans like me, I want to know what kind of sport is the most popular in our data, so I will do
this to figure out the answer. The hierarchy for sport is this Lotame Category Hierarchy^Sports & Recreation base on the data.

```odpsql
-- Assume we already create DataStream_Sample and Mapping_Sample in Athena
-- Let's run some sample queries in Athena

-- Calculate how many profile add the sport & recreation behavior in the DataStream
Select behavior_path, count(distinct profile_id) cc FROM
Mapping_Sample a
join
DataStream_Sample b
on (a.behavior_id=b.behavior_id)
where
a.behavior_path like 'Lotame Category Hierarchy^Sports & Recreation%' and b.action = 'add'
group by behavior_path order by cc desc;
```

Then we can get the result we are looking for,

```bash

 	behavior_path	cc
	Lotame Category Hierarchy^Sports & Recreation^Football (American)	45380
	Lotame Category Hierarchy^Sports & Recreation^Soccer	41506
	Lotame Category Hierarchy^Sports & Recreation^Camping	40397
	Lotame Category Hierarchy^Sports & Recreation^Sports Equipment	37102
	Lotame Category Hierarchy^Sports & Recreation^Football (American)^National Football League	35929
	Lotame Category Hierarchy^Sports & Recreation^Golf	34403
	Lotame Category Hierarchy^Sports & Recreation^Skiing	33310
	Lotame Category Hierarchy^Sports & Recreation^Baseball	32737
	Lotame Category Hierarchy^Sports & Recreation^Basketball	32506

Surprisingly, Basketball is not very high rank here, that is very interesting. Please go ahead to find your run there!!!
```