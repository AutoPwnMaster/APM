from socket import socket, AF_INET, SOCK_DGRAM
import re  # re libary
from subprocess import check_output  # 呼叫 Bash 庫

def get_ipv4():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip


def __Get_NetBios(Target_ip: str) -> str:
    try:
        output = check_output(f"nmblookup -A {Target_ip}", shell=True, text=True)  # try nmblookup
        output = output.split('\n')[1][1:]
        # first one is "Looking up status of {Target_ip}",  so use [1]
        # Second one is target , first of it is "\t",  so use [1:]

        index = output.rfind("<00>")  # find last <00> index
        return output[:index].strip()  # delet space
    except:
        return None


def __Get_Printer(NetBios: str, Target_ip: str) -> list:
    outputs = check_output(f"smbclient -L \\\\\\{NetBios} -I {Target_ip} -U \"[%]\"", shell=True, text=True) \
                  .split("\n")[3:]
    # try smbclient user and password is empty
    # first ~ third no use

    filter_outputs = []
    for output in outputs:
        # find the string that startwith '\t'
        # if not, means not our target after this
        if output.startswith('\t'):
            filter_outputs.append(output)
        else:
            break

    pattern = r'^\s*([^\s]+)\s+Printer'
    matches = []

    for data in filter_outputs:  # find the printer
        find_printer = re.findall(pattern, data)
        if not len(find_printer) == 0:
            matches.append("".join(find_printer))

    return matches


def Get_Printer(Target_ip):
    NetBios = __Get_NetBios(Target_ip)
    if not NetBios == None:
        return __Get_Printer(NetBios, Target_ip)
    else:
        return None

