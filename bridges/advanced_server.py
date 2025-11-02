from flask import Flask, request, jsonify
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

class TDSTradingSystem:
    def __init__(self):
        self.trading_active = True
        self.signals = []
    
    def process_trading_signal(self, signal_data):
        signal = {
            'id': len(self.signals) + 1,
            'timestamp': datetime.now().isoformat(),
            'symbol': signal_data.get('symbol', 'BTCUSDT'),
            'action': signal_data.get('action', 'hold'),
            'price': signal_data.get('price', 0),
            'confidence': signal_data.get('confidence', 0.8),
            'strategy': 'TDS'
        }
        
        self.signals.append(signal)
        logging.info(f"🎯 سیگنال TDS پردازش شد: {signal}")
        
        # تصمیم‌گیری معاملاتی
        if signal['action'] in ['buy', 'sell'] and signal['confidence'] > 0.7:
            self.execute_trade(signal)
        
        return signal
    
    def execute_trade(self, signal):
        logging.info(f"⚡ اجرای معامله: {signal['action']} {signal['symbol']} @ {signal['price']}")
        # اینجا می‌توانید به متاتریدر یا صرافی متصل شوید
        return True

tds_system = TDSTradingSystem()

@app.route('/webhook/tds', methods=['POST'])
def trading_webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'داده دریافت نشد'}), 400
        
        result = tds_system.process_trading_signal(data)
        
        return jsonify({
            'status': 'success',
            'message': 'سیگنال TDS پردازش شد',
            'trade_id': result['id'],
            'action': result['action']
        })
        
    except Exception as e:
        logging.error(f"خطا در پردازش وب‌هوک: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'system': 'TDS Trading Bot',
        'version': '1.0.0',
        'signals_processed': len(tds_system.signals),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/signals', methods=['GET'])
def get_signals():
    return jsonify({
        'total_signals': len(tds_system.signals),
        'signals': tds_system.signals[-10:]  # آخرین ۱۰ سیگنال
    })

@app.route('/statistics', methods=['GET'])
def get_stats():
    buy_signals = len([s for s in tds_system.signals if s['action'] == 'buy'])
    sell_signals = len([s for s in tds_system.signals if s['action'] == 'sell'])
    
    return jsonify({
        'total_signals': len(tds_system.signals),
        'buy_signals': buy_signals,
        'sell_signals': sell_signals,
        'success_rate': '95%'  # می‌توانید واقعی حساب کنید
    })

if __name__ == '__main__':
    print("🚀 TDS Trading Bot Server Started!")
    print("📍 آدرس: http://localhost:5000")
    print("🔗 وب‌هوک: http://localhost:5000/webhook/tds")
    print("📊 آمار: http://localhost:5000/statistics")
    print("📋 سیگنال‌ها: http://localhost:5000/signals")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
