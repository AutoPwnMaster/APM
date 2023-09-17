from pymetasploit3.msfrpc import MsfRpcClient
from libs.modules.Module_List import Modules




if __name__ == '__main__':
    client = MsfRpcClient("salt", port=55553, ssl=True)
    module = client.modules.use('exploit', Modules.MS10_061_SPOOLSS)

    options: list[str] = module.options
    options.sort()
    output: list[str] = []
    for i in options:
        if i == 'CheckModule':
            continue

        info: dict[str, str] = module.optioninfo(i)
        if ('default' in info.keys()) or (info['required'] is False):
            output.append(i)
        else:
            print(i)
    print(output)
    print("=None, ".join(output) + '=None')
