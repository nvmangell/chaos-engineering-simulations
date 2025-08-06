import flask
from flask import jsonify
import get_status 
from status_param import IP
from status_param import Https
from datetime import datetime
#from status_param import Https, status_data


app = flask.Flask(__name__, static_folder='static', template_folder='templates')

def get_status_dict():
    timestamp = datetime.now()
    overall_status = 'healthy_container' if get_status.update_status() else 'issue_container'
    status_history_list = get_status.get_status_history(40)
    status_history_list_length = len(status_history_list)
    status_history_percentage = round((sum(status_tuple[1] for status_tuple in status_history_list) / status_history_list_length) * 100, 2) if status_history_list_length > 0 else 0
    vm1_status_circ = 'status-circle-healthy-container' if get_status.status_data["vm1"]['status'] else 'status-circle-issue-container'
    vm2_status_circ = 'status-circle-healthy-container' if get_status.status_data["vm2"]['status'] else 'status-circle-issue-container'
    http_status_circ = 'status-circle-healthy-container' if get_status.status_data["home"]["status"] else 'status-circle-issue-container'
    login_status_circ = 'status-circle-healthy-container' if get_status.status_data["login"]['status'] else 'status-circle-issue-container'
    register_status_circ = 'status-circle-healthy-container' if get_status.status_data["register"]['status'] else 'status-circle-issue-container'
    board_status_circ = 'status-circle-healthy-container' if get_status.status_data["board"]['board_status'] and get_status.status_data["board"]["chess_move_status"] else 'status-circle-issue-container'
    vm1_sd_circ = 'status-circle-healthy-container' if get_status.status_data["vm1_systemd"]["status"] else 'status-cricle-issue-container'
    vm2_sd_circ = 'status-circle-healthy-container' if get_status.status_data["vm2_systemd"]["status"] else 'status-cricle-issue-container'
    vm1_dn_circ = 'status-circle-healthy-container' if get_status.status_data["vm1_dotnet"]["status"] else 'status-cricle-issue-container'
    vm2_dn_circ = 'status-circle-healthy-container' if get_status.status_data["vm2_dotnet"]["status"] else 'status-cricle-issue-container'


    vm1_check_mark = "✓" if "healthy" in vm1_status_circ else "✘"
    vm2_check_mark = "✓" if "healthy" in vm2_status_circ else "✘"
    http_check_mark = "✓" if "healthy" in http_status_circ else "✘"
    login_check_mark = "✓" if 'healthy' in login_status_circ else "✘"
    register_check_mark = "✓" if 'healthy' in register_status_circ else "✘"
    board_check_mark = "✓" if 'healthy' in board_status_circ else "✘"
    vm1_sd_check_mark =  "✓" if 'healthy' in vm1_sd_circ else "✘"
    vm2_sd_check_mark =  "✓" if 'healthy' in vm2_sd_circ else "✘"
    vm1_dn_check_mark =  "✓" if 'healthy' in vm1_dn_circ else "✘"
    vm2_dn_check_mark =  "✓" if 'healthy' in vm2_dn_circ else "✘"


    html_dict = {
        'overall_status': overall_status,
        'vm1_status_circ': vm1_status_circ,
        'vm2_status_circ': vm2_status_circ,
        'http_status_circ': http_status_circ,
        'login_status_circ': login_status_circ,
        'vm1_check_mark': vm1_check_mark,
        'vm2_check_mark': vm2_check_mark,
        'http_check_mark': http_check_mark,
        'login_status_mark': login_check_mark,
        'register_status_circ': register_status_circ,
        'register_check_mark': register_check_mark,
        'board_status_circ': board_status_circ,
        'board_check_mark': board_check_mark,
        'status_history_list': status_history_list,
        'status_history_list_length': status_history_list_length,
        'status_history_percentage': status_history_percentage,
        'vm1_sd_circ': vm1_sd_circ,
        'vm2_sd_circ': vm2_sd_circ,
        'vm1_dn_circ': vm1_dn_circ,
        'vm2_dn_circ': vm2_dn_circ,
        'vm1_sd_check_mark': vm1_sd_check_mark,
        'vm2_sd_check_mark': vm2_sd_check_mark,
        'vm1_dn_check_mark': vm1_dn_check_mark,
        'vm2_dn_check_mark': vm2_dn_check_mark,
        'timestamp': timestamp
    }
    
    return html_dict


@app.route('/') 
def home():
    html_dict = get_status_dict()

    return flask.render_template('index.html', **html_dict)

@app.route('/status')
def status():
    #get_status.update_status()
    #vm1_status = get_status.ping_vm_good(IP.VM1_IP)["status"]
    #vm2_status = get_status.ping_vm_good(IP.VM2_IP)["status"]
    #home_status = get_status.status_data["home"]["status"]
    
    vm1_message = get_status.status_data["vm1"]["message"]
    vm2_message = get_status.status_data["vm1"]["message"]
    login_message = get_status.status_data["login"]["message"]
    register_message = get_status.status_data["register"]["message"]
    board_message = get_status.status_data["board"]["message"]
    home_message = get_status.status_data["home"]["message"]
    
    vm1_sd_message = get_status.status_data["vm1_systemd"]["message"]
    vm2_sd_message = get_status.status_data["vm2_systemd"]["message"]
    vm1_dn_message = get_status.status_data["vm1_dotnet"]["message"]
    vm2_dn_message = get_status.status_data["vm2_dotnet"]["message"]

    flask_status_code = get_status.status_data["home"]["code"]

    data = {
        "http_message": home_message,
        "vm1_message": vm1_message,
        "vm2_message": vm2_message,
        "login_message": login_message,
        "register_message": register_message,
        "board_message": board_message,
        "vm1_sd_message": vm1_sd_message,
        "vm2_sd_message": vm2_sd_message,
        "vm1_dn_message": vm1_dn_message,
        "vm2_dn_message": vm2_dn_message
    }

    return jsonify(data), flask_status_code


if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug = True)
     app.run(debug = True)