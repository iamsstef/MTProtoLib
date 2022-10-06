#!/usr/bin/env python

from MTProtoLib import MTProto
import csv, time

API_ID = 1234 #REPLACE 1234 WITH YOUR API ID
API_HASH = 'REPLACE_WITH_YOUR_API_HASH'
BOT_TOKEN = 'REPLACE_WITH_YOUR_BOT_TOKEN'

MTProto = MTProto("csv_extractor_session", API_ID, API_HASH, BOT_TOKEN)

header = ['chat_id', 'chat_title', 'username', 'chat_type', 'date']
unix_timestamp = str(round(time.time()))

print(f"Writing data into 'csv_extractor_{unix_timestamp}.csv'...")

with open(f'csv_extractor_{unix_timestamp}.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in MTProto.GetDifferenceRequest():
        writer.writerow(row)

print("Done. Exiting...")
exit()