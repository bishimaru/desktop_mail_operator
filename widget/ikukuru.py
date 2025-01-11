import time
from selenium.webdriver.common.by import By
import random

def login(driver, wait, login_id, login_pass):
  
  driver.delete_all_cookies()
  # https://sp.194964.com/menu.html
  driver.get("https://sp.194964.com/menu.html")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  wait_time = random.uniform(3, 6)
  time.sleep(200)
  id_form = driver.find_element(By.ID, value="loginid")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="pwd")
  pass_form.send_keys(login_pass)
  time.sleep(1)
  send_form = driver.find_element(By.ID, value="B1login")