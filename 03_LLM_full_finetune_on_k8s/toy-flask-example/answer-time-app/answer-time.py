from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/answer_current_time", methods=["GET"])
def answer_current_time():
    print("In answer-time")
    now = datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time is: {current_time_str}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
