# This script scrapes an Indian government webite to get NGP
# status for every panchayat. 
# Written by Timothy Sweetser, @hacktuarial, October 2014
from selenium import webdriver
import pandas as pd
import string
import datetime
import time

output = '/Users/timothysweetser/Anna/scrape/'

def scrape(searchTerm, data, browser):
    starturl = 'http://tsc.gov.in/tsc/Report/PanchayatReport/RptFindGPStatus.aspx'
    searchbox = 'ctl00_ContentPlaceHolder1_txtSearchName'
    searchsubmit = 'ctl00_ContentPlaceHolder1_btnSubmit'
    results = 'ctl00_ContentPlaceHolder1_lnkbtnGpsCount'
    
    browser.get(starturl)
    browser.find_element_by_id(searchbox).send_keys(searchTerm)
    browser.find_element_by_id(searchsubmit).click()
    wait = 0
    waitMax = 2
    while(wait < waitMax):
        try:
            link = browser.find_element_by_id(results)
            link.click()

            wait = waitMax
        except:
            time.sleep(5)
            wait += 1
    wait = 0
    while(wait < waitMax):
        try:
            tbl = browser.find_element_by_id('ctl00_ContentPlaceHolder1_div_Data')
            wait = waitMax
        except:
            time.sleep(5)
            wait += 1

    allRows = tbl.find_elements_by_tag_name('tr')        
    rows_list = []
    rowIndex = 0
    for row in allRows:
        cells = row.find_elements_by_tag_name('td')
        dict1 = {}
        myList = []
        for cell in cells:
            myList.append(cell.text)
        if len(myList) >= 5:
            panchayat = str(myList[4])
            panchayat = panchayat[panchayat.find('>') + 1 : \
            panchayat.find('</a>')].strip()     
            dict1['SL'] = str(myList[0].strip())
            dict1['State'] = str(myList[1].strip())
            dict1['District'] = str(myList[2].strip())
            dict1['Block'] = str(myList[3].strip())
            dict1['Panchayat'] = panchayat
            dict1['NGP_Status'] = str(myList[5].strip())
        try:
            dict1['SL'] = int(dict1['SL'])
            rows_list.append(dict1)
            rowIndex += 1
        except:
            print 'Removed a row'  
        if rowIndex % 10 == 1:
            print rowIndex 
            print datetime.datetime.now()
    data = pd.DataFrame(rows_list)      
    data.to_csv(output + searchTerm + '.csv', index=False)
            
    
def isVowel(ch):
    return ch in ('a', 'e', 'h', 'i', 'o', 'u')

for ltr1 in string.lowercase:
    for ltr2 in string.lowercase:
        if (not (isVowel(ltr1) or isVowel(ltr2))): # both consonants
            searchTerm = ltr1 + ltr2
            data = pd.DataFrame(columns=('SL', 'State', 'District', 'Block', \
            'Panchayat', 'NGP_Status'))
            browser = webdriver.Firefox()
            scrape(searchTerm, data, browser)
            browser.close()
        else:
            for ltr3 in string.lowercase:
                searchTerm = ltr1 + ltr2 + ltr3
                data = pd.DataFrame(columns=('SL', 'State', 'District', 'Block', \
                'Panchayat', 'NGP_Status'))
                browser = webdriver.Firefox()
                try:
                    scrape(searchTerm, data, browser)
                except:
                    # no panchayats start with these letters - write empty CSV
                    data.to_csv(output + searchTerm + '.csv', index=False)
                browser.close()