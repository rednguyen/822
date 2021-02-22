import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from googletrans import Translator


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token = os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']



@slack_event_adapter.on('message')
def message(payLoad):
    print("quit")
    event = payLoad.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    translator = Translator(service_urls=['translate.googleapis.com'])
    translation = translator.translate(text, dest='ko')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=translation.text)

if __name__ == "__main__":
    app.run(debug=True)