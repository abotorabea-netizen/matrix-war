from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "Matrix_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"players": {}, "alliances": {}, "battles": [], "news": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return jsonify({"status": "Matrix War API is running"})

@app.route('/api/player/<user_id>')
def get_player(user_id):
    data = load_data()
    player = data.get("players", {}).get(user_id)
    if not player:
        return jsonify({"error": "not found"}), 404
    return jsonify(player)

@app.route('/api/rank')
def get_rank():
    data = load_data()
    players = data.get("players", {})
    rank = []
    for pid, p in players.items():
        power = (p.get("vikings",0)*5 + p.get("knights",0)*10 + 
                 p.get("archers",0)*7 + p.get("catapult",0)*20)
        rank.append({
            "kingdom_name": p.get("kingdom_name"),
            "power": power,
            "gold": p.get("gold", 0)
        })
    rank.sort(key=lambda x: x["power"], reverse=True)
    return jsonify(rank[:10])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
