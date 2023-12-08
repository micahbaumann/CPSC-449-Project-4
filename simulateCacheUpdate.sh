
#generated through GPT 

#!/bin/bash

# Define the new data list (as a JSON array)
new_data='["32","34", "35", "36"]'

# Define the new data list as a space-separated string
new_data_list="32 34 35 36"

# Use Python to get the current UTC timestamp
current_timestamp=$(python -c "import datetime; print(datetime.datetime.utcnow().timestamp())")

# Format the JSON string with the new data and timestamp
new_json="{\"data\": $new_data, \"last_modified\": $current_timestamp}"

# Update the Redis key with the new JSON string
redis-cli SET waitlist_4 "$new_json"

# Print a message indicating the update
echo "Updated waitlist_4 with the new data and timestamp: $current_timestamp"

# Delete the existing list in Redis
redis-cli DEL waitClassID_4

# Loop through the new data string and push each item to Redis
for id in $new_data_list; do
    redis-cli RPUSH waitClassID_4 "$id"
done

# Print a message indicating the list update
echo "Updated waitClassID_4 with new data: $new_data_list"
