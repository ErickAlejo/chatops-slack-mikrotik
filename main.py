import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from core.sshmikrotik import send_command_to_device_mikrotik
from datetime import datetime

app = App(token=os.getenv("SLACK_BOT_TOKEN"))
slack_secret = os.getenv("SLACK_SIGNING_SECRET")                        
event_message = "!kit " # Don't remove space blank

@app.message(event_message + "test")
def test(message,say):
    try:
        # Parser message
        text = message['text']

        # Filter data 
        slack_message = text.split('-')
        unecesasary = slack_message[0].split(' ')
        unecesasary.remove("!mcli")
        unecesasary.remove("test")

        # Set the rest
        ip_address = unecesasary[0]
        command = slack_message[1]

        mikrotik = {
            'device_type': 'mikrotik_routeros',
            'host': ip_address,
            'command': command,
            'username': 'admin',
            'password': 'YOUR_PASSW',
        }
        print(mikrotik)

    except Exception as e:
        say(f"Error in mesg: {str(e)}")


@app.message(event_message + "run")
def run_on(message,say):
    try:
        # Parser message
        text = message['text']

        # Filter data 
        slack_message = text.split('-')
        unecesasary = slack_message[0].split(' ')
        unecesasary.remove(event_message)
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
def load_file_configuration(ack, body, client: WebClient)

@app.message(event_message)
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