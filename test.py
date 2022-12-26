import requests

BASE = "http://127.0.0.1:5000/"


"""data = [{"likes": 10, "name": "How To", "views": 100},
        {"likes": 11, "name": "How Not To", "views": 101},
        {"likes": 12, "name": "Whatever", "views": 102}]

for i in range(len(data)):
    response = requests.put(BASE+"video/"+str(i), data[i])
    print(response.json())

input()
"""
response = requests.get(BASE+"video/2")
print(response.json())

input()

response = requests.patch(BASE+"video/2", {"likes":9})
print(response.json())