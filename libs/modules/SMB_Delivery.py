from pymetasploit3.msfrpc import MsfRpcClient

from libs.modules.Basic import Basic
from libs.modules.list.Payload_List import REVERSE_TCP


class SMB_Delivery(Basic):
    __module_options: list[str] = ['SRVHOST', 'SRVPORT', 'SMBDomain', 'Powershell__persist',
                                   'Powershell__prepend_protections_bypass', 'Powershell__strip_comments',
                                   'Powershell__strip_whitespace', 'Powershell__sub_vars', 'Powershell__sub_funcs',
                                   'Powershell__exec_in_place', 'Powershell__exec_rc4', 'Powershell__remove_comspec',
                                   'Powershell__noninteractive', 'Powershell__encode_final_payload',
                                   'Powershell__encode_inner_payload', 'Powershell__wrap_double_quotes',
                                   'Powershell__no_equals', 'Powershell__method']

    def __init__(self, rpc: MsfRpcClient, /,
                 # payload module
                 payload=REVERSE_TCP,

                 # module options
                 Powershell__encode_final_payload=None, Powershell__encode_inner_payload=None,
                 Powershell__exec_in_place=None, Powershell__exec_rc4=None, Powershell__method=None,
                 Powershell__no_equals=None, Powershell__noninteractive=None, Powershell__persist=None,
                 Powershell__prepend_protections_bypass=None, Powershell__remove_comspec=None,
                 Powershell__strip_comments=None, Powershell__strip_whitespace=None, Powershell__sub_funcs=None,
                 Powershell__sub_vars=None, Powershell__wrap_double_quotes=None, SMBDomain=None, SRVHOST=None,
                 SRVPORT=None,

                 # payload options
                 AutoLoadStdapi=None, AutoSystemInfo=None, AutoUnhookProcess=None, EXITFUNC=None,
                 EnableUnicodeEncoding=None, LPORT=None, PayloadUUIDTracking=None, PingbackRetries=None,
                 PingbackSleep=None, PrependMigrate=None, ReverseAllowProxy=None, ReverseListenerThreaded=None
                 ):
        """

        :param rpc:
        :param payload:
        :param Powershell__encode_final_payload:
        :param Powershell__encode_inner_payload:
        :param Powershell__exec_in_place:
        :param Powershell__exec_rc4:
        :param Powershell__method:
        :param Powershell__no_equals:
        :param Powershell__noninteractive:
        :param Powershell__persist:
        :param Powershell__prepend_protections_bypass:
        :param Powershell__remove_comspec:
        :param Powershell__strip_comments:
        :param Powershell__strip_whitespace:
        :param Powershell__sub_funcs:
        :param Powershell__sub_vars:
        :param Powershell__wrap_double_quotes:
        :param SMBDomain:
        :param SRVHOST:
        :param SRVPORT:
        :param AutoLoadStdapi:
        :param AutoSystemInfo:
        :param AutoUnhookProcess:
        :param EXITFUNC:
        :param EnableUnicodeEncoding:
        :param LPORT:
        :param PayloadUUIDTracking:
        :param PingbackRetries:
        :param PingbackSleep:
        :param PrependMigrate:
        :param ReverseAllowProxy:
        :param ReverseListenerThreaded:
        """

        super().__init__(rpc, 'windows/smb/smb_delivery', payload.name)

        for i in self.__module_options:
            if locals().get(i) is not None:
                self.set_module_option(i, locals().get(i))

        for i in payload.options:
            if locals().get(i) is not None:
                self.set_payload_option(i, locals().get(i))

    async def run(self):
        response = await super()._run()
        await self.trigger('on_read', response)

    def check_session(self, str):
        # TODO: 檢查連是否成功
        pass
