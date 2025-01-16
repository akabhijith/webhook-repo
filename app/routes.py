from flask import Blueprint, render_template, jsonify, request
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('webhook', __name__)

@webhook.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.json
        print("Webhook received:", data)         
        event_type = request.headers.get('X-GitHub-Event')
        print(f"Event type from headers: {event_type}")
        author = data.get('sender', {}).get('login')
        if not author:
            print("Author not found in payload")
        else:
            print(f"Author: {author}")
        timestamp = datetime.now().strftime('%d %B %Y - %I:%M %p UTC')
        print("got timestamp")
        from_branch = None
        to_branch = None
        if event_type == "push":
            branch = data.get('ref', '').split('/')[-1]
            print(f"Branch: {branch}")
            message = f"{author} pushed to {branch} on {timestamp}"
        elif event_type == "pull_request":
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            print(f"From Branch: {from_branch}, To Branch: {to_branch}")
            message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
        else:
            return {"message": "Unsupported event"}, 400
        print(f"Generated Message: {message}")
        event_document = {
            "event_type": event_type,
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": message
        }
        mongo.db.events.insert_one(event_document)
        return {"message": "Event stored"}, 200

    return render_template('index.html')
@webhook.route('/api/events', methods=["GET"])
def get_events():
    events = list(mongo.db.events.find({}, {'_id': 0}))  # Exclude '_id'
    return jsonify(events)