import json

# Prepare constants from JSON files
with open('webapp/constants/technology-used.json', 'r') as fp:
    TECH_USED = json.load(fp)

with open('webapp/constants/pages-config.json', 'r') as fp:
    PAGES_CONFIG = json.load(fp)