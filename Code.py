import time
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def open_homepage(url):
    driver.get(url)
    driver.set_window_size(1552, 832)
    driver.set_window_position(-2, 0)
    time.sleep(1)

def navigate_to_revenue_calculator():
    try:
        revenue_calculator_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Revenue Calculator")))
        revenue_calculator_link.click()
        time.sleep(1)
    except Exception as e:
        print(f"Error navigating to Revenue Calculator: {e}")

def adjust_window(width, height):
    try:
        driver.set_window_size(width, height)
        driver.set_window_position(-2, 0)
        time.sleep(1)
    except Exception as e:
        print(f"Error adjusting window: {e}")

def scroll_to_slider():
    try:
        slider_section = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":r0:"]')))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", slider_section)
        time.sleep(1)
    except Exception as e:
        print(f"Error scrolling to slider: {e}")

def set_slider_value(value_set_to):
    try:
        slider_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//span[@class='MuiSlider-root MuiSlider-colorPrimary MuiSlider-sizeMedium css-16i48op'])[1]")))
        slider_size = slider_element.size
        slider_width = slider_size['width']
        slider_value_max = 2000

        slider_current_value_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='number' and contains(@class, 'MuiInputBase-input')]")))
        current_slider_value = int(slider_current_value_element.get_attribute("value"))

        slider_set_value = value_set_to - current_slider_value
        pixel_move = (slider_width / slider_value_max) * slider_set_value

        slider_thumb = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//span[contains(@class,'MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary css-1sfugkh')]")))
        ActionChains(driver).drag_and_drop_by_offset(slider_thumb, pixel_move, 0).perform()
        time.sleep(1)
    except Exception as e:
        print(f"Error setting slider value: {e}")

def input_number(number_value):
    try:
        input_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='number' and contains(@class, 'MuiInputBase-input')]")))
        input_element.send_keys(Keys.BACK_SPACE * 4)
        input_element.send_keys(str(number_value))
        time.sleep(1)
    except Exception as e:
        print(f"Error inputting number: {e}")

def click_checkbox(cpt_code, value):
    try:
        checkbox = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//p[text()='{cpt_code}']/following::span[text()='{value}']/preceding::input[@type='checkbox'][1]")))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", checkbox)
        checkbox.click()
        time.sleep(1)
    except Exception as e:
        print(f"Error clicking checkbox for {cpt_code}: {e}")

def validate_total_reimbursement():
    try:
        recuring_reimbursement = wait.until(EC.presence_of_element_located((By.XPATH,
            "//div[@class='MuiBox-root css-m1khva']//p[@class='MuiTypography-root MuiTypography-body1 inter css-12bch19']")))
        print(f"Total Recurring Reimbursement: {recuring_reimbursement.text}")
        time.sleep(1)

        header_element = wait.until(EC.presence_of_element_located((By.XPATH, "//p[position()=4]//p[position()=1]")))
        print(f"Header displaying 'Total Recurring Reimbursement for all Patients Per Month:' shows the value: {header_element.text}, and the expected value is $110700")
        time.sleep(1)
    except Exception as e:
        print(f"Error validating total reimbursement: {e}")

def close_browser():
    driver.quit()

open_homepage("https://www.fitpeo.com/")
navigate_to_revenue_calculator()
adjust_window(412, 915)
scroll_to_slider()
#time.sleep(2)
set_slider_value(820)
#time.sleep(2)
adjust_window(1552, 832)
input_number(560)
#time.sleep(2)
click_checkbox('CPT-99091', '57')
click_checkbox('CPT-99453', '19.19')
click_checkbox('CPT-99454', '63')
click_checkbox('CPT-99474', '15')
validate_total_reimbursement()
close_browser()