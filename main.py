from datetime import datetime
import json
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket
from time import time

class ContextHost:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        contextEnd = False

        print(f"[{datetime.now()}] Server opened.")
        while True:
            if (contextEnd):
                break

            buff = ""
            client, addr = self.server_socket.accept()
            print(f"[{datetime.now()}] Client Connected.")

            while True:
                recv_bytes = client.recv(1024)

                if (len(recv_bytes) == 0):
                    print(f"[{datetime.now()}] Client Disconnected.")
                    break

                recv = recv_bytes.decode("utf-8")

                buff += recv
                index = buff.find("\r\n")

                if (index == -1):
                    continue
                else:
                    src = buff[:index]
                    buff = buff[index+2:]

                    try:
                        item = json.loads(src)
                        operate_type = item["type"]

                        print(f"[{datetime.now()}] Call Request, Type : {operate_type}")

                        if (operate_type == "terminate"):
                            print(f"[{datetime.now()}] Terminate.")
                            contextEnd = True
                            break
                        elif (operate_type == "execute"):
                            func_src = item["source"]
                            func_name = item["name"]

                            executes = item["executes"]
                            resultset = list()

                            print(f"[{datetime.now()}] Execute instructions : {len(executes)}")
                            
                            for execute in executes:
                                func_arg = execute["arg"]

                                stt = time()
                                exec(func_src)
                                execute_src = f"{func_name}(None, func_arg)"
                                res = eval(execute_src)
                                resultset.append(res)

                                edd = time()

                                #print(f"[{datetime.now()}] Done. elapsed : {(edd-stt)*1000}ms")
                            
                            res_json = json.dumps(resultset) + "\r\n"
                            client.send(res_json.encode())
                                
                    except Exception as e:
                        client.send((str(e) + "\r\n").encode())

host = ContextHost("0.0.0.0", 8888)
host.run()