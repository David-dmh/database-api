import pickle
import requests
import json
import time

filename = input("Filename in state_data (state_data/*filename*) to upload: ")
    
with open(f"state_data/{filename}", "rb") as f:
    listings = pickle.load(f)
    
for l_data in listings:
    try:
        r = requests.post("http://localhost:5000/houses", json=l_data)
        print("Load success")
    except:
        print("Connection refused by server...")
        print("Sleeping (5 sec)...")
        time.sleep(5)
        print("Resuming...")
        r = requests.post("http://localhost:5000/houses", json=l_data)

print(f"Upload for {filename} complete.")
