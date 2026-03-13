from flask import Flask, request, jsonify

app = Flask(__name__)

#1. create event class because i will use instances of it to store my data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return ({"id": self.id, "title": self.title})
    
#2. create a list of events that will act as my mock database
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

#3. create my get routes

@app.route("/", methods=["GET"])
def all_events():
    events_list = [e.to_dict() for e in events]
    return jsonify(events_list), 200

@app.route("/events/<int:id>", methods=["GET"])
def specific_event(id):
    event = next(e.to_dict() for e in events if e.id == id)
    if not event:
        return "Event not found, please try a different id.", 404
    return jsonify(event), 200 

#4. create post route

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    highest_id = max((e.id for e in events), default=0) + 1
    new_event = Event(id=highest_id, title=data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

#5. create patch route
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    data = request.get_json()
    event = next((e for e in events if e.id == id), None)
    if not event:
        return "No event with this id exists, please try a different id.", 404
    if "title" in data:
     event["title"] = data["title"]
    return jsonify(event.to_dict)

@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    global events
    event = next((e for e in events if e.id == id), None)
    if not event:
        return "No event with this id exists, please try a different id.", 404
    events = [e for e in events if e.id != id]
    return "Event deleted successfully", 204



if __name__ == "__main__":
    app.run(debug=True)
