from dataclasses import dataclass
import random
import time

@dataclass
class Login:
    username = "testbot2"
    password = "nL12^Cj3P=rcMq1Sw4Dq%!p2"
    password2 = "O-u+dw7e2O960Yjq=ZJ$-^4e"
    cookies_file_path = "automation/utils/cookies.json"
    link = "http://onemovechess-web.northcentralus.cloudapp.azure.com/Login"

@dataclass
class Register:
    username = 'BOT_TEST_REGISTER'
    sign_up_code = 'Carleton comps 2024-2025!'
    link = "http://onemovechess-web.northcentralus.cloudapp.azure.com/Register"

class Time:
    def sleep():
        return time.sleep(random.uniform(2, 4))
