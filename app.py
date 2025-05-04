from flask import Flask, jsonify
from utils import get_faang_daily_returns

app = Flask(__name__)

@app.route('/daily-returns', methods=['GET'])
def daily_returns():
    try:
        returns = get_faang_daily_returns()
        return jsonify({"status": "success", "data": returns}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
