from flask import Flask, request, jsonify, render_template
import json, os

app = Flask(__name__)

SCORES_FILE = 'scores.json'

# Helper: read/write scores
def read_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE) as f:
        return json.load(f)

def write_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

# Serve frontend
@app.route('/')
def index():
    return render_template('index.html')

# Submit a score
@app.route('/submitScore', methods=['POST'])
def submit_score():
    data = request.json
    name = data.get('name', 'Anon')
    score = data.get('score', 0)
    scores = read_scores()
    scores.append({'name': name, 'score': score})
    scores.sort(key=lambda x: x['score'], reverse=True)
    write_scores(scores[:10])  # keep top 10
    return jsonify({'status': 'ok'})

# Get leaderboard
@app.route('/getLeaderboard')
def get_leaderboard():
    return jsonify(read_scores())

if __name__ == '__main__':
    app.run(debug=True)
