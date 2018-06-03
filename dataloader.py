import json

with open('secret/data.json') as f:
    data = json.load(f)
    discordData = data['discord']
    redditData = data['reddit']
