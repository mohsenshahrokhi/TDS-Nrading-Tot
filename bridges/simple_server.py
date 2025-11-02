from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return {"status": "OK", "message": "NDS Server Running"}

if __name__ == '__main__':
    print("Server starting on http://localhost:5000")
    app.run(port=5000)
