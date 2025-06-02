from flask import Flask, request, send_from_directory
import subprocess
import os

app = Flask(__name__)

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

# Sert les fichiers statiques (HTML, JS, CSS, etc.)
@app.route('/Zynix_esbuild/dist/<path:filename>')
def serve_dist(filename):
    return send_from_directory(os.path.join('Zynix_esbuild', 'dist'), filename)

@app.route('/<path:filename>')
def serve_root_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)