from flask import Flask, render_template, request
from model import modelTrain, predictor
from recommendations import getSongs, get_motivational_tip

app = Flask(__name__)

# Load model ONCE (this is GOOD)
model, time_encoder, activity_encoder, colns, mood_encoder = modelTrain()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            sleep_hours = float(request.form["hoursSleep"])
            screen_time = float(request.form["screenTime"])
            activity = request.form["doings"].strip().lower()
            time_of_day = request.form["time"].strip().lower()
            mood_scale = int(request.form["feeling"])
            social_pref = request.form["social"].strip().lower()

            input_list = [
                sleep_hours,
                screen_time,
                activity,
                time_of_day,
                mood_scale,
                social_pref
            ]

            predicted_mood = predictor(
                input_list,
                model,
                time_encoder,
                activity_encoder,
                mood_encoder,
                colns
            )

            predicted_mood = str(predicted_mood)
            songs = getSongs(predicted_mood)
            tip = get_motivational_tip(predicted_mood)

            return render_template(
                "result.html",
                mood=predicted_mood,
                songs=songs,
                tip=tip
            )

        except Exception as e:
            return f"Something went wrong: {e}"

    return render_template("index.html")


# 🔴 CHANGE IS HERE ONLY 👇
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
