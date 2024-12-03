from widget import func, pcmax
import sys



if __name__ == '__main__':
  print(len(sys.argv))
  if len(sys.argv) > 1:
    
    name = str(sys.argv[1])
  user_data = func.get_user_data()
  
  for chara in user_data["pcmax"]:
        
            if chara['name'] == name:
                sorted_pcmax = chara
                break    
  driver, wait = func.get_driver(False)
  detail_area_flug = True
  headless = True
  pcmax.re_post(sorted_pcmax, driver, wait, detail_area_flug)