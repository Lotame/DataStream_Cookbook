# Adding Flavor...
#### ...After I have the Lotame Data Stream files downloaded...

#### ~15 minutes and a few ingredients...
1. Lotame Data Stream files: downloaded, uncompressed, and converted into csv format
2. Lotame Data Stream LDX behavior mapping file downloaded and converted to csv format
2. Access to the Amazon AWS CLI and Amazon Athena
4. A burning desire for deeper analytical understandings of your data

#### ...will yield...
* A better understanding of how to use AWS Athena to read this data, and do some really basic data analysis.

- - -

NOTE: If this is the first recipe you're following make sure you have completed the [set up instructions](https://github.com/Lotame/DataStream_Cookbook/tree/master/Recipes/lib) found in the lib directory read me. You need to add your Lotame credentials to the lotame.properties file and put that file in the root of your home directory, ~/. You only need to do this step once in order to run all these recipes. 

If you get an error stating: `No section: 'default'` then you probably didn't take care of the lotame.properties file first. 

- - - 


## Step 1: Copy DataStream data to an S3 bucket

```bash

# Now assuming you have run all preparation steps and we already have the mapping CSV file and the data stream file CSV file(s).
# Assume you have correctly configured your AWS CLI (command-line interface) credentials (see https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html)
# This command may take a while to run if you have a large amount of data downloaded; if so, you can test using just a few data files instead of the whole set downloaded from previous steps

aws s3 cp $PATH_TO_YOUR_LOCAL_MAPPING_CSV_FILE $PATH_TO_YOUR_S3_TARGET_MAPPING_CSV_DIRECTORY
aws s3 cp $PATH_TO_YOUR_LOCAL_DATASTREAM_DIRECTORY/ $PATH_TO_YOUR_S3_TARGET_DATASTREAM_DIRECTORY --exclude "*" --include "*.csv"
```

## Step 2: Get AWS Athena access and define the table structures

Here I'm assuming you've used:
* `,` as the delimiter for the data stream sample data
* the special charactor `\001` as the mapping delimiter

...as specified in earlier recipes. If you've used other delimiters, you will need to alter these table definitions accordingly.

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

## Step 3, Analyze the results

Since integer behavior ids don't tell me anything useful, let's find some interesting behaviors using the mapping file:

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

Oh man, many interesting behavior names. 

A sport fans like myself- I want to know what kind of sport is the most popular in our data. 

So, I will run some simple analysis on the data to find out. 

The hierarchy for sport is "Lotame Category Hierarchy^Sports & Recreation" in the mapping file, so any behaviors whose paths start with that substring are "sports" behaviors.

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

There. Now we can get the result we are looking for.

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
```

Surprisingly, Basketball is not ranked very highly here. 

Now go find your own surprising and interesting conclusions hidden in your data!

