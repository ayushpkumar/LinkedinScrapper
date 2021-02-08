
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 20:23:40 2021

@author: ayush
"""
# import parameters
from time import sleep
import logging,  pathlib, os
from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re, pandas
import time


global driver

data=pandas.DataFrame(columns=['Name','Email'])
names = []
emails = []
def writeCSV(data, path, logger):
    # infoLog("######## "+ data)
    # infoLog("######## ######## " + str(type(data)))
    output_file_name="LinkedinScraped.xlsx"
    output_file_name_split = output_file_name.split('.')
    output_file_name = "".join(output_file_name_split[0:-1]) + "_" + str(int(time.time())) + "." + \
                       output_file_name_split[-1]
    with pandas.ExcelWriter(path + '/Excel/' + output_file_name) as writer:
        data.to_excel(writer, sheet_name='Data')
        writer.save() 
        #infoLog(data)
    infoLog("Excel file with " + output_file_name + " Created !!", logger)
        
                      
def getElement(sel, logger):
    #infoLog(sel)
    name = sel.xpath('//h1/text()').extract_first()
    
    #email= sel.find_element_by_xpath('//*[@id="ember548"]/div/section[5]/div/a')
    # email = sel.xpath('//div/section/div/div/div/section/div/a.t-14/text()')
    email = sel.xpath('//a/text()')
    #infoLog("EMAIL" + str(email[1]))
    pattern=r'[^\s\>]+[^\s]+@+[^\s]+\.[\b(com)|(edu)|(io)|(net)\b\<]+'
    email= re.findall(pattern, str(email))
    
    #email=re.findall('[^\s\>]+[a-z]+@+[^\s]+\.[\bcom\b\<]+',str(email))
    name = name.strip("\n          ")
    infoLog(name + "|" + str(email), logger)
    
    if email == None:
        email = "Not Available"
    
    names.append(name)
    emails.append(email)




linkedin_urls=[]

def getLinkURL(i,driver,search,logger):
    #driver = webdriver.Chrome('/home/ayush/Desktop/Guardhat/scripts/chromedriver')
    driver.get('https://www.google.com')
    sleep(3)
    
    search_query = driver.find_element_by_name('q')
    # search_query.send_keys(parameters.search_query)
    search_query.send_keys(search)

    sleep(0.5)
    
    search_query.send_keys(Keys.RETURN)
    sleep(2)
    if int(i) > 1:
        i= i+1
        next_button = driver.find_element_by_xpath('//*[@id="xjs"]/div/table/tbody/tr/td['+ str(i) +']/a')
        next_button.click()     
     
    #results= driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a').get_attribute('href')
    results= driver.find_elements_by_css_selector('div.yuRUbf > a')
    #time.sleep(2)
    #results= [results.get_attribute('href') for result in results]
    #infoLog(results)
    infoLog("| ############ Reading URLS ############",logger)
    try :
       
        for elements in results:
            elements= elements.get_attribute('href')
            infoLog(elements, logger)
            #elements= elements.text
            #erid= elements.split("\n",1)
    #userid= userid.split(" > ",0)
            #infoLog(userid)

            #userid=userid[1].replace(' › ', '/in/')
            
            # infoLog(userid)
            # if userid != "www.linkedin.com/in/...":
            #     pass
            linkedin_urls.append(elements)
            
    except IndexError:
        criticalLog('Error Ocurred in Reading Url | Continuing the script', logger)
        pass
    
    
def infoLog(mssg, logger):
    #print(mssg)
    logger.info(mssg)
    
def debugLog(message):
    #print(message)
    logging.debug(message)

def criticalLog(msg, logger):
    #print(msg)
    logger.critical(msg, logger)

    
    
    
            
        

global logger        


def main():
    try:
        os.mkdir('LOG')
        os.mkdir('Excel')
    except Exception:
        pass
    
    
    
    
    path = os.path.abspath(os.getcwd())
    # infoLog(path)
    output_file_name="LOG_.log"
    output_file_name_split = output_file_name.split('.')
    output_file_name = "".join(output_file_name_split[0:-1]) + "_" + str(int(time.time())) + "." + \
                       output_file_name_split[-1]
    
    p= str(path + output_file_name)
    
    logger = logging.getLogger(__name__)
    
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(output_file_name)
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.ERROR)
    
    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    #logger.info('This is a warning')
    #logger.error('This is an error')
    
    output_file_name_1="LOGGER_Scraper_.log"
    output_file_name_split = output_file_name_1.split('.')
    output_file_name_1 = "".join(output_file_name_split[0:-1]) + "_" + str(int(time.time())) + "." + \
                       output_file_name_split[-1]
    
    logging.basicConfig(filename = output_file_name_1, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level='INFO')
    infoLog('Path for log file' + p, logger)    
    #logging.basicConfig(filename= path + '/LOG/' + output_file_name, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    #logging.warning('This will get logged to a file')
    infoLog("####  Starting the Program   ####", logger)
    infoLog("#### Linkedin Scrapping Tool ####", logger)
    infoLog("####          Ayush	   ####",  logger)
    infoLog("####  ayushpkumar@gmail.com  ####",  logger)
    infoLog("####       v-1.0.0           ####", logger)
    usrname= input('Enter Linkedin User Name  : ')
    password1= input("Enter Linkedin Password  : ")
    search= input("Enter Search Query (If Multiple Seperate by \" AND \")")
    search = 'site:linkedin.com/in/ AND \"' + search
    opVar= input("Headless Mode True / False :")
    noSearch= input('Number of Searches [Max :75] : ')
    options= Options()
    options.headless = False
    if opVar == "True":
        options.headless = True
    
    infoLog('## Linkedin Scrapper Started  ##', logger)
    
    infoLog('#Username : ' + usrname, logger)
    
    chromepath= path + '/chromedriver'
    print(chromepath)
    
    driver = webdriver.Chrome('/home/ayush/Desktop/Guardhat/scripts/chromedriver' , chrome_options=options)
    
    #options= Options()
    #options.headless = True
    # driver = webdriver.Chrome('/home/ayush/Desktop/Guardhat/scripts/chromedriver')
    
    driver.get('https://www.linkedin.com')
    infoLog('#### Attempting Linkedin Login  ####', logger)
    username = driver.find_element_by_id('session_key')
    # username.send_keys(parameters.linkedin_username)
    username.send_keys(usrname)
    sleep(0.5)
    
    password = driver.find_element_by_id('session_password')
    #password.send_keys(parameters.linkedin_password)
    password.send_keys(password1)
    sleep(0.5)
    
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    sleep(10)
    infoLog('#### Linkedin Login Succesfull  ####', logger)
    x = 0
    #linkedin_urls=["https://www.linkedin.com/in/ayushpkumar", 'https://linkedin.com/in/mikhailzhavoronkov']
    while len(linkedin_urls) < int(noSearch):
        x = x + 1
        getLinkURL(x, driver, search,logger)
        #infoLog(linkedin_urls)

        
        # For loop to iterate over each URL in the list
    try:
        for linkedin_url in linkedin_urls:
    
        # get the profile URL 
            driver.get(linkedin_url + "/detail/contact-info/")
    
        # add a 5 second pause loading each URL
            sleep(5)
    
        # assigning the source code for the webpage to variable sel
            sel = Selector(text=driver.page_source) 
            #infoLog("SOURCE" + str(sel))
            getElement(sel, logger)
    except Exception:
        criticalLog('Exception Ocurred | Handling Now ... ', logger)
        for linkedin_url in linkedin_urls:
    
        # get the profile URL 
            driver.get("https://" + linkedin_url + "/detail/contact-info/")
    
        # add a 5 second pause loading each URL
            sleep(3)
    
        # assigning the source code for the webpage to variable sel
            sel = Selector(text=driver.page_source) 
            getElement(sel, logger)
        
       
    #Selector.re(self, regex)
    # terminates the application
    #driver.quit()
    
    #driver.quit()
    
    #infoLog(names)
    #infoLog(emails)
    names1= pandas.DataFrame(names)
    email1= pandas.DataFrame(emails)
    finalUrl= pandas.DataFrame(linkedin_urls)
    data = pandas.concat([names1,email1,finalUrl], axis=1)
    infoLog(data, logger)
    #logging.basicConfig(filename = p, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    writeCSV(data, path)
        
if __name__ == "__main__":
   main()
