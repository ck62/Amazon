from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import json
from datetime import datetime


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
driver = webdriver.Chrome(options=chrome_options, executable_path=r'./chromedriver.exe')

with open("ASIN-JSON.txt") as c:
    print("Reading Codes")
    codes = c.read().splitlines()
    
print("Successfull") 
links = []
for c in codes:
    print("Generating Links")
    links.append("https://sellercentral.amazon.com/abis/ajax/reconciledDetailsV2?asin="+c)
print("Successfull") 

for i,l in enumerate(links):
    driver.get(l)
    print("\nOpening Webpage ", codes[i])
    time.sleep(7)
    ele = driver.find_element_by_tag_name("body")
    print("Found JSON")
    data = ele.text
    print("Writing to file "+codes[i]+"-JSON.txt")
    with open(codes[i]+"-JSON.txt", 'w', encoding='utf-8') as f:
        f.write(data)
    print("File Write Successfull")
    print("Converting to JSON")
    json_string = json.loads(data)
    LessKeywords = json_string["detailPageListingResponse"]["generic_keywords"]['value'].split()
    LessAll = json_string["detailPageListingResponse"]["generic_keywords"]['value']
    #date = datetime.today().strftime('%Y-%m-%d')
    date = datetime.today().strftime('%Y%m%d')
    fname = codes[i]
    print("Extracting Keys")
    with open("Keywords-JSON.csv", 'a') as f:
        f.write("\"" + fname + "\",\"" + date + "\",\""+ LessAll + "\"\n")
        for item in LessKeywords:
            row = "\"" + fname + "\",\"" + date + "\",\""+ item + "\"\n"
            f.write(row)
    print("Keys Extracted for "+fname)
    print("File Keywords-JSON.csv Updated")

    # Create bak-all JSON Files
    print("Writing to file bak-"+codes[i]+"-all.txt")
    with open("bak-"+codes[i]+"-all.txt", 'w') as f:
        json.dump(json_string, f, indent=4, sort_keys=True)
    print("File Write Successful")
    print("Done")

    
    


# chrome.exe -remote-debugging-port=9014 --user-data-dir="D:\Freelance\Amazon\Cookies"