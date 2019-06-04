# Adding more flavor...
#### ...After I have the Lotame Data Stream files downloaded...

#### ~15 minutes and a few ingredients...
1. Lotame Data Stream files: downloaded, uncompressed, and converted into csv format
2. Access to the Amazon AWS CLI, Amazon S3, and Amazon Redshift
3. A burning desire for deeper analytical understandings of your data

#### ...will yield...
* A  to read this data, and do some really basic data analysis.


- - -

NOTE: If this is the first recipe you're following make sure you have completed the [set up instructions](https://github.com/Lotame/DataStream_Cookbook/tree/master/Recipes/lib) found in the lib directory read me. You need to add your Lotame credentials to the lotame.properties file and put that file in the root of your home directory, ~/. You only need to do this step once in order to run all these recipes. 

If you get an error stating: `No section: 'default'` then you probably didn't take care of the lotame.properties file first. 

- - - 

## Upload to Amazon S3

First, if you've got uncompressed Lotame Data Stream files in csv format on a local machine or stored somewhere that is not Amazon S3, here is how to rectify that situation.

```bash
aws cp --recursive /directory/containing/my/uncompressed/data/stream/csv/files s3://my-bucket-name/and/where/i/want/my/data/stream/files/to/be/stored
```

There, now your uncompressed Lotame Data Stream files are safe, sound, and secure in an Amazon S3 bucket, and ready for some in depth analysis.

## Import into Redshift

There are a few ways you can import your csv files into a Redshift database, but running this command on your Redshift cluster is the easiest way to go by far.

```sql
COPY lotame.data_stream (id varchar(50),type carchar(10),region varchar(2),country varchar(10),client_id smallint,behavior_id smallint,timestamp bigint,action varchar(1))
FROM 's3://my-bucket-name/and/where/i/want/my/data/stream/files/to/be/stored/' 
CREDENTIALS 'aws_access_key_id=mYACcessKeY;aws_secret_access_key=MYSEcrEtkeY'
```

> Note: Redshift doesn't like csv headers, so you'll want to remove the first line from those csv files if going this route. If this is a typical route that you tend to go, we recommend modifying the `JsontoCsvConverter.py` script to not write the csv header for each file.

> Hint: To remove the first line from a file on a Unix system, try `tail -n +2 filename.csv > filename2.csv`
