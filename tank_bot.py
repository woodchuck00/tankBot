#!/usr/bin/python

import re
import time
import json
import psutil
import os
import requests

from slackclient import SlackClient

current = os.path.dirname(os.path.realpath(__file__))
config_json = os.path.join(current, 'config.json')


# Get config file for api keys
with open(config_json, 'r') as f:
    config = json.load(f)

slack_api = config['SLACK_CONFIG']['api']
slack_channel = config['SLACK_CONFIG']['channel']
slack_config = config['SLACK_CONFIG']['clientId']

# Get SlackBot
slack_client = SlackClient(slack_api)

# Delay or reading stream
RTM_READ_DELAY = 1

# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "tankbot":
        slack_user_id = user.get('id')
        break


def process_command(message):
    """
        Process bot command
    """

    if 'client_msg_id' in message:
        if message['text'].startswith("<@%s>" % slack_user_id):

            print "Message received: %s" % json.dumps(message, indent=2)

            message_text = message['text'].\
                split("<@%s>" % slack_user_id)[1].\
                strip()

            if re.match(r'.*(cpu).*', message_text, re.IGNORECASE):
                cpu_pct = psutil.cpu_percent(interval=1, percpu=False)

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text="My CPU is at %s%%." % cpu_pct,
                    as_user=True)

            if re.match(r'.*(memory|ram).*', message_text, re.IGNORECASE):
                mem = psutil.virtual_memory()

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text="My RAM is at %s%%." % mem.percent,
                    as_user=True)

            if re.match(r'.*(temp).*', message_text, re.IGNORECASE):
                temp = psutil.sensors_temperatures()

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text="My temperature is at %sC." %
                    temp['cpu-thermal'][0][1],
                    as_user=True)

            if re.match(r'.*(reboot).*', message_text, re.IGNORECASE):
                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text="Tankbot needs to take a break.",
                    as_user=True)
                os.system("sudo reboot")

            if re.match(r'.*(live).*', message_text, re.IGNORECASE):
                url = 'https://api.twitch.tv/helix/streams?user_login=markham_stein'

                r = requests.get(url, headers={'Client-ID': slack_config})
                json_r = r.json()
                data = json_r['data']
                print (data)
                if not data:
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Stream is off. ",
                        as_user=True)
                else:
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Stream is on.",
                        as_user=True)


def hello_tankbot():
    """
        Say hello when bot goes online
    """
    slack_client.api_call(
        "chat.postMessage",
        channel=slack_channel,
        text="Tankbot is now online",
        as_user=True)


# Make Connection to the Slack API
if slack_client.rtm_connect(with_team_state=False):
    print "Connected!"
    hello_tankbot()

    while True:
        try:
            for message in slack_client.rtm_read():
                process_command(message)
            time.sleep(RTM_READ_DELAY)
        except Exception as e:
            print("Reconnecting..." + str(e))
            slack_client.rtm_connect(with_team_state=False)
else:
    print("Connection failed. Exception traceback printed above.")
