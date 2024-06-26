#https://pypi.org/project/websocket_client/
import websocket, json

def on_message(ws, message):
    print('HEEEEEEEEEEEEEEREEEEEEEEEEE IS THE MESSSSSSSSSSSSSSSSSSSSAGEEEEEEEEEEEEEEEEEEE')
    print('*'*60)
    response = json.loads(message)
    # base = response['data'][0]
    # print(response['data'][0]['s'])
    print(response)
    print('*'*60)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cc4f982ad3ia9srm3fog",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()