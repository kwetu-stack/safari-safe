from flask import Flask, render_template, request, redirect, jsonify
import uuid

app = Flask(__name__)

# TEMP storage (in-memory)
locations = {}

# -----------------------
# Home
# -----------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------
# Start Journey
# -----------------------
@app.route("/start", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        destination = request.form.get("destination")

        # Generate unique journey ID
        journey_id = str(uuid.uuid4())[:8]

        return redirect(f"/live/{journey_id}")

    return render_template("start.html")


# -----------------------
# Traveler (sends location)
# -----------------------
@app.route("/live/<journey_id>")
def live(journey_id):
    return render_template("live.html", journey_id=journey_id)


# -----------------------
# Viewer (tracks location)
# -----------------------
@app.route("/track/<journey_id>")
def track(journey_id):
    return render_template("track.html", journey_id=journey_id)


# -----------------------
# API: Update Location
# -----------------------
@app.route("/update_location/<journey_id>", methods=["POST"])
def update_location(journey_id):
    data = request.get_json()

    lat = data.get("latitude")
    lng = data.get("longitude")

    locations[journey_id] = {
        "lat": lat,
        "lng": lng
    }

    return jsonify({"status": "ok"})


# -----------------------
# API: Get Location
# -----------------------
@app.route("/get_location/<journey_id>")
def get_location(journey_id):
    return jsonify(locations.get(journey_id, {}))


# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)