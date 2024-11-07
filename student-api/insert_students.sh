#!/bin/bash

for i in {1..20}
do
  curl -X POST https://fealtyx-1.onrender.com/ \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Student $i\", \"age\": $((18 + $i)), \"email\": \"student$i@example.com\"}"
  echo ""
done
