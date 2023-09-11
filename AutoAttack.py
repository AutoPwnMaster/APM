# build_connection.py (Temporary)

from subprocess import call  # 呼叫 Bash 庫

from pymetasploit3.msfrpc import MsfRpcClient  # 建立 API 客戶端


class Auto_Attack:

    # 當 class 被建立(須帶入一個參數)時，自動執行
    def __init__(self, password) -> None:
        self.password = password

    def Build_Server(self):
        call(['/bin/bash', './build_server.sh', self.password])
        # 相當於執行 /bin/bash ./build_server.sh $password

    def Connection(self):
        try:
            self.client = MsfRpcClient(self.password, port=55553, ssl=True)  # 建立客戶端
            self.console_id = self.client.consoles.console().cid  # 控制 ID
            self.console = self.client.consoles.console(self.console_id)  # 控制器
            print("Connection success !!!")
        except:
            print("Connection error")
            # haha
