from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

SECRET_KEY = "buraya-gizli-anahtarinizi-yazin"

@app.route('/')
def home():
    return "TradingView Webhook Bot Çalışıyor! ✅"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        if data.get('secret') != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        
        log_message = f"\n{'='*50}\n"
        log_message += f"Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        log_message += f"Gelen Sinyal: {json.dumps(data, indent=2)}\n"
        print(log_message)
        
        action = data.get('action')
        symbol = data.get('symbol')
        quantity = data.get('quantity', 0.001)
        
        result = {
            "type": action.upper(),
            "symbol": symbol,
            "quantity": quantity,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"İşlem: {json.dumps(result, indent=2)}")
        
        return jsonify({
            "status": "success",
            "message": "İşlem alındı",
            "data": result
        }), 200
        
    except Exception as e:
        print(f"HATA: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
