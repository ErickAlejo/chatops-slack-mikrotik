# Author: Erick Alejandro Graterol
# Bot: netoolkit
# Description: toolkit to working on routers, backups-files and text

# Third-part and natives
import os
from slack_bolt import App
from datetime import datetime
from slack_sdk import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Local vars and classes
from core.sshmikrotik import send_command_to_device_mikrotik
from core.config.paths import folder_of_backups_file
from core.helpers.file_management import SEARCH
from core.helpers.file_management import READ

# Init APP
app = App(token=os.getenv("SLACK_BOT_TOKEN"))
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
slack_secret = os.getenv("SLACK_SIGNING_SECRET")                        
event_message = "!kit " # Don't remove space blank


@app.message(event_message + "test")
def test_run(message, say):
    try:
        # Parser message
        text = message['text']

        # Filter data 
        slack_message = text.split('-')
        unecesasary = slack_message[0].split(' ')
        unecesasary.remove("!kit")
        unecesasary.remove("test")

        # Set the rest
        ip_address = unecesasary[0]
        command = slack_message[1]

        mikrotik = {
            'device_type': 'mikrotik_routeros',
            'host': ip_address,
            'command': command,
            'username': 'admin',
            'password': 'Erudit',
        }
        print(mikrotik)

    except Exception as e:
        say(f"Error in mesg: {str(e)}")

@app.message(event_message + "load")
def test_upload(message, say, body):

    text = message['text']
    slack_message = text.split(' ', 2)
    slack_message.remove("!kit") # Remove command
    slack_message.pop(0) # Remove flag and just take message of slack

    filename_get_from_slack = slack_message[0] + ".txt"

    find_file = SEARCH.file_in_folder(folder_of_backups_file, filename_get_from_slack)
    print(find_file)
    if find_file:
        new_file = client.files_upload_v2(
            title = "Backup File",
            filename = f"{filename_get_from_slack}",
            content = f"{READ.txt_file(f'{folder_of_backups_file}/{filename_get_from_slack}')}",
        )

        file_url = new_file.get("file").get("permalink")
        new_message = client.chat_postMessage(
            channel = f"{body['event']['channel']}",
            text = f"Your File here {file_url}"
        )

    else:
        say("```🟥 Not found your file```")



@app.message(event_message + "run")
def run_on(message, say):
    try:
        # Parser message
        text = message['text']

        # Filter data 
        slack_message = text.split('-')
        unecesasary = slack_message[0].split(' ')
        unecesasary.remove("!kit")
        unecesasary.remove("run")

        # Set the rest
        ip_address = unecesasary[0]
        command = slack_message[1]

        # Execute on device
        data = send_command_to_device_mikrotik(ip_address, command)

        # Get datetime
        now = datetime.now()
        formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")

        # Send to channel slack
        say(f"🔸 Host : *{ip_address}*\n🔸 Command : '{command}'\n🔸 Executed at: {formatted_time}\n ```{data}```")
    
    except Exception as e:
        say(f"Error in mesg: {str(e)}")

@app.message(event_message + "load")
def load_file_configuration(message, say, body):
    text = message['text']
    slack_message = text.split(' ', 2)
    slack_message.remove("!kit") # Remove command
    slack_message.pop(0) # Remove flag and just take message of slack

    filename_get_from_slack = slack_message[0] + ".txt"

    find_file = SEARCH.file_in_folder(folder_of_backups_file, filename_get_from_slack)
    print(find_file)
    if find_file:
        new_file = client.files_upload_v2(
            title = "Backup File",
            filename = f"{filename_get_from_slack}",
            content = f"{READ.txt_file(f'{folder_of_backups_file}/{filename_get_from_slack}')}",
        )

        file_url = new_file.get("file").get("permalink")
        new_message = client.chat_postMessage(
            channel = f"{body['event']['channel']}",
            text = f"Your File here {file_url}"
        )

    else:
        say("```🟥 Not found your file```")


@app.message(event_message + 'help')
def help(say):
    try:
        helpman = [
        f"{event_message}                          - Print manual",
        f"{event_message} run     <IP> - <COMMAND> - Execute command on device mikrotik for instance: !mcli run 100.127.x.x - interface print detail where x",
        f"{event_message} load    <HOSTNAME>       - Load device configuration-backup",
        f"{event_message} search  <WORD>           - Search all devices with an Hostname specific"
        ]

        mesg = "\n".join(line for line in helpman)
        like_block_code = str(f"```{mesg}```")
        say(like_block_code)
        
    except Exception as e:
        say(f"Error in mesg {str(e)}")


if __name__ == "__main__":
    try:            
        handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
        handler.start()

    except KeyboardInterrupt:
        print("\nStopped ...\n")
