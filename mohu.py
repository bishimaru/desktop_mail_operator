from widget import func
import signal
import sys
import time 

def signal_handler(signum, frame):
    print("SIGINT")
    sys.exit()

if __name__ == '__main__':
  
  headless = False
  driver, wait = func.get_driver(headless)
  driver.get("https://crocro.com/tools/item/view_browser_inf/?/item/view_browser_inf")
  time.sleep(10)


