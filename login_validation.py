import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# set the Chrome webdriver path
chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
driver = webdriver.Chrome(chrome_driver_path)

# navigate to the URL
url = "https://www.saucedemo.com/"
driver.get(url)

# try to log in with standard user, enter the credentials
username = driver.find_element("id", "user-name")
username.clear()
username.send_keys("standard_user")

password = driver.find_element("id", "password")
password.clear()
password.send_keys("secret_sauce")
password.send_keys(Keys.RETURN)

# wait for the products page to appear, with a maximum wait time of 3 seconds
try:
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
except TimeoutException:
    print("Login took too long!")

# validate successful login
assert "https://www.saucedemo.com/inventory.html" in driver.current_url

# logout
driver.find_element("id", "react-burger-menu-btn").click()
logout = driver.find_element("id", "logout_sidebar_link")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'logout_sidebar_link')))
logout.click()

# try to login with locked user, enter credentials
username = driver.find_element("id", "user-name")
username.clear()
username.send_keys("locked_out_user")

password = driver.find_element("id", "password")
password.clear()
password.send_keys("secret_sauce")
password.send_keys(Keys.RETURN)

# validate error
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'error')))
driver.find_element(By.CLASS_NAME, "error-button").click()

# try to login with problem user, enter credentials
username = driver.find_element("id", "user-name")
username.clear()
username.send_keys("problem_user")

password = driver.find_element("id", "password")
password.clear()
password.send_keys("secret_sauce")
password.send_keys(Keys.RETURN)

# wait for the products page to appear, with a maximum wait time of 3 seconds
try:
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
except TimeoutException:
    print("Login took too long!")

# validate successful login
assert "https://www.saucedemo.com/inventory.html" in driver.current_url

# check that all images of every item are the same NOTE: can't make it work quickly due to two different elements
# being of same class
# img_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_img") expected_src =
# img_elements[0].get_attribute("src") for img_element in img_elements: print(img_element.get_attribute("src"))
# print(expected_src) assert img_element.get_attribute("src") == expected_src

# due: check the error in the last inventory item

# logout
driver.find_element("id", "react-burger-menu-btn").click()
logout = driver.find_element("id", "logout_sidebar_link")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'logout_sidebar_link')))
logout.click()

# try to login with performance_glitch_user, enter credentials
username = driver.find_element("id", "user-name")
username.clear()
username.send_keys("locked_out_user")

password = driver.find_element("id", "password")
password.clear()
password.send_keys("secret_sauce")
password.send_keys(Keys.RETURN)

# wait for the products page to appear, with a maximum wait time of 3 seconds
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
except TimeoutException:
    print("Login took too long!")

# close the browser
driver.close()
