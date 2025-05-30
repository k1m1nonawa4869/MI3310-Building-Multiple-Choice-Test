import json

with open("questions.json", "r",encoding="utf-8") as qs:
    qs = json.load(qs)
print(qs[0]["question"])