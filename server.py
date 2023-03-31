
from flask import Flask, jsonify, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
client = Client(account_sid, auth_token)


from whisper import transcribe
import uuid

app = Flask(__name__)


def fetch(url):
    r = requests.get(url, allow_redirects=True)
    filename = "/tmp/{}".format(uuid.uuid1())
    open(filename, 'wb').write(r.content)
    return filename


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World!"})

@app.route('/bot-status', methods=['POST'])
def bot_status():
    incoming_msg = request.values.get('Body', '')
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    msg.body('working fine beep boop')
    responded = False
    return str(resp)

@app.route('/bot-receiver', methods=['POST'])
def bot_receiver():
    resp = MessagingResponse()
    msg = resp.message()
    try:
        incoming_msg = request.values.get('MediaUrl0', '')
        number = request.values.get('From', '')
        print(number)
        print(incoming_msg)
        path_to_audio = fetch(incoming_msg)
        print(path_to_audio)
        transcript = transcribe(path_to_audio)
        print(transcript)
        # msg.body(transcript)

        if not transcript:
            raise Exception("No transcript found")

        message = client.messages.create(
        from_=twilio_number,
        body=transcript,
        to=number
        )

        print(message.sid)

    except:
        msg.body('somethings wrong... my b')
    return str(resp)

if __name__ == '__main__':
    app.run(port=5002)