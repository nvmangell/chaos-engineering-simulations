''''
get_status.py
Returns status of One Move Chess Components
'''

import os
import time
import csv
import concurrent
import pandas as pd
import requests
import sys
from status_param import Https, status_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from notify import send_alert_email
from collections import deque
from status_param import IP
from automation.bot import bot_procedure
import subprocess

def ping_vm_good(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        return {"status": True,
                "message": "VM is running with No errors"
                }
    else:
        return {"status": False,
                "message": "VM is running with No errors"
                }

def check_vm1_systemd():
    try:
        command = "ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com pgrep -l systemd || true"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and "systemd" in result.stdout:
            return {"status": True, "message": f'VM1 System Domain Up & Running.'}
        else:
            return {"status": False, "message": f'ERROR: VM1 System Domain Down. Outputted: {result.stdout.strip()}'}
    except Exception as e:
        return {"status": False, "message": f'ERRRO: VM1 System Domaind Down. Ouputted: {str(e)}'}
        
def check_vm2_systemd():
    try:
        command = "ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com pgrep -l systemd || true"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and "systemd" in result.stdout:
            return {"status": True, "message": f'VM2 System Domain Up & Running.'}
        else:
            return {"status": False, "message": f'ERROR: VM2 System Domain Down. Outputted: {result.stdout.strip()}'}
    except Exception as e:
        return {"status": False, "message": f'ERRRO: VM2 System Domaind Down. Ouputted: {str(e)}'}
        

def check_vm1_dotnet_running():
    try:
        command = "ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com pgrep -l dotnet"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and "dotnet" in result.stdout:
            return {"status": True, "message": "VM1 Dotnet is running."}
        elif "Permission denied" in result.stderr or "Could not resolve hostname" in result.stderr:
            return {"status": False, "message": f"SSH ERROR: {result.stderr.strip()}"}
        else:
            return {"status": False, "message": "ERROR: VM1 Dotnet is not running."}
    except Exception as e:
        return {"status": False, "message": f"ERROR: {str(e)}"}

def check_vm2_dotnet_running():
    try:
        command = "ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com pgrep -l dotnet || true"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and "dotnet" in result.stdout:
            return {"status": True, "message": "VM2 Dotnet is running."}
        elif "Permission denied" in result.stderr or "Could not resolve hostname" in result.stderr:
            return {"status": False, "message": f"SSH ERROR: {result.stderr.strip()}"}
        else:
            return {"status": False, "message": "ERROR: VM2 Dotnet is not running."}
    except Exception as e:
       return {"status": False, "message": f"ERROR: {str(e)}"}

def check_http_status(url: str):
    try:
        session = requests.Session()
        response = session.get(url, allow_redirects=True)

        final_url = response.url
        print(f"Final URL after redirects: {final_url}")

        if final_url == Https.url_login and url != Https.url_login:
            print(f"Redirected to login page: {final_url}")
            return {
                "status": False,
                "code": response.status_code,
                "message": "Redirected to login page",
                "final_url": final_url
            }

        elif response.status_code == 200:
            print(f"Status code: {response.status_code} - Reached the correct page")
            return {
                "status": True,
                "code": response.status_code,
                "message": "Page loaded successfully",
                "final_url": final_url
            }

        else:
            print(f"Website returned status code: {response.status_code}")
            return {
                "status": False,
                "code": response.status_code,
                "message": f"Error: Unexpected status code {response.status_code}",
                "final_url": final_url
            }

    except requests.exceptions.RequestException as e:
        # for errors
        print(f"An error occurred: {e}")
        return {
            "status": False,
            "code": None,
            "message": f"Request failed with error: {e}",
            "final_url": None
        }

# created a global variable to check if a message has already been sent.
# I don't want it sending us emails constantly if something is down, just one is fine.
prev_failed_services = set() 

def update_status():
    global prev_failed_services
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(ping_vm_good, IP.VM1_IP): "vm1_info",
            executor.submit(ping_vm_good, IP.VM2_IP): "vm2_info",
            executor.submit(check_http_status, status_data["home"]["url"]): "home_status_info",
            executor.submit(check_vm1_systemd): "vm1_sd_info",
            executor.submit(check_vm2_systemd): "vm2_sd_info",
            executor.submit(check_vm1_dotnet_running): "vm1_dotnet_info",
            executor.submit(check_vm2_dotnet_running): "vm2_dotnet_info",
            executor.submit(bot_procedure): "bot_info"
        }
        results = {}
        for future in concurrent.futures.as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = {"status": False, "message": f"Error: {e}"}

    vm1_info = results["vm1_info"]
    vm2_info = results["vm2_info"]
    home_status_info = results["home_status_info"]
    register_status_info, login_status_info, board_status_info = results["bot_info"]
    vm1_sd_info = results["vm1_sd_info"]
    vm2_sd_info = results["vm2_sd_info"]
    vm1_dotnet_info = results["vm1_dotnet_info"]
    vm2_dotnet_info = results["vm2_dotnet_info"]


    status_data["home"]["status"] = home_status_info["status"]
    status_data["home"]["message"] = home_status_info["message"]
    status_data["home"]["code"] = home_status_info["code"]
    status_data["register"]["status"] = register_status_info["status"]
    status_data["register"]["message"] = register_status_info["message"]
    status_data["board"]["board_status"] = board_status_info["board_status"]
    status_data["board"]["chess_move_status"] = board_status_info["chess_move_status"]
    status_data["board"]["message"] = board_status_info["message"]
    status_data["login"]["status"] = login_status_info["status"]
    status_data["login"]["message"] = login_status_info["message"]
    status_data["vm1"]["status"] = vm1_info["status"]
    status_data["vm1"]["message"] = vm1_info["message"]
    status_data["vm2"]["status"] = vm1_info["status"]
    status_data["vm2"]["message"] = vm1_info["message"]
    status_data["vm1_systemd"]["status"] = vm1_sd_info["status"]
    status_data["vm1_systemd"]["message"] = vm1_sd_info["message"]
    status_data["vm2_systemd"]["status"] = vm2_sd_info["status"]
    status_data["vm2_systemd"]["message"] = vm2_sd_info["message"]
    status_data["vm1_dotnet"]["status"] = vm1_dotnet_info["status"]
    status_data["vm1_dotnet"]["message"] = vm1_dotnet_info["message"]
    status_data["vm2_dotnet"]["status"] = vm2_dotnet_info["status"]
    status_data["vm2_dotnet"]["message"] = vm2_dotnet_info["message"]


    
    
    # this checks which parts are failing
    failed_services = set()
    if not home_status_info["status"]:
        failed_services.add("home")
    if not register_status_info["status"]:
        failed_services.add("register")
    if not login_status_info["status"]:
        failed_services.add("login")
    if not vm1_dotnet_info["status"]:
        failed_services.add("vm1 dotnet")
    if not vm2_dotnet_info["status"]:
        failed_services.add("vm2 dotnet")
    if not vm1_sd_info["status"]:
        failed_services.add("vm1 system domain")
    if not vm2_sd_info["status"]:
        failed_services.add("vm2 system domain")

    # Update status history (status_history.csv)
    # Updates the history CSV to reflect a failure on the status page history 
    # Also adds a new row in the history CSV when a new day starts
    df = pd.read_csv("status_history.csv", sep=';')
    current_time = time.localtime()
    midnight_struct = time.struct_time((
        current_time.tm_year, current_time.tm_mon, current_time.tm_mday, 
        0, 0, 0,  # Set hours,minutes,seconds to 0
        current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst
    ))
    start_of_today = int(time.mktime(midnight_struct))
    last_entry_time = df.at[0, "start_of_day"]
    if start_of_today >= last_entry_time + 86400:
        new_default_row = pd.DataFrame({
            "start_of_day": [start_of_today], 
            "status": [0],
            "status_info": [0]
        })
        df = pd.concat([new_default_row, df], ignore_index=True)
        df.to_csv("status_history.csv", sep=';', index=False)
        df = pd.read_csv("status_history.csv", sep=';')
    if failed_services:
        print(df.at[0, "status_info"])
        failures_list_str = None

        if df.at[0, "status_info"] == '0':
            failures_list_str = ', '.join(failed_services)
        else:
            old_failures = df.at[0, "status_info"].split(', ')
            updated_failed_services = failed_services | set(old_failures)
            failures_list_str = ', '.join(updated_failed_services)
        df.at[0, "status_info"] = failures_list_str
        df.at[0, "status"] = 1
        df.to_csv("status_history.csv", sep=';', index=False) 
    # End of status history code

    # Emailing service
    if failed_services != prev_failed_services:
        if failed_services:
            subject = "ALERT: Service Failures Detected"
            details = []
            for service in failed_services:
                s = status_data[service]
                details.append(f"{service.capitalize()} page error: {s['message']}")
            body = "\n".join(details)
            send_alert_email(subject, body)
        else:
            subject = "All services recovered"
            body = "All services are now healthy."
            send_alert_email(subject, body)

        prev_failed_services = failed_services.copy()

    return len(failed_services) == 0

def format_date(epoch_time):
    struct_time = time.localtime(epoch_time)
    day = struct_time.tm_mday  # Get the day
    month = time.strftime("%b", struct_time)  # Get abbreviated month
    if 10 <= day % 100 <= 20: # get correct suffix
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return f"{month} {day}{suffix}"

def get_status_history(days: int) -> list:
    '''
    days: number of days worth of statuses to retrieve
    '''
    return_queue = deque([])
    with open("status_history.csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader) # skip the header
        row_count = sum(1 for row in reader)
        if days > row_count: 
            days = row_count
        
        csvfile.seek(0) # Put reader back to start
        header = next(reader) # skip header

        for row in range(days):
            curr_row = next(reader)
            date = format_date(float(curr_row[0]))
            status = not bool(int(curr_row[1]))  # csv stores status as 0 or 1
            status_info = curr_row[2] #this is a string
            return_queue.appendleft((date, status, status_info))

    return list(return_queue)
