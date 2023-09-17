from pymetasploit3.msfrpc import MsfRpcClient

if __name__ == '__main__':
    client = MsfRpcClient("salt", port=55553, ssl=True)
    print(client.sessions.list)
    # for i in client.sessions.list.keys():
    #     client.sessions.session(i).stop()
    module = client.modules.use('exploit', 'windows/smb/smb_delivery')

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
    # print(output)
    # print("=None, ".join(output) + '=None')
