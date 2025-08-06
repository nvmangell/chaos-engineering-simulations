import json
import time
from fake_useragent import UserAgent
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ECimport 
from selenium.webdriver.support import expected_conditions as EC
import pdb
from automation.utils.constants import Login, Register, Time

def setup_driver():
    """
    Set up and return the Selenium WebDriver with undetected_chromedriver and fake user-agent.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-background-timer-throttling")  # Keep browser active
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://onemovechess-web.northcentralus.cloudapp.azure.com/')
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=options)
    return driver


def save_cookies(driver, filename):
    """
    Save cookies from the current browser session to a file.
    """
    cookies = driver.get_cookies()
    with open(filename, "w") as file:
        json.dump(cookies, file)
    print(f"Cookies saved to {filename}")

def load_login_cookies(driver, filename):
    """
    Load cookies from a file into the browser session.
    """
    with open(filename, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print(f"Cookies loaded from {filename}")

def login_and_store_cookies(driver):
    """
    Log in to LinkedIn and store session cookies.
    """
    driver.get(Login.link)
    Time.sleep()  # Wait for the login page to load

    # Perform login
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    email_field.send_keys("your_email@example.com")
    password_field.send_keys("your_password")
    password_field.send_keys(Keys.RETURN)
    Time.sleep()  # Wait for the login page to load

def login_to_game(driver):
    try:
        driver.get(Login.link)
        username = driver.find_element(By.ID, 'userName')
        username.send_keys(Login.username)
        signupcode = driver.find_element(By.ID, 'password')
        signupcode.send_keys(Login.password)

        submit = driver.find_element(By.ID, 'loginButton')
        submit.click()
        Time.sleep()
        login_block = driver.find_element(By.ID, 'accountLink')
        db = "OPT"
        if Login.username not in login_block.text:
            #Opt password does not work, trying confgi password
            print("password for opt failed... Trying config password.")
            signupcode.clear()
            signupcode.send_keys(Login.password2)
            submit.click()
            db = "config"
            Time.sleep()
            print("Finished logging in with config password.")
        # grab log in block again 
        login_block = driver.find_element(By.ID, 'accountLink')
        
        if Login.username in login_block.text:
            print("entered here!")
            return login_status(True, f"Login created successfully. Current database : {db}.")
        else:
            message = driver.find_element(By.XPATH, "/html/body/div/main/form/div[1]/div[3]").text
            return login_status(False, f"Login failed for both OPT and Config. Error code: {message}")
    except Exception as e:
        print(f"Login FAILED Error: {e}", )
        return login_status(False, f'Login bot failed. Database is unkown. Error: {e}')
        

def find_first_move(driver):
    squares = driver.find_elements(By.XPATH, "//div[contains(@class, 'square')]")
    print(f"Number of squares found: {len(squares)}")

    for square in squares:
        ActionChains(driver).move_to_element(square).perform()
        background_color = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');", square)
        if background_color == "rgb(169, 169, 169)" or background_color == "rgb(105, 105, 105)":
            target_square = get_drag_location(driver, square)
            return square, target_square
    return None, None

def get_drag_location(driver, start_square):
    squares = driver.find_elements(By.XPATH, "//div[contains(@class, 'square')]")
    for square in squares:
        background_color = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');", square
        )
        if (background_color == "rgb(105, 105, 105)" or background_color == "rgb(169, 169, 169)") and start_square != square:
            print("Found draging location")
            return square
    return None

def make_random_move(driver):
    start_square, target_square = find_first_move(driver)
    if start_square == None or target_square == None:
        print("No possible moves found!")
    else:
        print("dragging")
        ActionChains(driver).drag_and_drop(start_square, target_square).perform()
        print("Move performed!")
        return True
    return False

def bot_register(driver):   
    try:
        driver.get(Register.link)
        username = driver.find_element(By.ID, 'newUserName')
        username.send_keys(Register.username)

        signupcode = driver.find_element(By.ID, 'signUpCode')
        signupcode.send_keys(Register.sign_up_code)

        submit = driver.find_element(By.ID, 'registerUserButton')
        submit.click()
        Time.sleep()
        password_block = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordBlock')))
        if password_block.is_displayed():
            generated_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'newPassword')))
            print(f"Registered account successfully, PASSWORD: {generated_password}")
            return register_status(True, "Registration successful.")
        
        else:
            print("No password shown")
            return register_status(False, "Registration Failed! Errror: Bot failed to retrieve password block.")
        
    except Exception:
        return register_status(False, 'Register Broke causing register to fail')
    
def register_status(register_status: bool, message: str) -> dict:
    return {
        "status": register_status,
        "message": message
    }

def login_status(login_status: bool, message: str) -> dict:
    return {
        "status": login_status,
        "message": message
    }

def check_board_status(driver):
    driver.get("http://onemovechess-web.northcentralus.cloudapp.azure.com/Chess")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chessBoard")))
        board_message = "Chessboard Successfully Loaded"

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/main/h2")))
        try:
            make_random_move(driver)
            board_message = "Successfully Moved Chess Pieces and allocated new board"
            Time.sleep()
            return get_chessboard_status(True, True, board_message)
        except:
            board_message = "Loaded board but Failed to Move Chess Pieces"
            return get_chessboard_status(True, False, board_message)
    except:
        board_message = "Board Allocation Failed"
        return get_chessboard_status(False, False, board_message)

def bot_procedure():
    try:
        driver = setup_driver()
        register_status = bot_register(driver)
        driver.refresh()
        login_status = login_to_game(driver)
        board_status = check_board_status(driver)
    finally:
        print("bot finished")
        return register_status, login_status, board_status


def get_chessboard_status(board_status: bool, chess_move_status: bool, message: str) -> dict:
    return {
        "board_status": board_status,
        "chess_move_status": chess_move_status,
        "message": message
    } 