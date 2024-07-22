import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def main(sequence_key):
    options = webdriver.ChromeOptions()
    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(10)
    
    # Open the target website
    driver.get("https://ecom.meusburger.com/index/index.asp")
    
    # Handle the cookie consent banner, and decline it
    try:
        decline_button = driver.find_element(By.ID, "econda-pp2-banner-reject-all-cookies-text")
        decline_button.click()
        print("Decline button clicked.")
    except Exception as e:
        print(f"Error: {e}")
        
    # Define the scraping sequences depending on parts required
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
    
    # Get the selected scraping sequence
    scrape_dict = scraping_sequences.get(sequence_key)
    if not scrape_dict:
        print(f"Invalid sequence key: {sequence_key}")
        driver.quit()
        return

    ## Clicking sequence shown in try-except clause
    try:
        # Click the first button
        first_button = driver.find_element(By.CSS_SELECTOR, ".katbutton1[title='Katalog für Formenbau anzeigen']")
        first_button.click()
        time.sleep(2)
        
        # Click the second button
        second_button = driver.find_element(By.CSS_SELECTOR, scrape_dict[0])
        second_button.click()
        time.sleep(2)
        
        # Click the third button
        third_button = driver.find_element(By.CSS_SELECTOR, scrape_dict[1])
        third_button.click()
        time.sleep(2)
        
        # Handle special cases for FB/P Plates, FW Parts and E Parts
        if sequence_key in ["FB/P Plates", "FW Parts"]:
            reload_links = driver.find_elements(By.CSS_SELECTOR, "a.js-reload")
            spec_button_ = reload_links[1].get_attribute('href').split('/')[-1]
            specific_button = driver.find_element(By.CSS_SELECTOR, f"a.js-reload[href='{spec_button_}']")
            specific_button.click()
        elif sequence_key == "E Parts":
            driver.find_elements(By.CSS_SELECTOR, ".js-table.table-menu.table.frame")[0].find_elements(By.CSS_SELECTOR, "table tbody tr")[0].click()
        time.sleep(2)
        
        # Find and iterate through rows in the symmnu div
        symmnu_div = driver.find_element(By.CSS_SELECTOR, scrape_dict[2])
        rows = symmnu_div.find_elements(By.CSS_SELECTOR, scrape_dict[3])
        total_rows = len(rows)
        
        for index in range(total_rows):
            symmnu_div = driver.find_element(By.CSS_SELECTOR, scrape_dict[2])
            row = symmnu_div.find_elements(By.CSS_SELECTOR, "table tbody tr")[index]

            link = row.find_element(By.TAG_NAME, "td")
            link_1 = link.find_element(By.TAG_NAME, "a")
            icon_lister = link_1.find_element(By.TAG_NAME, "img").get_attribute(scrape_dict[4])

            # Check to ensure the desired part names are scraped/downloaded
            if scrape_dict[5] in icon_lister:
                link_1.click()
                time.sleep(2.5)

                table_div = driver.find_element(By.CSS_SELECTOR, ".js-table.table.frame")
                table_links = table_div.find_elements(By.CSS_SELECTOR, "table tbody tr td")

                # Iterate through each downloadable cell in the part table
                for table_link in table_links:
                    try:
                        add_2_cart = table_link.find_element(By.TAG_NAME, "a")
                        add_2_cart.click()
                        time.sleep(1.0)

                        # Handle the pop-up alert
                        WebDriverWait(driver, 5).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        # print("Alert accepted")
                    except Exception as e:
                        # print(f"Exception caught: {e}")
                        pass

                # time.sleep(2)
        
        # Select all items in the list
        CAD_selecto_button = driver.find_element(By.CSS_SELECTOR, ".orderlist_button[title='Alle Artikel der Liste markieren']")
        CAD_selecto_button.click()
        time.sleep(20)
        
        # Export the CAD files
        CAD_exporter1_button = driver.find_element(By.CSS_SELECTOR, "div.button[onclick='liste_redirect(5);")
        CAD_exporter1_button.click()
        time.sleep(40)
        
        # Switch to the new window
        main_window_handle = driver.current_window_handle
        all_window_handles = driver.window_handles

        for handle in all_window_handles:
            if handle != main_window_handle:
                new_window_handle = handle
                driver.switch_to.window(new_window_handle)

        time.sleep(20)
        
        # Select the desired CAD format        
        dropdown_button = driver.find_element(By.ID, "outputformat_3d-button")
        dropdown_button.click()

        time.sleep(20)

        third_option = driver.find_element(By.CSS_SELECTOR, "#ui-id-12")
        third_option.click()

        time.sleep(10)

        dropdown_text = driver.find_element(By.CSS_SELECTOR, "#outputformat_3d-button .ui-selectmenu-text").text
        
        # Download the CAD files
        download_button = driver.find_element(By.ID, "btCadDownload3D")
        download_button.click()

        time.sleep(10)

        download_dialog = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "Popup_CADDownload"))
        )

        time.sleep(5)

        download_link = download_dialog.find_element(By.CSS_SELECTOR, "a.FileLink.icon-click2cad_download_export")
        download_link.click()

        # time.sleep(60)

        print("All buttons clicked successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Give sufficient time to download (1 minute), the quite the driver
    print("Downloading....")
    time.sleep(60)
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Meusburger website.")
    parser.add_argument("sequence_key", type=str, help="One of the 9 keys in scraping_sequences.")
    args = parser.parse_args()

    main(args.sequence_key)
