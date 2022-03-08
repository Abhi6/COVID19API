import json
with open('/Users/abhinavmara/Desktop/Python/FirstAPI/COVID19_stats.json','r') as f:
    data_dict = json.load(f)

print(data_dict['States']['Virginia']['Counties']['Henrico County'])