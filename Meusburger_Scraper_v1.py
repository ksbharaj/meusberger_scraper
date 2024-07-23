import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def main(sequence_key):
    options = webdriver.ChromeOptions()

    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)
    
    driver.get("https://ecom.meusburger.com/index/index.asp")
    
    try:
        decline_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "econda-pp2-banner-reject-all-cookies-text")))
        decline_button.click()
        print("Decline button clicked.")
    except Exception as e:
        print(f"Error: {e}")
        
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
        first_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".katbutton1[title='Katalog für Formenbau anzeigen']")))
        first_button.click()
        time.sleep(2)
        
        second_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, scrape_dict[0])))
        second_button.click()
        time.sleep(2)
        
        third_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, scrape_dict[1])))
        third_button.click()
        time.sleep(2)
        
        if sequence_key in ["FB/P Plates", "FW Parts"]:
            reload_links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.js-reload")))
            spec_button_ = reload_links[1].get_attribute('href').split('/')[-1]
            specific_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a.js-reload[href='{spec_button_}']")))
            specific_button.click()
        elif sequence_key == "E Parts":
            first_row = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-table.table-menu.table.frame table tbody tr")))
            first_row.click()
        time.sleep(2)
        
        symmnu_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, scrape_dict[2])))
        rows = symmnu_div.find_elements(By.CSS_SELECTOR, scrape_dict[3])
        total_rows = len(rows)
        
        for index in range(total_rows):
            if sequence_key == "E Parts":
                symmnu_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, scrape_dict[2])))
            row = symmnu_div.find_elements(By.CSS_SELECTOR, scrape_dict[3])[index]

            link = row.find_element(By.TAG_NAME, "td")
            link_1 = link.find_element(By.TAG_NAME, "a")
            icon_lister = link_1.find_element(By.TAG_NAME, "img").get_attribute(scrape_dict[4])
            ## If the part type contains the desired string, we scrape!
            if scrape_dict[5] in icon_lister:
                # Click the element
                link_1.click()
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".js-spinner.loading_con")))

                table_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".js-table.table.frame")))
                table_links = table_div.find_elements(By.CSS_SELECTOR, "table tbody tr td")

                for table_link in table_links:
                    try:
                        add_2_cart = table_link.find_element(By.TAG_NAME, "a")
                        add_2_cart.click()

                        # Handle the pop-up alert
                        WebDriverWait(driver, 5).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".js-spinner.loading_con")))
                    except Exception as e:
                        pass

        CAD_selecto_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".orderlist_button[title='Alle Artikel der Liste markieren']")))
        CAD_selecto_button.click()
        time.sleep(20)
        
        CAD_exporter1_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button[onclick='liste_redirect(5);']")))
        CAD_exporter1_button.click()
        time.sleep(40)
        
        main_window_handle = driver.current_window_handle
        all_window_handles = driver.window_handles

        for handle in all_window_handles:
            if handle != main_window_handle:
                new_window_handle = handle
                driver.switch_to.window(new_window_handle)

        time.sleep(20)
        
        dropdown_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "outputformat_3d-button")))
        dropdown_button.click()

        time.sleep(20)

        third_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-id-12")))
        third_option.click()

        time.sleep(20)

        download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btCadDownload3D")))
        download_button.click()

        time.sleep(20)

        download_dialog = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "Popup_CADDownload"))
        )

        time.sleep(10)

        download_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.FileLink.icon-click2cad_download_export")))
        download_link.click()

        print("All buttons clicked successfully.")
        print("Downloading....")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(60)
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Meusburger website.")
    parser.add_argument("sequence_key", type=str, help="One of the 9 keys in scraping_sequences.")
    args = parser.parse_args()

    main(args.sequence_key)
