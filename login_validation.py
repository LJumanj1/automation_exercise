import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Function: log in with a user and a password
def login_page(user, password):
    user_element = driver.find_element("id", "user_name")
    user_element.clear()
    user_element.send_keys(user)

    password_element = driver.find_element("id", "password")
    password_element.clear()
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)
    # wait for the inventory page to appear, with a maximum wait time of 3 seconds
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
    except TimeoutException:
        print("Login took too long!")


# set the Chrome webdriver path
chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
driver = webdriver.Chrome(chrome_driver_path)

# navigate to the URL
url = "https://www.saucedemo.com/"
driver.get(url)

# try to log in with standard user, enter the credentials
login_page("standard_user", "secret_sauce")

# validate successful login
assert "https://www.saucedemo.com/inventory.html" in driver.current_url

# logout
driver.find_element("id", "react-burger-menu-btn").click()
logout = driver.find_element("id", "logout_sidebar_link")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'logout_sidebar_link')))
logout.click()

# try to log in with locked user, enter credentials
login_page("locked_out_user", "secret_sauce")

# validate error
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'error')))
driver.find_element(By.CLASS_NAME, "error-button").click()

# try to log in with problem user, enter credentials
login_page("problem_user", "secret_sauce")

# validate successful login
assert "https://www.saucedemo.com/inventory.html" in driver.current_url

# check that all images of every item are the same
# DUE: CHECK PROBLEM USER

# logout
driver.find_element("id", "react-burger-menu-btn").click()
logout = driver.find_element("id", "logout_sidebar_link")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'logout_sidebar_link')))
logout.click()

# try to log in with performance_glitch_user, enter credentials
login_page("performance_glitch_user", "secret_sauce")

# close the browser
driver.close()
