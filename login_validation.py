import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Function: log in with a user and a password
def login_page(user, password):
    print("Login in with user \'" + user + "\'. . .")
    user_element = driver.find_element("id", "user-name")
    user_element.clear()
    user_element.send_keys(user)

    password_element = driver.find_element("id", "password")
    password_element.clear()
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    # wait for the inventory page to appear
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((
            By.CLASS_NAME, "shopping_cart_container")))
    except TimeoutException:
        print("Login took too long!")
        if driver.find_element(By.CLASS_NAME, 'error'):
            # validate error and close it
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'error')))
            assert driver.find_element(By.XPATH, "//h3[@data-test='error']").text == "Epic sadface: Sorry, this user " \
                                                                                     "has been locked out."
            print("User \'" + user + "\' couldn\'t log in")
            driver.find_element(By.CLASS_NAME, "error-button").click()
        return
    # validate successful login
    assert "https://www.saucedemo.com/inventory.html" in driver.current_url


# Function: log out from the page
def logout_page():
    driver.find_element("id", "react-burger-menu-btn").click()
    logout = driver.find_element("id", "logout_sidebar_link")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'logout_sidebar_link')))
    logout.click()
    print("Logged out :)")


# Function: validate all the items from the inventory page, without changing sorting
def validate_items():
    validate_single_item(1, "/static/media/sauce-backpack-1200x1500.0a0b85a3.jpg", "Sauce Labs Backpack")
    validate_single_item(2, "/static/media/bike-light-1200x1500.37c843b0.jpg", "Sauce Labs Bike Light")
    validate_single_item(3, "/static/media/bolt-shirt-1200x1500.c2599ac5.jpg", "Sauce Labs Bolt T-Shirt")
    validate_single_item(4, "/static/media/sauce-pullover-1200x1500.51d7ffaf.jpg", "Sauce Labs Fleece Jacket")
    validate_single_item(5, "/static/media/red-onesie-1200x1500.2ec615b2.jpg", "Sauce Labs Onesie")
    validate_single_item(6, "/static/media/red-tatt-1200x1500.30dadef4.jpg", "Test.allTheThings() T-Shirt (Red)")


# Function: validate image and name for an item of the current page
def validate_single_item(item, image, name):
    # validate the image hash of the item
    validated_image = driver.find_element(By.XPATH, "//div[@class='inventory_item'][" + str(item)
                                          + "]//img").get_attribute("src")
    try:
        assert validated_image == "https://www.saucedemo.com" + image
    except AssertionError:
        print("Image is not the same for item " + str(item) + "!")
        if validated_image == "https://www.saucedemo.com/static/media/sl-404.168b1cce.jpg":
            print("You found instead a cute dog!!")
    # validate the item's name
    validated_name = driver.find_element(By.XPATH, "//div[@class='inventory_item'][" + str(item)
                                         + "]//div[@class='inventory_item_name']").text
    try:
        assert validated_name == name
    except AssertionError:
        print("Name is not the same for item " + str(item) + "!")
    # due: validate description


# ----------------------------------------------------------------------------------------------------------------------

# set the Chrome webdriver path
chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
driver = webdriver.Chrome(chrome_driver_path)

# navigate to the URL
url = "https://www.saucedemo.com/"
driver.get(url)

# try to log in with standard user, enter the credentials
login_page("standard_user", "secret_sauce")
validate_items()
logout_page()

# try to log in with locked user, enter credentials
login_page("locked_out_user", "secret_sauce")

# try to log in with problem user, enter credentials
login_page("problem_user", "secret_sauce")
validate_items()
logout_page()

# try to log in with performance_glitch_user, enter credentials
login_page("performance_glitch_user", "secret_sauce")
validate_items()
logout_page()

# close the browser
driver.close()
