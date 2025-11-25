import json
import re
import os
# import mysql.connector

#-- files
input_file = './data/task1_d.json'
output_file = './data/task1_d_valid.json'

#-- fix encoding

def clean_price(price_str):
    '''Convert price sting to float in USD, handling $ & mis-encoded euro.'''
    if not price_str:
        return None
    euro_symbols = ['\u20ac', '\u00e2\u201a\u00ac']  # euro variants
    is_euro = any(sym in price_str for sym in euro_symbols)

    # Remove all non-digit/non-dot characters
    cleaned = re.sub(r'[^\d.]','',price_str)
    try:
        price = float(cleaned)
        if is_euro:
            price *= 1.2
        return round(price,2)
    except ValueError:
        return None
    
def fix_encoding(text):
    ''' Fix mis-encoded UTF-8 text.'''
    if not text:
        return text
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError,UnicodeDecodeError):
        return text


# read raw file
with open(input_file,'r',encoding='utf-8') as file:
    raw_data = file.read()

# converting invalid file to valid json file using regex
valid_json = re.sub(r':(\w+)\s*=>', r'"\1": ', raw_data)

# Checking if valid JSON
data = json.loads(valid_json)

for record in data:
    if 'price' in record:
        record['price'] = clean_price(record['price'])
    for field in ['author', 'title', 'publisher', 'genre']:
        if field in record:
            record[field] = fix_encoding(record[field])

# Save final file
with open(output_file,'w',encoding='utf-8') as f:
    json.dump(data,f,indent=4)

if os.path.getsize(output_file) > 0:
    print("file saved successfully.")
