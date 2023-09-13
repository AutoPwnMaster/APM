from enum import Enum


class Payloads(str, Enum):
    BIND_TCP_RC4 = 'windows/x64/meterpreter/bind_tcp_rc4'
    BIND_TCP_UUID = 'windows/x64/meterpreter/bind_tcp_uuid'
    REVERSE_TCP_RC4 = 'windows/x64/meterpreter/reverse_tcp_rc4'
    REVERSE_TCP_UUID = 'windows/x64/meterpreter/reverse_tcp_uuid'
    BIND_NAMED_PIPE = 'windows/x64/meterpreter/bind_named_pipe'
    BIND_TCP = 'windows/x64/meterpreter/bind_tcp'
    BIND_IPV6_TCP = 'windows/x64/meterpreter/bind_ipv6_tcp'
    BIND_IPV6_TCP_UUID = 'windows/x64/meterpreter/bind_ipv6_tcp_uuid'
    REVERSE_WINHTTP = 'windows/x64/meterpreter/reverse_winhttp'
    REVERSE_HTTPS = 'windows/x64/meterpreter/reverse_https'
    REVERSE_HTTP = 'windows/x64/meterpreter/reverse_http'
    REVERSE_WINHTTPS = 'windows/x64/meterpreter/reverse_winhttps'
    REVERSE_NAMED_PIPE = 'windows/x64/meterpreter/reverse_named_pipe'
    REVERSE_TCP = 'windows/x64/meterpreter/reverse_tcp'
    METERPRETER_BIND_NAMED_PIPE = 'windows/x64/meterpreter_bind_named_pipe'
    METERPRETER_BIND_TCP = 'windows/x64/meterpreter_bind_tcp'
    METERPRETER_REVERSE_HTTP = 'windows/x64/meterpreter_reverse_http'
    METERPRETER_REVERSE_HTTPS = 'windows/x64/meterpreter_reverse_https'
    METERPRETER_REVERSE_IPV6_TCP = 'windows/x64/meterpreter_reverse_ipv6_tcp'
    METERPRETER_REVERSE_TCP = 'windows/x64/meterpreter_reverse_tcp'