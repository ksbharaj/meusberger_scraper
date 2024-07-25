import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import time


#  Function that helps get to navigate from the home screen to the desired parts page
def clicks_to_parts_from_home_screen(driver, part_fam_list, sequence_key):
    first_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".katbutton1[title='Katalog für Formenbau anzeigen']")))
    first_button.click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, part_fam_list[0])))

    second_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, part_fam_list[0])))
    second_button.click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, part_fam_list[1])))

    third_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, part_fam_list[1])))
    third_button.click()
    time.sleep(0.5)

    ## Additional clicks for other parts
    if sequence_key in ["FB/P Plates", "FW Parts"]:
        reload_links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.js-reload")))
        spec_button_ = reload_links[1].get_attribute('href').split('/')[-1]
        specific_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a.js-reload[href='{spec_button_}']")))
        specific_button.click()
    elif sequence_key == "E Parts":
        first_row = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-table.table-menu.table.frame table tbody tr")))
        first_row.click()
    time.sleep(0.5)

def main(sequence_key):
    options = webdriver.ChromeOptions()

    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)
    
    driver.get("https://ecom.meusburger.com/index/index.asp")
    
    ## Decline cookies
    try:
        decline_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "econda-pp2-banner-reject-all-cookies-text")))
        decline_button.click()
        print("Decline button clicked.")
    except Exception as e:
        print(f"Error: {e}")
    
    ## Dictionary that holds the sequences of clicks for a given Part Group
    scraping_sequences = {
        "F/P Length": [".tab[title='Formaufbauten längs']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                       ".js-symmnu.symmnu.symmnu_fp.frame", "table tbody tr", "title", "F"],
        "F/P Cross": [".tab[title='Formaufbauten quer']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                      ".js-symmnu.symmnu.symmnu_fp.frame", "table tbody tr", "title", "F"],
        "FB/P Blocks": [".tab[title='Backenformen']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                        ".js-symmnu.symmnu.frame", "table tbody tr", "alt", "F"],
        "FB/P Plates": [".tab[title='Backenformen']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                        ".js-symmnu.symmnu.frame", "table tbody tr", "alt", "F"],
        "FW Plates": [".tab[title='Wechselformen']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                      ".js-symmnu.symmnu.symmnu_fw.frame", "table tbody tr", "title", "F"],
        "FW Parts": [".tab[title='Wechselformen']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                     ".js-symmnu.symmnu.symmnu_fw.frame", "table tbody tr", "title", "F"],
        "FM Parts": [".tab[title='FM - Mikroformen']", "#button_normal.menu_button[title='Aufbau manuell zusammenstellen']",
                     ".js-symmnu.symmnu.frame", "table tbody tr", "title", "F"],
        "H Parts": [".tab[title='H 1000 Spannsystem']", "#button_normal.menu_button[title='H 1000 Zubehör']",
                    ".js-eteile.eteile.frame", "table tbody tr", "src", "/h"],
        "E Parts": [".tab[title='E - Einbauteile']", "[title='Alle *']",
                    ".js-eteile.eteile.frame", "table tbody tr", "src", "/"],
    }
    
    scrape_dict = scraping_sequences.get(sequence_key)
    if not scrape_dict:
        print(f"Invalid sequence key: {sequence_key}")
        driver.quit()
        return

    try:
        ### Get to the desired parts screen
        clicks_to_parts_from_home_screen(driver, scrape_dict, sequence_key)
        
        ### Get the part sub-groups (rows) to scrape from
        symmnu_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, scrape_dict[2])))
        rows = symmnu_div.find_elements(By.CSS_SELECTOR, scrape_dict[3])
        total_rows = len(rows)
        
        ### Start scraping through each sub-group/row and its constituent parts
        for index in tqdm(range(total_rows), desc="Scraping rows"):
            #### Additional clicks necessary for certain part sub-groups
            if sequence_key in ["FB/P Plates", "FW Parts"]:
                reload_links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.js-reload")))
                spec_button_ = reload_links[1].get_attribute('href').split('/')[-1]
                specific_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a.js-reload[href='{spec_button_}']")))
                specific_button.click()

            #### These are some edge cases i.e. where the part has no CAD file, or the "Weiter" button is non-existent.
            #### They are too infrequent to write code for, and are not worth scraping- so best to bypass them altogether.
            if sequence_key == "E Parts":
                if index == 303 or index == 501 or index == 805 or index == 808 or index == 885:
                    continue  
            
            #### Wait for the loading to end before progressing with clicks any further
            WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".js-spinner.loading_con")))

            #### Extract row (part group) information again
            symmnu_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, scrape_dict[2])))
            row = symmnu_div.find_elements(By.CSS_SELECTOR, scrape_dict[3])[index]

            #### Obtain the link from the row and part group name from the image file on its icon
            link = row.find_element(By.TAG_NAME, "td")
            link_1 = link.find_element(By.TAG_NAME, "a")
            icon_lister = link_1.find_element(By.TAG_NAME, "img").get_attribute(scrape_dict[4])
            
            #### If the name includes characters we are looking for, proceed with scraping!
            if scrape_dict[5] in icon_lister:
                ##### Click the element
                link_1.click()
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".js-spinner.loading_con")))

                ##### We get all the part links from the associated part table
                table_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".js-table.table.frame")))
                table_links = table_div.find_elements(By.CSS_SELECTOR, "table tbody tr td")

                ##### Iterate through all the links
                for table_link in table_links:
                    ###### If the part links can be added to the cart, it is likely to have a CAD file assocaited with it, if not, 
                    ###### then it certainly does not. 
                    try:
                        add_2_cart = table_link.find_element(By.TAG_NAME, "a")
                        add_2_cart.click()

                        ####### A pop-up appears if you pick parts from the same sub-group. This is just accepted and we carry on
                        WebDriverWait(driver, 1.25).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".js-spinner.loading_con")))
                    except Exception as e:
                        pass
                        
                ##### Select all the parts in the list that have CAD files with them
                CAD_selecto_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".orderlist_button[title='Alle Artikel der Liste markieren']")))
                CAD_selecto_button.click()
                time.sleep(0.5)

                ##### Click on the button that helps export these CAD files. This pops-up a new window           
                CAD_exporter1_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button[onclick='liste_redirect(5);']")))
                CAD_exporter1_button.click()
                time.sleep(3.5)
                
                ##### If a new window pops-up, there must be a CAD file to scrape! So we switch to the new window 
                main_window_handle = driver.current_window_handle
                all_window_handles = driver.window_handles
                ##### There's a chance that none of the parts in the cart have CAD files. To ensure this doesn't hinder us, 
                ##### we use a if-else clause
                if len(all_window_handles) > 1:
                    for handle in all_window_handles:
                        if handle != main_window_handle:
                            new_window_handle = handle
                            driver.switch_to.window(new_window_handle)
                            driver.set_window_size(1920, 1080)
                    
                    ###### We give the window some time to load, and then maximize that window so that all buttons are clickable 
                    time.sleep(3.5)
                    driver.set_window_size(1920, 1080)

                    ###### Some parts allow for furhter customization before they can be scraped. We can just accept the default settings
                    while True:
                        # Check if the "Weiter" button is present
                        print("Checking for 'Weiter' button")
                        buttons = driver.find_elements(By.XPATH, "//input[@id='okbut' and @value='Weiter']")
                        if not buttons:
                            # Exit the loop if the button is not present
                            break
                        else:
                            # Click the button if it is present
                            weiter_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//input[@id='okbut' and @value='Weiter']"))
                            )
                            print("Clicking on 'Weiter' button")
                            weiter_button.click()
                            time.sleep(5)
                            driver.set_window_size(1920, 1080)
                    
                    ###### We only need to set "STEP" as the download file format in the first instance. Subsequently, it gets selected 
                    ###### automatically. 
                    if index == 0:
                        dropdown_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "outputformat_3d-button")))
                        dropdown_button.click()
                    
                        third_option = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-id-12")))
                        third_option.click()

                    ###### We wait a bit for all to load, and then progress with clicking the download button
                    time.sleep(5)
                    download_button = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "btCadDownload3D")))
                    download_button.click()

                    ###### We then wait for another CAD download pop-up, and then click on the link to initiate the download!
                    download_dialog = WebDriverWait(driver, 120).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "Popup_CADDownload"))
                    )
                    download_link = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.FileLink.icon-click2cad_download_export")))
                    download_link.click()

                    print("All buttons clicked successfully.")
                    print("Downloading....")
                    
                    driver.close()
                else:
                    print("No new window created, continuing with next steps.")

                ##### Once the download's done, we switch to the main window, delete the cookies and refresh so that the cart empties.
                driver.switch_to.window(main_window_handle)
                driver.delete_all_cookies()
                driver.refresh()

                
    except Exception as e:
        print(f"Error: {e}")

    ## (Hopefully) all downloads are completed successfully, and we can end the script in a minute.
    print("All downloads completed. Script will terminate in 60 seconds...")
    time.sleep(60)
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Meusburger website.")
    parser.add_argument("sequence_key", type=str, help="One of the 9 keys in scraping_sequences.")
    args = parser.parse_args()

    main(args.sequence_key)
