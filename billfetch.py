from selenium.webdriver.common.by import By
from  selenium import webdriver
import  time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException

from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.chrome.options import Options

from flask import Flask,request,jsonify
import os 

app = Flask(__name__)
@app.route('/')
def hello_world():
  return 'Hello from Flask!'

#/usr/bin/chromedriver



chrome_optionss = Options()
chrome_optionss.add_argument("--disable-extensions")
chrome_optionss.add_argument("--headless")
chrome_optionss.add_argument("--disable-gpu")
chrome_optionss.add_argument("disable-infobars")
#chrome_optionss.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",chrome_options=chrome_optionss)


#driver.get()
@app.route("/api/waterbill",methods=['POST'])
def waterbill():
    
    waterbill={}  
    driver.get("https://rajasthan.gov.in/SPRAY/PHED.aspx")
    actions = ActionChains(driver)       
    driver.implicitly_wait(10)
    select_phed=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[2]/div/select")
    opt=Select(select_phed)
    actions.double_click(opt.select_by_index(1)).perform()
    driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[2]/table/tbody/tr[3]/td[2]/input").send_keys("7665196615")
    driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[2]/table/tbody/tr[4]/td[2]/input").send_keys("admin@ikedapl.com")
               
    driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[2]/input").send_keys(request.form['knumber'])
    driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[2]/div/input[1]").click()
    customer_name = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[1]/div[2]")))
    driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[2]/input").clear()
    customer_name=customer_name.text
    accountnum=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[4]/div[2]").text
    phed=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[3]/div[2]").text
    billmonth=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[5]/div[2]").text
    billamount=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[7]/div[2]").text
    consumer_address=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[7]/div[2]").text
    
    billyear=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[6]/div[2]").text
    billduedate=driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div/div/div/div/div[3]/table/tbody/tr[2]/td/div/div[2]/div/div[2]/div[2]/div[8]/div[2]").text
    waterbill['Customer Name']=customer_name
    waterbill['PHED']=phed
    waterbill['Bill Month']=billmonth
    waterbill['Bill Amount']=billamount
    waterbill['Account Number']=accountnum
    waterbill['Bill Year']=billyear
    waterbill['Bill Due Date']=billduedate
   
    return jsonify(waterbill)
    waterbill.clear()
    driver.close()
  driver.get("https://rajasthan.gov.in/SPRAY/PHED.aspx")	
    

if __name__ == '__main__':
  app.run(threaded=True)
