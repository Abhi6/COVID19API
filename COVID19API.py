from fastapi import FastAPI
import requests
import json


with open('/Users/abhinavmara/Desktop/Python/FirstAPI/COVID19_stats.json') as file:
    data = json.load(file)

app = FastAPI()

@app.get('/')
def home():
    return {'Page':'Home'}

@app.get('/USA')
def usa():
    return {'USA':data['USA']}

@app.get('/USA/cases')
def usa_cases():
    return {'USA':{'Cases':data['USA']['Cases']}}

@app.get('/USA/cases/{aspect}')
def usa_cases_stat(aspect):
    for dict_aspect in data['USA']['Cases']:
        if dict_aspect.lower() == aspect.lower():
            return {
                'USA': {
                    'Cases':data['USA']['Cases'][dict_aspect]
                }
            }

@app.get('/USA/deaths')
def usa_deaths():
    return {'USA':{'Deaths':data['USA']['Deaths']}}

@app.get('/USA/deaths/{aspect}')
def usa_deaths_stat(aspect):
    for dict_aspect in data['USA']['Deaths']:
        if dict_aspect.lower() == aspect.lower():
            return {
                'USA': {
                    'Deaths':data['USA']['Deaths'][dict_aspect]
                }
            }



@app.get('/{state_name}')
def state(state_name):
    for state in data['States']:
        if state.lower() == state_name.lower():
            new_dict = {
                state: {
                    '7-day average cases':data['States'][state]['7-day average cases'],
                    '7-day average deaths':data['States'][state]['7-day average deaths'],
                    'Total cases':data['States'][state]['Total cases'],
                    'Total deaths':data['States'][state]['Total deaths'],
                    '7-day average hospitalizations':data['States'][state]['7-day average hospitalizations'],
                    '7-day average hospitalizations per 100k':data['States'][state]['7-day average hospitalizations per 100k'],
                    'Counties':data['States'][state]['Counties']
                }
            }
            return new_dict

@app.get('/{state_name}/{aspect}')
def state_stat(state_name, aspect):
    for state in data['States']:
        if state.lower() == state_name.lower():
            for dict_aspect in data['States'][state]:
                if dict_aspect.lower() == aspect.lower():
                    return {
                        state: {
                            dict_aspect: data['States'][state][dict_aspect]
                            }
                    }

@app.get('/{state_name}/by_county/{county_name}')
def county(state_name, county_name):
    for state in data['States']:
        if state.lower() == state_name.lower():
            for county in data['States'][state]['Counties']:
                if county_name.lower() in county.lower():
                    return {
                        state: {
                            county: data['States'][state]['Counties'][county]
                        }
                    }

@app.get('/{state_name}/by_county/{county_name}/{aspect}')
def county_stat(state_name, county_name, aspect):
    for state in data['States']:
        if state.lower() == state_name.lower():
            for county in data['States'][state]['Counties']:
                if county_name.lower() in county.lower():
                    for stat in data['States'][state]['Counties'][county]:
                        if aspect.lower() == stat.lower():
                            return {
                                state: {
                                    county: {
                                        stat:data['States'][state]['Counties'][county][stat]
                                    }
                                }
                            }