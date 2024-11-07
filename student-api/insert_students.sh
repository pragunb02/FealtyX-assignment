#!/bin/bash

# Start Flask app (on the port provided by Render)
python3 app.py &

# Wait for the app to start (optional, you can adjust the sleep time if needed)
sleep 5

# Run the student insertion script (if Flask is up and running)
./insert_students.sh
