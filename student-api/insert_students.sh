#!/bin/bash

for i in {1..20}
do
  curl -X POST http://localhost:5001/students \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Student $i\", \"age\": $((18 + $i)), \"email\": \"student$i@example.com\"}"
  echo ""
done
