import os


def kill_api():
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com sudo pkill dotnet")

def kill_webui():
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com sudo pkill dotnet")

#note: don't use this until we back up the db
def drop_games_from_db():
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com sqlite3 /home/azureuser/.config/OneMoveChess.db 'DROP TABLE games'")
def rename_db():
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com mv /home/azureuser/.config/OneMoveChess.db /home/azureuser/.config/OneMoveChess-Moved.db")

kill_api()
