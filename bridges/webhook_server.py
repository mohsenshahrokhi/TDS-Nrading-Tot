from flask import Flask, request, jsonify
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/webhook/nds', methods=['POST'])
def webhook_nds():
    try:
        data = request.json
        logging.info(f"📡 سیگنال NDS دریافت شد: {data}")
        
        return jsonify({
            "status": "success",
            "message": "سیگنال پردازش شد",
            "signal": data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "running",
        "service": "NDS Trading Bot",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 NDS Webhook Server Started!")
    print("📍 آدرس: http://localhost:5000")
    print("🔗 وب‌هوک: http://localhost:5000/webhook/nds")
    app.run(host='0.0.0.0', port=5000, debug=True)
