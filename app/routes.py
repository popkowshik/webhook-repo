from flask import Blueprint, request, render_template, jsonify
from . import db
from datetime import datetime
import time

main = Blueprint('main', __name__)
collection = db['events']  # Collection name inside your database

@main.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook received:", data)

    event_type = request.headers.get('X-GitHub-Event')  # Identify the event type
    print("Event Type:", event_type)
    if event_type == "push":
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

        msg = f'"{author}" pushed to "{to_branch}" on {timestamp}'

    elif event_type == "pull_request":
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

        msg = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'

    elif event_type == "ping":
        print("Ping received")
        return jsonify({"message": "Ping OK"}), 200
    
    else:
        print("Unhandled event:", event_type)
        return jsonify({"message": "Ignored"}), 200

    collection.insert_one({"message": msg, "timestamp": time.time()})
    return jsonify({"message": "Event stored"}), 200

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/events')
def get_events():
    events = list(collection.find().sort("timestamp", -1))
    messages = [e['message'] for e in events]
    return jsonify(messages)
