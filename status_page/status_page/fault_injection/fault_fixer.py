import os

def restart_api():
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com "sudo killall dotnet; cd /opt/OneMoveChess; nohup dotnet OneMoveChess.WebUI.dll 1> /var/log/onemovechess.log 2> /var/log/onemovechess.log &"')

def restart_webui():
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com "sudo killall dotnet; cd /opt/OneMoveChess; nohup dotnet OneMoveChess.WebUI.dll 1> /var/log/onemovechess.log 2> /var/log/onemovechess.log &"')

def rename_db():
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com mv /home/azureuser/.config/*.db /home/azureuser/.config/OneMoveChess.db')
    restart_api()

restart_api()
restart_webui()
