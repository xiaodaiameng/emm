import os
import re

folder_path = "C:/Users/ass/Desktop/temp"
nameList = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if re.search(r'\.mp3$', file, re.IGNORECASE):
            name = f"/music/{file}"
            nameList.append(name)

for i in nameList:
    print(f"'{i}',")