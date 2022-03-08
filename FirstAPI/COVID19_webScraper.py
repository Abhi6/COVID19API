# json parsing
import json

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# create driver
driver = webdriver.Firefox()
driver.maximize_window()

# establish wait time
wait = WebDriverWait(driver,20)

# get URL
driver.get('https://usafacts.org/visualizations/coronavirus-covid-19-spread-map')

# create json
data = {
    'USA' : {
        'Cases' : {

        },
        'Deaths' : {

        }
    },
    'States' : {

    }
}

# get usa statistics
USA_cases_totalReported = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[1]/td[1]'))).text
USA_cases_recentDate = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]'))).text
USA_cases_7DayAverage = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]'))).text
USA_deaths_totalReported = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[1]'))).text
USA_deaths_recentDate = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[2]'))).text
USA_deaths_7DayAverage = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[3]'))).text

# store USA statistics in data dict
data['USA']['Cases']['Total Reported'] = USA_cases_totalReported
data['USA']['Cases']['Most Recent Date'] = USA_cases_recentDate
data['USA']['Cases']['7-Day Average'] = USA_cases_7DayAverage

data['USA']['Deaths']['Total Reported'] = USA_deaths_totalReported
data['USA']['Deaths']['Most Recent Date'] = USA_deaths_recentDate
data['USA']['Deaths']['7-Day Average'] = USA_deaths_7DayAverage

# get an array of all states (plus some other states that can be ignored)
states = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'MuiTableRow-root')))

# parsing starts here
del states[0:4]             # getting rid of unnecessary data
for state in states:        # iterating through every state and storing every datapoint in json format
    state_arr = state.text.split(' ')
    parse_state_arr = []

    i = 0
    state_name = state_arr[i]
    while (i < len(state_arr)):
        if state_arr[i].isalpha() == True and state_arr[i+1].isalpha() == True:
            state_name += ' ' + state_arr[i+1]
        else:
            parse_state_arr.append(state_arr[i])
        i += 1
    parse_state_arr.insert(0, state_name)
    del parse_state_arr [1]
    data['States'][parse_state_arr[0]]  = {
        '7-day average cases':parse_state_arr[1],
        '7-day average deaths':parse_state_arr[2],
        'Total cases':parse_state_arr[3],
        'Total deaths':parse_state_arr[4],
        '7-day average hospitalizations':parse_state_arr[5],
        '7-day average hospitalizations per 100k':parse_state_arr[6],
        'Counties': {

        }
    }

count = 1
iter = True
while (iter):
    new = str(count)
    try:
        state_click = wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[3]/div[3]/div/div[1]/div[3]/div/div/table/tbody/tr[{new}]/th/a')))
    except:
        iter = False
        break
    count = int(count)
    count += 1
    name = state_click.text
    state_click.click()
    counties = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'MuiTableRow-root')))
    del counties[0:4]
    for county in counties:
        county_arr = county.text.split(' ')
        parse_county_arr = []

        i = 0
        county_name = county_arr[i]
        while (i < len(county_arr)):
            if county_arr[i].isalpha() == True and county_arr[i+1].isalpha() == True:
                county_name += ' ' + county_arr[i+1]
            else:
                parse_county_arr.append(county_arr[i])
            i += 1
        parse_county_arr.insert(0, county_name)
        del parse_county_arr [1]
        data['States'][name]['Counties'][parse_county_arr[0]] = {
            '7-day average cases':parse_county_arr[1],
            '7-day average deaths':parse_county_arr[2],
            'Cases':parse_county_arr[3],
            'Deaths':parse_county_arr[4]
            }
        

    driver.back()

# parsing ends and driver is exited
driver.quit()

json_object = json.dumps(data, indent=4)

with open('COVID19_stats.json','w') as f:
    json.dump(data,f)