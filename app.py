from flask import Flask, jsonify, request
import ccxt
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# This is the function from your script, now wrapped in an API endpoint
def get_coinbase_ohlcv(symbol, timeframe, limit=100):
    try:
        exchange = ccxt.coinbasepro()
        exchange.load_markets()
        
        if symbol not in exchange.markets:
            return None, f"Symbol '{symbol}' not found on Coinbase."
        
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        if not ohlcv:
            return None, f"No data found for {symbol} with timeframe {timeframe}."

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Convert DataFrame to a list of lists for JSON serialization
        data_list = df.values.tolist()
        return data_list, None

    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# The API route that your Node.js app will call
@app.route('/api/data/candles', methods=['GET'])
def get_candles_endpoint():
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe')
    limit = request.args.get('limit', type=int)

    if not all([symbol, timeframe, limit]):
        return jsonify({"success": False, "message": "Missing required parameters: symbol, timeframe, or limit"}), 400

    candles, error = get_coinbase_ohlcv(symbol, timeframe, limit)
    
    if error:
        return jsonify({"success": False, "message": error}), 500
    
    return jsonify({"success": True, "data": candles})

if __name__ == '__main__':
    # You can run this with a production-ready server like Gunicorn in production
    app.run(host='0.0.0.0', port=5001)
