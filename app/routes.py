from flask import Blueprint, render_template, jsonify, request
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('webhook', __name__)

@webhook.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.json
        event_type = data.get('action')
        author = data.get('sender', {}).get('login')
        timestamp = datetime.now().strftime('%d %B %Y - %I:%M %p UTC')

        if event_type == "push":
            branch = data.get('ref', '').split('/')[-1]
            message = f"{author} pushed to {branch} on {timestamp}"
        elif event_type == "pull_request":
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
        elif event_type == "merge":
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            message = f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
        else:
            return {"message": "Unsupported event"}, 400

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