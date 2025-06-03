from flask import Flask, request, send_from_directory, jsonify
import subprocess
import os
import requests  # Assurez-vous d'avoir installé la bibliothèque requests

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # Mets ta clé dans une variable d'environnement
HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY")

@app.route('/')
def index():
    return send_from_directory('.', 'gallery.html')

@app.route('/Zynix_esbuild/dist/<path:filename>')
def custom_static(filename):
    return send_from_directory('Zynix_esbuild/dist', filename)

# ...dans app.py...
@app.route('/api/openai', methods=['POST'])
def openai_proxy():
    data = request.get_json()
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data,
            timeout=30
        )
        print("OpenAI status:", response.status_code)
        print("OpenAI response:", response.text)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.Timeout:
        print("OpenAI API timeout")
        return jsonify({"error": {"message": "OpenAI API timeout"}}), 504
    except Exception as e:
        print("OpenAI API error:", str(e))
        return jsonify({"error": {"message": str(e)}}), 500


@app.route('/api/hunter', methods=['GET'])
def hunter_proxy():
    company = request.args.get('company')
    response = requests.get(
        "https://api.hunter.io/v2/domain-search",
        params={
            "company": company,
            "api_key": HUNTER_API_KEY
        }
    )
    return jsonify(response.json()), response.status_code


@app.route('/update_csv', methods=['POST'])
def update_csv():
    data = request.get_json()
    with open('test.csv', 'w', encoding='utf-8') as f:
        f.write(data['csv'])
    return {'status': 'ok'}

@app.route('/run_enrichment', methods=['POST'])
def run_enrichment():
    subprocess.Popen(['python', 'csv_to_df.py'])
    return {'status': 'enrichment started'}


@app.route('/<path:filename>')
def serve_root_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)