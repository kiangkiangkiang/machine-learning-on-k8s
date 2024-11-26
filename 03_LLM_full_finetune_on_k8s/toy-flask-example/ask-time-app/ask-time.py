import requests
from flask import Flask

app = Flask(__name__)


@app.route("/ask_time", methods=["GET"])
def ask_time():
    print("In ask-time")
    try:
        response = requests.get(
            "http://answer-time-service:5000/answer_current_time", timeout=5
        )
        response.raise_for_status()  # 檢查 HTTP 狀態碼
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Error occurred while contacting answer-time-service", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
