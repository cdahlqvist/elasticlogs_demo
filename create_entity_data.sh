#/bin/bash

LOGSTASH_PATH="../logstash-2.3.2/bin/logstash"

# First ensure there is a file named 'logs' in the data directory that is larger than 0 bytes
file="./data/logs"
if [ ! -s "$file" ]
then
	echo "ERROR: $file does not exist or does not contain any data."
	exit
fi

# Create file containing entity centric data to index
echo $(date) " Start creating entity centric data file"
cat ./data/logs | $LOGSTASH_PATH -f ./elasticlogs_entity_generation.conf | ./aggregate_entities.py > ./data/entities
echo $(date) " Completed creating entity centric data file"

file="./data/entities"
if [ ! -s "$file" ]
then
	echo "ERROR: $file was not created successfully."
	exit
fi

