#!/bin/bash

# Base URL
base_url="http://localhost:5300/enroll"

# Common class ID, username, and email
class_id="6"  # Replace with your class ID
username="test"
email="test_email@example.com"

# Enroll 40 students
for student_id in $(seq 1 50); do
    # Construct the URL
    enroll_url="${base_url}/${student_id}/${class_id}/${username}/${email}"

    # Make the HTTP POST request to enroll the student
    curl -X POST "$enroll_url"

    # Optional: Print a message for each enrollment
    echo "Enrolled student ID ${student_id} in class ID ${class_id}"
done

# Finished
echo "All students enrolled."
