#!/usr/bin/env python
# coding: utf-8

# ## inputs

# * need to download compatible chrome driver for selenium: https://chromedriver.chromium.org/downloads
# * also may need to permit usage in System Prefs for the first use

# In[193]:


# set driver location
chromedriver_location = "/Users/erik.bethke1/Python Projects/Sweepstakes/chromedriver"

# personal inputs
email_in = "" # string
first_name = '' # string
last_name = '' # string
address_1 = '' # string
address_city = '' # string no abbrev
address_state = '' # string
address_zip = '' # string
phone = '' # string
gender = '' # must be in M/F/O/P for: Male/Female/Other/Prefer Not to Say
dob_m = '' # must be in string format (not int)
dob_day = ''
dob_year = ''
mvpd = '' # I leave it as Netflix but can be modified to any vals in the list


# ## code

# In[143]:


# need to install selenium if not already installed
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


# In[194]:


# list of paths
xpaths = ['//*[@id="name_Firstname"]',
          '//*[@id="name_Lastname"]',
          '//*[@id="address_Address1"]',
          '//*[@id="address_City"]',
          '//*[@id="address_State"]',
          '//*[@id="address_Zip"]',
          '//*[@id="phone"]',
          '//*[@id="date_of_birth_month"]',
          '//*[@id="date_of_birth_day"]',
          '//*[@id="date_of_birth_year"]',
          '//*[@id="mvpd"]'
         ]
# values associated with those paths
xpath_vals = [first_name, last_name, address_1, address_city, address_state, address_zip, phone, dob_m, dob_day, dob_year, mvpd]


# In[198]:


driver = webdriver.Chrome(chromedriver_location)
# dictionary of webframe/iframe to iterate over
webframes = {"https://www.hgtv.com/sweepstakes/hgtv-smart-home/sweepstakes" : '//*[@id="ngxFrame171583"]',
           "https://www.diynetwork.com/hgtv-smart-home?ocid=direct": '//*[@id="ngxFrame171589"]'}
for webpage in webframes:
    # set driver
    driver.get(webpage)
    sleep(3) # sleep for page to load to avoid errors
    # email entry page
    # wait, then switch to iframe
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,webframes.get(webpage))))
    # wait, then send email_in to input
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="xReturningUserEmail"]'))).send_keys(email_in)
    # click the "begin entry" button



    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="xCheckUser"]'))).click()
    #driver.find_element_by_xpath('//*[@id="xCheckUser"]').click()
    try:

        # rest of info page
        # wait until the form reloads with the new contents
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="xSubmitContainer"]')))

        # for all non-radio/checkbox
        for xpath, val in zip(xpaths, xpath_vals):
            driver.find_element_by_xpath(xpath).send_keys(val)

        # for radio buttons
        # gender
        if gender == 'M':
            driver.find_element_by_xpath('//*[@id="gender_1"]').click()
        elif gender == 'F':
            driver.find_element_by_xpath('//*[@id="gender_0"]').click()
        elif gender == 'O':
            driver.find_element_by_xpath('//*[@id="gender_2"]').click()
        else: # safe bet for prefer not to say to catch issues
            driver.find_element_by_xpath('//*[@id="gender_3"]').click()

        # submit entry
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="xSubmitContainer"]'))).click()
        sleep(2)
    except:
        pass
