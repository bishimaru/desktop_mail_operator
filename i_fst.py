from widget import func, ikukuru
import time

def ikukuru_fst(user_data, headless):
  for i in user_data:
    driver, wait = func.get_driver(headless)
    ikukuru.login(driver, wait, i["login_mailaddress"], i["password"])
    ikukuru.set_search_filter(driver, wait)
    ikukuru.send_fst_message(driver, wait, i["fst_message"], 15)
    driver.quit()
    time.sleep(2)

if __name__ == '__main__':
  user_data = func.get_user_data()
  headless = False
  ikukuru_fst(user_data["ikukuru"], headless)