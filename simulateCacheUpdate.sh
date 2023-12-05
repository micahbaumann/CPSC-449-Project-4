#!/bin/bash

# Use Python to get the current UTC timestamp
current_timestamp=$(python -c "import datetime; print(datetime.datetime.utcnow().timestamp())")

# Format the JSON string with the new timestamp
new_json="{\"data\": 1, \"last_modified\": $current_timestamp}"

# Update the Redis key with the new JSON string
redis-cli SET waitlist_4_33 "$new_json"

# Print a message indicating the update
echo "Updated waitlist_4_33 with the new timestamp: $current_timestamp"
