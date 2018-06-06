import json

with open('secret/data.json') as f:
    data = json.load(f)
    discord_data = data['discord']
    reddit_data = data['reddit']
