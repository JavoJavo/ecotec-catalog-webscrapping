from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def ID_wait_and_capture_text(ID, stove):
    try:
        if type(ID) == list:
            #print('RED FLAG!')
            for ID_ in ID:
                wait = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, ID_)))
                element = driver.find_element(By.ID, ID_).text
                if element != '':
                    stove.append(element)
                    return 0
            stove.append('NAN')
        else:
            wait = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, ID)))
            element = driver.find_element(By.ID, ID).text
            stove.append(element)
    except:
        stove.append('FAILED TO CAPTURE')
        print('FAILED TO CAPTURE {}'.format(ID))


        
header_data = ['stove_details_name','details_manu','details_web','stove_desc']
iwa_tiers = ['details_tiers_eff_num','details_tiers_safe_num','details_tiers_co_num','details_tiers_pm_num','details_tiers_dur_num','details_tiers_iwa_ie_num']
cust_info = ['stove_life','pot_rec','pot_cap','stove_feed','stove_food_common']
general_info = ['stove_price','stove_dimensions','stove_weight','stove_dimensions','stove_assembly_materials']
iso_performance_metrics = ['iso_co_val', 'iso_co_sd', 'iso_co_num', 'iso_co_date', 'iso_co_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iso_pm_val', 'iso_pm_sd', 'iso_pm_num', 'iso_pm_date', 'iso_pm_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iso_eff_char_val', 'iso_eff_char_sd', 'iso_eff_char_num', 'iso_eff_char_date', 'iso_eff_char_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iso_eff_val', 'iso_eff_sd', 'iso_eff_num', 'iso_eff_date', 'iso_eff_fuel',
                           'iso_safe_val', 'iso_safe_sd', 'iso_safe_num', 'iso_safe_date', 'iso_safe_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iso_dur_val', 'iso_dur_sd', 'iso_dur_num', 'iso_dur_date', 'iso_dur_fuel']
iwa_performance_metrics = ['iwa_co_val', 'iwa_co_sd', 'iwa_co_num', 'iwa_co_date', 'hp_co_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iwa_pm_val', 'iwa_pm_sd', 'iwa_pm_num', 'iwa_pm_date', 'hp_pm_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iwa_co_low_val', 'iwa_co_low_sd', 'iwa_co_low_num', 'iwa_co_low_date', 'lp_co_fuel', # !! MISSING DATA SOURCE HERE !!
                           'iwa_pm_low_val', 'iwa_pm_low_sd', 'iwa_pm_low_num', 'iwa_pm_low_date', 'lp_pm_fuel'] # !! MISSING DATA SOURCE HERE !!
iwa_efficiency_metrics = ['iwa_eff_val', 'iwa_eff_sd', 'iwa_eff_num', 'iwa_eff_date', 'hp_eff_fuel', # !! MISSING DATA SOURCE HERE !!
                          'iwa_eff_val', 'iwa_eff_sd', 'iwa_eff_num', 'iwa_eff_date', 'hp_eff_fuel'] # !! MISSING DATA SOURCE HERE !!

header = header_data + iwa_tiers + cust_info + general_info + iso_performance_metrics + iwa_performance_metrics + iwa_efficiency_metrics




def check_for_commas(stove):
    checked_stove = []
    for e in stove:
        if e.find(',') != -1:
            checked_stove.append('\"'+e+'\"')
        else:
            checked_stove.append(e)
    return checked_stove

        
    
# Opening webpage
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')
driver = webdriver.Chrome(options=options)
#driver.implicitly_wait(15)
driver.get("http://catalog.cleancookstoves.org/")
assert "Clean" in driver.title
#elem = driver.find_element(By.CLASS_NAME, "col-md-4")
#.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'col-md-4')))

# Getting number of pages
wait = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pg_max")))
while True:
    try:
        pages = int(driver.find_element(By.ID, "pg_max").text)
        break
    except:
        sleep(3)
    
