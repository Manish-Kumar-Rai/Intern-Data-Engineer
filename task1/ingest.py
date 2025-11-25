import json
import re
import os
# import mysql.connector

#-- files
input_file = 'task1_d.json'
output_file = 'task1_d_valid.json'

with open(input_file,'r') as file:
    raw_data = file.read()

# converting invalid file to valid json file using regex
valid_json = re.sub(r':(\w+)\s*=>',r'"\1":',raw_data)

# Checking if valid JSON
data = json.loads(valid_json)

# Save final file
with open(output_file,'w',encoding='utf-8') as f:
    json.dump(data,f,indent=4)

if os.path.getsize(output_file) > 0:
    print("file saved successfully.")