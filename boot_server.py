from flask import Flask, request, jsonify

app = Flask(__name__)
storage = {}

@app.route('/set/<key>', methods=['POST'])
def set_key(key):
    value = request.json.get('value')
    storage[key] = value
    return jsonify({"message": f"Key '{key}' set to '{value}'"}), 200

@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    value = storage.get(key, None)
    if value is None:
        return jsonify({"error": f"Key '{key}' not found"}), 404
    return jsonify({"key": key, "value": value}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8468)
