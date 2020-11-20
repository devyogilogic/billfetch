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
@app.route('/api/fetchbill/', methods=[ 'POST'])
def fetchbill():
    details={}
    driver=0
    Stateslement=0
    drp=0
    actions=0
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2,  
                                'plugins': 2, 'popups': 2, 'geolocation': 2, 
                                'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                                'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                                'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                                'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                                'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                                'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                                'durable_storage': 2}}

    chrome_optionss = Options()
    chrome_optionss.add_argument("--disable-extensions")
    chrome_optionss.add_argument("--headless")
    chrome_optionss.add_argument("--disable-gpu")
    chrome_optionss._binary_location=os.environ.get("GOOGLE_CHROME_BIN")
    chrome_optionss.add_argument("disable-infobars")
    chrome_optionss.add_argument("--no-sandbox")
    chrome_optionss.add_argument("--disable-dev-sh-usage")
    
    chrome_optionss.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",chrome_options=chrome_optionss)
    driver.get('https://www.amazon.in/hfc/bill/electricity?ref_=apay_deskhome_Electricity')
                    
    try :
            
            actions = ActionChains(driver)       
            driver.implicitly_wait(10)
            
            Stateslement = driver.find_element_by_id("ELECTRICITY")
            drp = Select(Stateslement)
            
                    
            actions.double_click(drp.select_by_visible_text(request.form['state'])).perform()
            mainstr = "ELECTRICITY>hfc-states-" + request.form['state'].lower()
            
            options = driver.find_element_by_id(mainstr)
            z = Select(options)
            actions.double_click(z.select_by_visible_text(request.form['boardname'])).perform()
            data = driver.find_element_by_xpath("//*[@id='hfcBillPaymentAuthForm']/div[3]/div[1]/div[1]/label").text
            driver.find_element_by_xpath("//*[@id='" + data + "']").send_keys(request.form['number'])
            driver.find_element_by_id("fetchBillActionId-announce").click()
            customerelement=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='fetch-bill-table']/tbody/tr[2]/td[2]")))
            element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='paymentBtnId-announce']")))
            element_amount=WebDriverWait(driver,5).until(

                EC.element_to_be_clickable((By.ID,"paymentBtnAmountText"))
            )
            customer_name=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/form/div[5]/div/div/table/tbody/tr[2]/td[2]").text
            due_date=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/form/div[5]/div/div/table/tbody/tr[3]/td[2]").text
            bill_amount=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/form/div[5]/div/div/table/tbody/tr[4]/td[2]").text
            details['Success']=True
            details['Customer Name']=customer_name
            details['Due Date']=due_date
            details['Amount']=bill_amount
            details['Message']="Bill Found"
            driver.find_element_by_xpath("//*[@id='" + data + "']").clear()
            driver.close()
            return jsonify(details)
            
    except Exception:
        print("IN EXCEPT BLOCK")
        try :
            message=driver.find_element_by_xpath("/html/body/div[7]/div/div/div/div")
            print(message.text)
            driver.find_element_by_xpath("//*[@id='" + data + "']").clear()
        
            
            details['Success']=False
            details['Customer Name']=None
            details['Due Date']=None
            details['Amount']=None
            details['Message']=message.text
            driver.close()
            return jsonify(details)
        except :
            details['Success']=False
            details['Customer Name']=None
            details['Due Date']=None
            details['Amount']=None
            details['Message']="Something Went Wrong Please Try After Sometime"
            driver.close()
            return jsonify(details)


if __name__ == '__main__':
  app.run()