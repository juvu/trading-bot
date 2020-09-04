import websocket, json
from configparser import ConfigParser

class AlpacaStream:
    def __init__(self,key_id,secret_key,symbols,log=False):
        self.key_id = key_id
        self.secret_key = secret_key
        self.symbols = symbols
        self.log = log
        self.socket = "wss://data.alpaca.markets/stream"
        self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_message=self.on_message, on_close=self.on_close)

    def start(self):
        self.ws.run_forever()

    # Open a socket, authenticate, and stream
    def on_open(self):
        print("Open")
        auth_data = {
            "action": "authenticate",
            "data": {
                "key_id": self.key_id,
                "secret_key": self.secret_key
            }
        }
        self.ws.send(json.dumps(auth_data))

        listen_message = {
            "action": "listen",
            "data": {
                "streams": self.symbols
            }
        }
        self.ws.send(json.dumps(listen_message))


    # On messange handler
    def on_message(self,message):
        print(message)
        data = json.loads(message)
        if 'error' in data["data"].keys():
            self.ws.close()
            print(data["data"]["error"])
        # else:
        #     if self.log: 
        #         if data["stream"] not in ["authorization","listening"]:
        #             self.writeLog(data["stream"],data["data"])
            

    # Close socket handler
    def on_close(self,ws):
        print("Closed")
    
    # s,e,T,v,av,op,vw,o,c,h,l,a
    def writeLog(self,name,data):
        fd = open(name+".txt","a+")
        fd.write("%ld,%ld,%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n" % 
        (data['s'],data['e'],data['T'],data['v'],data['av'],data['op'],data['vw'],data['o'],data['c'],data['h'],data['l'],data['a']))
        fd.close()

parser = ConfigParser()
parser.read("config.ini")
key_id = parser.get("auth","key_id")
secret_key = parser.get("auth","secret_key")
symbols = ["alpacadatav1/T.AAPL","alpacadatav1/T.MSFT","alpacadatav1/T.TSLA","alpacadatav1/T.BA"]

stream = AlpacaStream(key_id,secret_key,symbols,log=True)
stream.start()