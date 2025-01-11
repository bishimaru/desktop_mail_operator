from widget import func, ikukuru



def ikukuru_test(user_data, headless):
  driver, wait = func.get_driver(headless)
  ikukuru.login(driver, wait, user_data[0], user_data[1])



if __name__ == '__main__':
  user_data = func.get_user_data()
  user_data = ["erikahuwhiuhs@icloud.com", "7234e"]
  headless = False
  ikukuru_test(user_data, headless)