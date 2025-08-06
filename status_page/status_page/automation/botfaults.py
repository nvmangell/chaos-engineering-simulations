from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time

class Login:
    def __init__(self, username, password, link = "http://onemovechess-web.northcentralus.cloudapp.azure.com/Login"):
        self.username = username
        self.password = password
        self.link = link

def login_status(success, message):
    return {"success": success, "message": message}

def login_to_game(login):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)  # Use your desired browser driver
        driver.get(login.link)

        username = driver.find_element(By.ID, 'userName')
        username.send_keys(login.username)

        password = driver.find_element(By.ID, 'password')
        password.send_keys(login.password)

        submit = driver.find_element(By.ID, 'loginButton')
        submit.click()
        
        time.sleep(3)  # Wait for page to load

        login_block = driver.find_element(By.ID, 'accountLink')
        if login.username in login_block.text:
            result = login_status(True, f"Login successful for {login.username}")
        else:
            message = driver.find_element(By.XPATH, "/html/body/div/main/form/div[1]/div[3]").text
            result = login_status(False, f"Login failed for {login.username}, message: {message}")

        driver.quit()
        return result
    except Exception as e:
        return login_status(False, f"Login error for {login.username}: {str(e)}")

# Define 10 accounts
accounts = [
    Login("testbot1", "636Uq*MF@-h08ss89hW7JJ3@"),
    Login("testbot2", "nL12^Cj3P=rcMq1Sw4Dq%!p2"),
    Login("testbot3", "UQ07qdMO&790eAC01$A87@-F"),
    Login("testbot4", "^7q=*oW3359-%-tY09BP=9*K"),
    Login("testbot5", "L80%0+E-@&4E32s5bDV%0-$5"),
    Login("testbot6", "w8pre&H!%84qF@1_t2@A@*lT"),
    Login("testbot7", "i6005*$8&4Hi6aX6h=$_B!j8"),
    Login("testbot8", "Dtcg%G89@k3eL!2*b9e+!o3-"),
    Login("testbot9", "p0N02BKFI22RMsdJM=PO+Vqv"),
    Login("testbot10", "H^rdz#c6B!_d%_WLL-9O*Gy&"),
]

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(login_to_game, accounts))

for res in results:
    print(res)