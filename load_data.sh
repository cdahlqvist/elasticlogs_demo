#/bin/bash

ESHOST="127.0.0.1:9200"
LOGSTASH_PATH="../logstash-2.3.2/bin/logstash"

# First ensure there is a file named 'logs' in the data directory that is larger than 0 bytes
file="./data/logs"
if [ ! -s "$file" ]
then
	echo "ERROR: $file does not exist or does not contain any data."
	exit
fi

file="./data/entities"
if [ ! -s "$file" ]
then
	echo "ERROR: $file does not exist or does not contain any data."
	exit
fi

# Ensure the correct index template is loaded
curl -XPOST http://$ESHOST/_template/elasticlogs -d @elasticlogs_template.json

# Load both raw and entity centril data into Elasticsearch
echo $(date) " Start loading entity centric data file"
cat ./data/entities | $LOGSTASH_PATH -f ./elasticlogs_entities.conf
echo $(date) " Completed loading entity centric data file"

echo $(date) " Start loading raw data file"
cat ./data/logs | $LOGSTASH_PATH -f ./elasticlogs_raw.conf > ./data/errors
echo $(date) " Completed loading raw data file"
