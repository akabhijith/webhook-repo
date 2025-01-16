Webhook Repository
This repository captures GitHub webhook events (push, pull_request, merge), stores them in a MongoDB database, and displays the events in a dynamically updating UI.

Features
Automatically processes GitHub webhook events.
Stores event data in MongoDB.
Displays the latest events on a user-friendly web page.
Dynamically updates every 15 seconds.
Setup and Deployment
Clone the Repository:

Instruction
git clone https://github.com/akabhijith/webhook-repo.git
cd webhook-repo
Set Up Environment Variables:

Define MONGO_URI with your MongoDB connection string.
For local testing, use a .env file:
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/github_events?retryWrites=true&w=majority

Add GitHub Webhook:

Go to Settings → Webhooks in your GitHub repository.
