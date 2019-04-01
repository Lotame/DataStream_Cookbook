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