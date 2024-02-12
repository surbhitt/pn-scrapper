from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


clean_up = (
    lambda string: string.replace("GST Certificate", "")
    .replace("PAN File", "")
    .replace("Address Proof", "")
    .replace("-NA-", "")
    .strip()
)

driver = webdriver.Chrome()
driver.get("https://hprera.nic.in/PublicDashboard")

# ensure the page is correct
assert "HPRERA" in driver.title

modal_links = []

try:
    # data is fetched from the server 
    # takes 30-50 sec on avg
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "reg-Projects"))
    )
    modal_links = driver.find_elements(By.XPATH, '//a[@title="View Application"]')[:5]
except:
    # TODO: determine the type of err
    print("[ERR] Failed while waiting for data fetch")
    driver.close()
    exit(1)

data = []
req_fields = ("GSTIN No.", "PAN No.", "Name", "Permanent Address")

for link in modal_links:
    link.click()
    req_field_val_map = {}
    try:
        # data is fetched to populate table, values we want 
        # takes < 10 sec on average
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@id="project-menu-html"]/div/div/div/table')
            )
        )
        
        # collect all the rows to further examine for required fields 
        rows = driver.find_elements(By.XPATH, "//tr")

        for row in rows:
            # first td is the identifier e.g. Name
            identifier = row.find_element(By.XPATH, "./td[1]")
            if identifier.text in req_fields:
                # second is the value e.g. Maninder Singh
                value = row.find_element(By.XPATH, "./td[2]")
                req_field_val_map[identifier.text] = clean_up(value.text)
    except Exception as ex:
        print("[ERR] Failed while storing data")
        driver.close()
        exit(1)
    data.append(req_field_val_map)
    driver.find_element(By.CLASS_NAME, "close").click()

json.dump(data, open("data.json", "w"), indent=4)
driver.close()
