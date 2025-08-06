from dataclasses import dataclass

@dataclass
class Https:
    url_home= "http://onemovechess-web.northcentralus.cloudapp.azure.com/"
    url_register= "http://onemovechess-web.northcentralus.cloudapp.azure.com/Register"
    url_login= "http://onemovechess-web.northcentralus.cloudapp.azure.com/login"
    BOT = {"botname": "testbot2", "password": "nL12^Cj3P=rcMq1Sw4Dq%!p2"}

@dataclass
class IP:
    VM1_IP = '52.225.235.130'
    VM2_IP = '65.52.239.81'

status_data = {
    "home": {"status": None, "url": Https.url_home, "message": '', 'code': None},
    "register": {"status": None, "url": Https.url_register, "message": ''},
    "board": {"board_status": None, "chess_move_status": None, "url": Https.url_register, "message": ''},
    "login": {"status": None, "url": Https.url_login, "message": ''},
    "vm1": {"status": None, "url": Https.url_login, "message": ''},
    "vm2": {"status": None, "message": ''},
    "vm1_systemd": {"status": None, "message": ''},
    "vm2_systemd": {"status": None, "message": ''},
    "vm1_dotnet": {"status": None, "message": ''},
    "vm2_dotnet": {"status": None, "message": ''},
}