# Getting stoves per page
#list_of_stoves = []
with open("stoves.csv", "w") as file:
    file.write(','.join(header)+'\n')

    # Iterating pages
    for p in range(pages):
        wait = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "col-md-4")))
        elements = driver.find_elements(By.CLASS_NAME, "col-md-4")

        # Iterating elements per page
        for i,el in enumerate(elements):
            stove = []
            #if i==1:
                #sleep(5)

            # Clicking on stoves
            for iii in range(5):
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(el))
                except:
                    sleep(3)
            try:
                el.click()
            except:
                driver.execute_script("window.scrollTo(0, Y)")
                el.click()
            #sleep(.3)
            sleep(1.3)
 

            # Changing to stove tab
            try:
                parent_tab = driver.window_handles[0]
                ##obtain browser tab window
                ##if i == 5:
                    ##sleep(10)
                child_tab = driver.window_handles[1]
                #switch to tab browser
                driver.switch_to.window(child_tab)
            except:
                continue
            
            # Data capture
            try:
                # Clicking on additional details button
                wait = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "show_result_details")))
                result_details = driver.find_element(By.ID, "show_result_details")
                result_details.click()

                # Capturing header data
                header_data = ['stove_details_name','details_manu','details_web','stove_desc']
                ID_wait_and_capture_text('stove_details_name', stove)
                print('Capturing {} header data...'.format(stove[-1]))
                ID_wait_and_capture_text('details_manu', stove)
                ID_wait_and_capture_text('details_web', stove)
                ID_wait_and_capture_text('stove_desc', stove)
                #print('Header data captured')
                #print(len(stove))

                # Capturing IWA tiers (any of them may not be present) (could have different ID but be the same)
                iwa_tiers = [['details_tiers_eff_num','details_tiers_iwa_eff_num'],['details_tiers_safe_num','details_tiers_iwa_safe_num'],
                             'details_tiers_co_num','details_tiers_pm_num','details_tiers_dur_num','details_tiers_iwa_ie_num']
                for tiers in iwa_tiers:
                    ID_wait_and_capture_text(tiers, stove)
                #print('IWA data captured')
                #print(len(stove))


                # Capturing additional details from additional details button
                #print('Capturing additinal details data...')
                # Information for customers
                cust_info = ['stove_life','pot_rec','pot_cap','stove_feed','stove_food_common']
                for info in cust_info:
                    ID_wait_and_capture_text(info, stove)
                #print('Information for customers captured')
                #print(len(stove))
                # General info
                general_info = ['stove_price','stove_dimensions','stove_weight','stove_dimensions','stove_assembly_materials']
                for info in general_info:
                    ID_wait_and_capture_text(info, stove)
                #print('General info captured')
                #print(len(stove))

                # ISO performance metrics
                iso_performance_metrics = ['iso_co_val', 'iso_co_sd', 'iso_co_num', 'iso_co_date', 'iso_co_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iso_pm_val', 'iso_pm_sd', 'iso_pm_num', 'iso_pm_date', 'iso_pm_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iso_eff_char_val', 'iso_eff_char_sd', 'iso_eff_char_num', 'iso_eff_char_date', 'iso_eff_char_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iso_eff_val', 'iso_eff_sd', 'iso_eff_num', 'iso_eff_date', 'iso_eff_fuel',
                                           'iso_safe_val', 'iso_safe_sd', 'iso_safe_num', 'iso_safe_date', 'iso_safe_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iso_dur_val', 'iso_dur_sd', 'iso_dur_num', 'iso_dur_date', 'iso_dur_fuel'] # !! MISSING DATA SOURCE HERE !!
                for metric in iso_performance_metrics:
                    ID_wait_and_capture_text(metric, stove)
                #print('ISO performance metrics captured')
                #print(len(stove))

                # IWA emissions
                iwa_performance_metrics = ['iwa_co_val', 'iwa_co_sd', 'iwa_co_num', 'iwa_co_date', 'hp_co_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iwa_pm_val', 'iwa_pm_sd', 'iwa_pm_num', 'iwa_pm_date', 'hp_pm_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iwa_co_low_val', 'iwa_co_low_sd', 'iwa_co_low_num', 'iwa_co_low_date', 'lp_co_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iwa_pm_low_val', 'iwa_pm_low_sd', 'iwa_pm_low_num', 'iwa_pm_low_date', 'lp_pm_fuel'] # !! MISSING DATA SOURCE HERE !!
                for metric in iwa_performance_metrics:
                    ID_wait_and_capture_text(metric, stove)
                #print(len(stove))

                 # IWA efficiency
                iwa_efficiency_metrics = ['iwa_eff_val', 'iwa_eff_sd', 'iwa_eff_num', 'iwa_eff_date', 'hp_eff_fuel', # !! MISSING DATA SOURCE HERE !!
                                           'iwa_eff_val', 'iwa_eff_sd', 'iwa_eff_num', 'iwa_eff_date', 'hp_eff_fuel'] # !! MISSING DATA SOURCE HERE !!
                for metric in iwa_efficiency_metrics:
                    ID_wait_and_capture_text(metric, stove)
                #print(len(stove))


                #list_of_stoves.append(stove)
                stove = check_for_commas(stove)
                file.write(','.join(stove)+'\n')

                
            except:
                None
            
            # Closing and returning to parent tab
            #close browser tab window
            driver.close()
            #switch to parent window
            driver.switch_to.window(parent_tab)

        wait = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "next_btn")))
        next_btn = driver.find_element(By.ID, "next_btn")#next-btn")
        next_btn.click()


    driver.close()
#print(element)
#print(len(elements))

    
