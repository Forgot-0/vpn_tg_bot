import base64
from enum import Enum
import time
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import random
import string
from urllib.parse import quote, urlencode

class Protocols(str, Enum):
    VMESS = 'vmess'
    VLESS = 'vless'
    TROJAN = 'trojan'
    SHADOWSOCKS = 'shadowsocks'
    DOKODEMO = 'dokodemo-door'
    SOCKS = 'socks'
    HTTP = 'http'
    WIREGUARD = 'wireguard'
    FREEDOM = 'freedom'
    BLACKHOLE = 'blackhole'
    DNS = 'dns'

class SSMethods(str, Enum):
    AES_256_GCM = 'aes-256-gcm'
    AES_128_GCM = 'aes-128-gcm'
    CHACHA20_POLY1305 = 'chacha20-poly1305'
    CHACHA20_IETF_POLY1305 = 'chacha20-ietf-poly1305'
    XCHACHA20_POLY1305 = 'xchacha20-poly1305'
    XCHACHA20_IETF_POLY1305 = 'xchacha20-ietf-poly1305'
    BLAKE3_AES_128_GCM = '2022-blake3-aes-128-gcm'
    BLAKE3_AES_256_GCM = '2022-blake3-aes-256-gcm'
    BLAKE3_CHACHA20_POLY1305 = '2022-blake3-chacha20-poly1305'

class TLSFlowControl(str, Enum):
    VISION = "xtls-rprx-vision"
    VISION_UDP443 = "xtls-rprx-vision-udp443"

class TLSVersion(str, Enum):
    TLS10 = "1.0"
    TLS11 = "1.1"
    TLS12 = "1.2"
    TLS13 = "1.3"

class TLSCipher(str, Enum):
    AES_128_GCM = "TLS_AES_128_GCM_SHA256"
    AES_256_GCM = "TLS_AES_256_GCM_SHA384"
    CHACHA20_POLY1305 = "TLS_CHACHA20_POLY1305_SHA256"
    ECDHE_ECDSA_AES_128_CBC = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
    ECDHE_ECDSA_AES_256_CBC = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"
    ECDHE_RSA_AES_128_CBC = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"
    ECDHE_RSA_AES_256_CBC = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"
    ECDHE_ECDSA_AES_128_GCM = "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"
    ECDHE_ECDSA_AES_256_GCM = "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
    ECDHE_RSA_AES_128_GCM = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
    ECDHE_RSA_AES_256_GCM = "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
    ECDHE_ECDSA_CHACHA20_POLY1305 = "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256"
    ECDHE_RSA_CHACHA20_POLY1305 = "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"

class UTLSFingerprint(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    IOS = "ios"
    ANDROID = "android"
    EDGE = "edge"
    _360 = "360"
    QQ = "qq"
    RANDOM = "random"
    RANDOMIZED = "randomized"
    UNSAFE = "unsafe"

class ALPNOption(str, Enum):
    H3 = "h3"
    H2 = "h2"
    HTTP1 = "http/1.1"

class SniffingOption(str, Enum):
    HTTP = "http"
    TLS = "tls"
    QUIC = "quic"
    FAKEDNS = "fakedns"

class UsageOption(str, Enum):
    ENCIPHERMENT = "encipherment"
    VERIFY = "verify"
    ISSUE = "issue"

class DomainStrategy(str, Enum):
    AS_IS = "AsIs"
    USE_IP = "UseIP"
    USE_IPV6V4 = "UseIPv6v4"
    USE_IPV6 = "UseIPv6"
    USE_IPV4V6 = "UseIPv4v6"
    USE_IPV4 = "UseIPv4"
    FORCE_IP = "ForceIP"
    FORCE_IPV6V4 = "ForceIPv6v4"
    FORCE_IPV6 = "ForceIPv6"
    FORCE_IPV4V6 = "ForceIPv4v6"
    FORCE_IPV4 = "ForceIPv4"

class TCPCongestion(str, Enum):
    BBR = "bbr"
    CUBIC = "cubic"
    RENO = "reno"

class UsersSecurity(str, Enum):
    AES_128_GCM = "aes-128-gcm"
    CHACHA20_POLY1305 = "chacha20-poly1305"
    AUTO = "auto"
    NONE = "none"
    ZERO = "zero"

class ModeOption(str, Enum):
    AUTO = "auto"
    PACKET_UP = "packet-up"
    STREAM_UP = "stream-up"
    STREAM_ONE = "stream-one"

class RandomUtil:
    @staticmethod
    def random_int_range(start: int, end: int) -> int:
        return random.randint(start, end)
    @staticmethod
    def random_seq(length: int) -> str:
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @staticmethod
    def random_short_ids(count: int = 4) -> List[str]:
        return [RandomUtil.random_seq(8) for _ in range(count)]

@dataclass
class XrayCommonClass(ABC):
    @staticmethod
    def to_json_array(arr: List[Any]) -> List[Dict[str, Any]]:
        return [obj.to_json() for obj in arr]

    @classmethod
    @abstractmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> Any:
        """Must be implemented by subclasses"""
        raise NotImplementedError

    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        """Must be implemented by subclasses"""
        raise NotImplementedError

    def to_string(self, format_output: bool = True) -> str:
        if format_output:
            return json.dumps(self.to_json(), indent=2)
        return json.dumps(self.to_json())

    @staticmethod
    def to_headers(v2_headers: Optional[Dict[str, Any]]) -> List[Dict[str, str]]:
        new_headers = []
        if v2_headers:
            for key, values in v2_headers.items():
                if isinstance(values, str):
                    new_headers.append({"name": key, "value": values})
                else:
                    for value in values:
                        new_headers.append({"name": key, "value": value})
        return new_headers

    @staticmethod
    def to_v2_headers(headers: List[Dict[str, str]], arr: bool = True) -> Dict[str, Any]:
        v2_headers = {}
        if not headers:
            return v2_headers
            
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if not name or not value:
                continue
            if name not in v2_headers:
                v2_headers[name] = [value] if arr else value
            else:
                if arr:
                    v2_headers[name].append(value)
                else:
                    v2_headers[name] = value
        return v2_headers

@dataclass
class TcpRequest(XrayCommonClass):
    version: str = "1.1"
    method: str = "GET"
    path: List[str] = field(default_factory=lambda: ["/"])
    headers: List[Dict[str, str]] = field(default_factory=list)

    def add_path(self, path: str) -> None:
        self.path.append(path)

    def remove_path(self, index: int) -> None:
        self.path.pop(index)

    def add_header(self, name: str, value: str) -> None:
        self.headers.append({"name": name, "value": value})

    def remove_header(self, index: int) -> None:
        self.headers.pop(index)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'TcpRequest':
        if json_data is None:
            json_data = {}
        return cls(
            version=json_data.get("version", "1.1"),
            method=json_data.get("method", "GET"),
            path=json_data.get("path", ["/"]),
            headers=XrayCommonClass.to_headers(json_data.get("headers", {}))
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "method": self.method,
            "path": self.path.copy(),
            "headers": XrayCommonClass.to_v2_headers(self.headers)
        }

@dataclass
class TcpResponse(XrayCommonClass):
    version: str = "1.1"
    status: str = "200"
    reason: str = "OK"
    headers: List[Dict[str, str]] = field(default_factory=list)

    def add_header(self, name: str, value: str) -> None:
        self.headers.append({"name": name, "value": value})

    def remove_header(self, index: int) -> None:
        self.headers.pop(index)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'TcpResponse':
        if json_data is None:
            json_data = {}
        return cls(
            version=json_data.get("version", "1.1"),
            status=json_data.get("status", "200"),
            reason=json_data.get("reason", "OK"),
            headers=XrayCommonClass.to_headers(json_data.get("headers", {}))
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status,
            "reason": self.reason,
            "headers": XrayCommonClass.to_v2_headers(self.headers)
        }

@dataclass
class TcpStreamSettings(XrayCommonClass):
    accept_proxy_protocol: bool = False
    type: str = "none"
    request: TcpRequest = field(default_factory=TcpRequest)
    response: TcpResponse = field(default_factory=TcpResponse)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'TcpStreamSettings':
        if json_data is None:
            json_data = {}
        header = json_data.get("header", {})
        return cls(
            accept_proxy_protocol=json_data.get("acceptProxyProtocol", False),
            type=header.get("type", "none"),
            request=TcpRequest.from_json(header.get("request")),
            response=TcpResponse.from_json(header.get("response"))
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "acceptProxyProtocol": self.accept_proxy_protocol,
            "header": {
                "type": self.type,
                "request": self.request.to_json() if self.type == "http" else None,
                "response": self.response.to_json() if self.type == "http" else None,
            }
        }

@dataclass
class KcpStreamSettings(XrayCommonClass):
    mtu: int = 1350
    tti: int = 50
    up_cap: int = 5
    down_cap: int = 20
    congestion: bool = False
    read_buffer: int = 2
    write_buffer: int = 2
    type: str = "none"
    seed: str = field(default_factory=lambda: RandomUtil.random_seq(10))

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'KcpStreamSettings':
        if json_data is None:
            json_data = {}
        return cls(
            mtu=json_data.get("mtu", 1350),
            tti=json_data.get("tti", 50),
            up_cap=json_data.get("uplinkCapacity", 5),
            down_cap=json_data.get("downlinkCapacity", 20),
            congestion=json_data.get("congestion", False),
            read_buffer=json_data.get("readBufferSize", 2),
            write_buffer=json_data.get("writeBufferSize", 2),
            type=json_data.get("header", {}).get("type", "none"),
            seed=json_data.get("seed", RandomUtil.random_seq(10))
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "mtu": self.mtu,
            "tti": self.tti,
            "uplinkCapacity": self.up_cap,
            "downlinkCapacity": self.down_cap,
            "congestion": self.congestion,
            "readBufferSize": self.read_buffer,
            "writeBufferSize": self.write_buffer,
            "header": {
                "type": self.type,
            },
            "seed": self.seed,
        }

@dataclass
class WsStreamSettings(XrayCommonClass):
    accept_proxy_protocol: bool = False
    path: str = "/"
    host: str = ""
    headers: List[Dict[str, str]] = field(default_factory=list)
    heartbeat_period: int = 0

    def add_header(self, name: str, value: str) -> None:
        self.headers.append({"name": name, "value": value})

    def remove_header(self, index: int) -> None:
        self.headers.pop(index)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'WsStreamSettings':
        if json_data is None:
            json_data = {}
        return cls(
            accept_proxy_protocol=json_data.get("acceptProxyProtocol", False),
            path=json_data.get("path", "/"),
            host=json_data.get("host", ""),
            headers=XrayCommonClass.to_headers(json_data.get("headers", {})),
            heartbeat_period=json_data.get("heartbeatPeriod", 0)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "acceptProxyProtocol": self.accept_proxy_protocol,
            "path": self.path,
            "host": self.host,
            "headers": XrayCommonClass.to_v2_headers(self.headers, False),
            "heartbeatPeriod": self.heartbeat_period,
        }

@dataclass
class GrpcStreamSettings(XrayCommonClass):
    service_name: str = ""
    authority: str = ""
    multi_mode: bool = False

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'GrpcStreamSettings':
        if json_data is None:
            json_data = {}
        return cls(
            service_name=json_data.get("serviceName", ""),
            authority=json_data.get("authority", ""),
            multi_mode=json_data.get("multiMode", False)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "serviceName": self.service_name,
            "authority": self.authority,
            "multiMode": self.multi_mode,
        }

@dataclass
class HTTPUpgradeStreamSettings(XrayCommonClass):
    accept_proxy_protocol: bool = False
    path: str = "/"
    host: str = ""
    headers: List[Dict[str, str]] = field(default_factory=list)

    def add_header(self, name: str, value: str) -> None:
        self.headers.append({"name": name, "value": value})

    def remove_header(self, index: int) -> None:
        self.headers.pop(index)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'HTTPUpgradeStreamSettings':
        if json_data is None:
            json_data = {}
        return cls(
            accept_proxy_protocol=json_data.get("acceptProxyProtocol", False),
            path=json_data.get("path", "/"),
            host=json_data.get("host", ""),
            headers=XrayCommonClass.to_headers(json_data.get("headers", {}))
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "acceptProxyProtocol": self.accept_proxy_protocol,
            "path": self.path,
            "host": self.host,
            "headers": XrayCommonClass.to_v2_headers(self.headers, False),
        }

@dataclass
class xHTTPStreamSettings(XrayCommonClass):
    path: str = "/"
    host: str = ""
    headers: List[Dict[str, str]] = field(default_factory=list)
    sc_max_buffered_posts: int = 30
    sc_max_each_post_bytes: str = "1000000"
    no_sse_header: bool = False
    x_padding_bytes: str = "100-1000"
    mode: str = ModeOption.AUTO

    def add_header(self, name: str, value: str) -> None:
        self.headers.append({"name": name, "value": value})

    def remove_header(self, index: int) -> None:
        self.headers.pop(index)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'xHTTPStreamSettings':
        if json_data is None:
            json_data = {}
        return cls(
            path=json_data.get("path", "/"),
            host=json_data.get("host", ""),
            headers=XrayCommonClass.to_headers(json_data.get("headers", {})),
            sc_max_buffered_posts=json_data.get("scMaxBufferedPosts", 30),
            sc_max_each_post_bytes=json_data.get("scMaxEachPostBytes", "1000000"),
            no_sse_header=json_data.get("noSSEHeader", False),
            x_padding_bytes=json_data.get("xPaddingBytes", "100-1000"),
            mode=json_data.get("mode", ModeOption.AUTO)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "host": self.host,
            "headers": XrayCommonClass.to_v2_headers(self.headers, False),
            "scMaxBufferedPosts": self.sc_max_buffered_posts,
            "scMaxEachPostBytes": self.sc_max_each_post_bytes,
            "noSSEHeader": self.no_sse_header,
            "xPaddingBytes": self.x_padding_bytes,
            "mode": self.mode,
        }

@dataclass
class TlsCert(XrayCommonClass):
    use_file: bool = True
    cert_file: str = ""
    key_file: str = ""
    cert: str = ""
    key: str = ""
    ocsp_stapling: int = 3600
    one_time_loading: bool = False
    usage: str = UsageOption.ENCIPHERMENT
    build_chain: bool = False

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'TlsCert':
        if json_data is None:
            json_data = {}

        if "certificateFile" in json_data and "keyFile" in json_data:
            return cls(
                use_file=True,
                cert_file=json_data.get("certificateFile", ""),
                key_file=json_data.get("keyFile", ""),
                ocsp_stapling=json_data.get("ocspStapling", 3600),
                one_time_loading=json_data.get("oneTimeLoading", False),
                usage=json_data.get("usage", UsageOption.ENCIPHERMENT),
                build_chain=json_data.get("buildChain", False),
            )
        else:
            return cls(
                use_file=False,
                cert='\n'.join(json_data.get("certificate", [])) if isinstance(json_data.get("certificate"), list) else json_data.get("certificate", ""),
                key='\n'.join(json_data.get("key", [])) if isinstance(json_data.get("key"), list) else json_data.get("key", ""),
                ocsp_stapling=json_data.get("ocspStapling", 3600),
                one_time_loading=json_data.get("oneTimeLoading", False),
                usage=json_data.get("usage", UsageOption.ENCIPHERMENT),
                build_chain=json_data.get("buildChain", False),
            )

    def to_json(self) -> Dict[str, Any]:
        if self.use_file:
            return {
                "certificateFile": self.cert_file,
                "keyFile": self.key_file,
                "ocspStapling": self.ocsp_stapling,
                "oneTimeLoading": self.one_time_loading,
                "usage": self.usage,
                "buildChain": self.build_chain,
            }
        else:
            return {
                "certificate": self.cert.split('\n') if '\n' in self.cert else self.cert,
                "key": self.key.split('\n') if '\n' in self.key else self.key,
                "ocspStapling": self.ocsp_stapling,
                "oneTimeLoading": self.one_time_loading,
                "usage": self.usage,
                "buildChain": self.build_chain,
            }

@dataclass
class TlsSettings(XrayCommonClass):
    allow_insecure: bool = False
    fingerprint: str = UTLSFingerprint.CHROME

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'TlsSettings':
        if json_data is None:
            json_data = {}
        return cls(
            allow_insecure=json_data.get("allowInsecure", False),
            fingerprint=json_data.get("fingerprint", UTLSFingerprint.CHROME),
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "allowInsecure": self.allow_insecure,
            "fingerprint": self.fingerprint,
        }

@dataclass
class TlsStreamSettings(XrayCommonClass):
    sni: str = ""
    min_version: str = TLSVersion.TLS12
    max_version: str = TLSVersion.TLS13
    cipher_suites: str = ""
    reject_unknown_sni: bool = False
    disable_system_root: bool = False
    enable_session_resumption: bool = False
    certs: List[TlsCert] = field(default_factory=lambda: [TlsCert()])
    alpn: List[str] = field(default_factory=lambda: [ALPNOption.H3, ALPNOption.H2, ALPNOption.HTTP1])
    settings: TlsSettings = field(default_factory=TlsSettings)

    def add_cert(self) -> None:
        self.certs.append(TlsCert())

    def remove_cert(self, index: int) -> None:
        self.certs.pop(index)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'TlsStreamSettings':
        if json_data is None:
            json_data = {}
            
        certs = [TlsCert.from_json(cert) for cert in json_data.get("certificates", [])] if json_data.get("certificates") else [TlsCert()]
        settings = TlsSettings.from_json(json_data.get("settings", {})) if json_data.get("settings") else TlsSettings()
        
        return cls(
            sni=json_data.get("serverName", ""),
            min_version=json_data.get("minVersion", TLSVersion.TLS12),
            max_version=json_data.get("maxVersion", TLSVersion.TLS13),
            cipher_suites=json_data.get("cipherSuites", ""),
            reject_unknown_sni=json_data.get("rejectUnknownSni", False),
            disable_system_root=json_data.get("disableSystemRoot", False),
            enable_session_resumption=json_data.get("enableSessionResumption", False),
            certs=certs,
            alpn=json_data.get("alpn", [ALPNOption.H3, ALPNOption.H2, ALPNOption.HTTP1]),
            settings=settings
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "serverName": self.sni,
            "minVersion": self.min_version,
            "maxVersion": self.max_version,
            "cipherSuites": self.cipher_suites,
            "rejectUnknownSni": self.reject_unknown_sni,
            "disableSystemRoot": self.disable_system_root,
            "enableSessionResumption": self.enable_session_resumption,
            "certificates": XrayCommonClass.to_json_array(self.certs),
            "alpn": self.alpn,
            "settings": self.settings.to_json(),
        }

@dataclass
class RealitySettings(XrayCommonClass):
    public_key: str = ""
    fingerprint: str = UTLSFingerprint.CHROME
    server_name: str = ""
    spider_x: str = "/"

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'RealitySettings':
        if json_data is None:
            json_data = {}
        return cls(
            public_key=json_data.get("publicKey", ""),
            fingerprint=json_data.get("fingerprint", UTLSFingerprint.CHROME),
            server_name=json_data.get("serverName", ""),
            spider_x=json_data.get("spiderX", "/")
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "publicKey": self.public_key,
            "fingerprint": self.fingerprint,
            "serverName": self.server_name,
            "spiderX": self.spider_x,
        }

@dataclass
class RealityStreamSettings(XrayCommonClass):
    show: bool = False
    xver: int = 0
    dest: str = "yahoo.com:443"
    server_names: str = "yahoo.com,www.yahoo.com"
    private_key: str = ""
    min_client: str = ""
    max_client: str = ""
    max_timediff: int = 0
    short_ids: List[str] = field(default_factory=RandomUtil.random_short_ids)
    settings: RealitySettings = field(default_factory=RealitySettings)

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'RealityStreamSettings':
        if json_data is None:
            json_data = {}

        server_names = json_data.get("serverNames", "yahoo.com,www.yahoo.com")
        if isinstance(server_names, list):
            server_names = ",".join(server_names)

        return cls(
            show=json_data.get("show", False),
            xver=json_data.get("xver", 0),
            dest=json_data.get("dest", "yahoo.com:443"),
            server_names=server_names,
            private_key=json_data.get("privateKey", ""),
            min_client=json_data.get("minClient", ""),
            max_client=json_data.get("maxClient", ""),
            max_timediff=json_data.get("maxTimeDiff", 0),
            short_ids=json_data.get("shortIds", RandomUtil.random_short_ids()),
            settings=RealitySettings.from_json(json_data.get("settings", {}))
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "show": self.show,
            "xver": self.xver,
            "dest": self.dest,
            "serverNames": self.server_names,
            "privateKey": self.private_key,
            "minClient": self.min_client,
            "maxClient": self.max_client,
            "maxTimeDiff": self.max_timediff,
            "shortIds": self.short_ids,
            "settings": self.settings.to_json(),
        }

@dataclass
class SockoptStreamSettings(XrayCommonClass):
    accept_proxy_protocol: bool = False
    tcp_fast_open: bool = False
    mark: int = 0
    tproxy: str = "off"
    tcp_mptcp: bool = False
    tcp_no_delay: bool = False
    domain_strategy: str = DomainStrategy.USE_IP
    tcp_max_seg: int = 1440
    dialer_proxy: str = ""
    tcp_keep_alive_interval: int = 0
    tcp_keep_alive_idle: int = 300
    tcp_user_timeout: int = 10000
    tcp_congestion: str = TCPCongestion.BBR
    v6_only: bool = False
    tcp_window_clamp: int = 600
    interface_name: str = ""

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'SockoptStreamSettings':
        if json_data is None or not json_data:
            return cls()
            
        return cls(
            accept_proxy_protocol=json_data.get("acceptProxyProtocol", False),
            tcp_fast_open=json_data.get("tcpFastOpen", False),
            mark=json_data.get("mark", 0),
            tproxy=json_data.get("tproxy", "off"),
            tcp_mptcp=json_data.get("tcpMptcp", False),
            tcp_no_delay=json_data.get("tcpNoDelay", False),
            domain_strategy=json_data.get("domainStrategy", DomainStrategy.USE_IP),
            tcp_max_seg=json_data.get("tcpMaxSeg", 1440),
            dialer_proxy=json_data.get("dialerProxy", ""),
            tcp_keep_alive_interval=json_data.get("tcpKeepAliveInterval", 0),
            tcp_keep_alive_idle=json_data.get("tcpKeepAliveIdle", 300),
            tcp_user_timeout=json_data.get("tcpUserTimeout", 10000),
            tcp_congestion=json_data.get("tcpcongestion", TCPCongestion.BBR),
            v6_only=json_data.get("V6Only", False),
            tcp_window_clamp=json_data.get("tcpWindowClamp", 600),
            interface_name=json_data.get("interface", "")
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "acceptProxyProtocol": self.accept_proxy_protocol,
            "tcpFastOpen": self.tcp_fast_open,
            "mark": self.mark,
            "tproxy": self.tproxy,
            "tcpMptcp": self.tcp_mptcp,
            "tcpNoDelay": self.tcp_no_delay,
            "domainStrategy": self.domain_strategy,
            "tcpMaxSeg": self.tcp_max_seg,
            "dialerProxy": self.dialer_proxy,
            "tcpKeepAliveInterval": self.tcp_keep_alive_interval,
            "tcpKeepAliveIdle": self.tcp_keep_alive_idle,
            "tcpUserTimeout": self.tcp_user_timeout,
            "tcpcongestion": self.tcp_congestion,
            "V6Only": self.v6_only,
            "tcpWindowClamp": self.tcp_window_clamp,
            "interface": self.interface_name
        }

@dataclass
class StreamSettings(XrayCommonClass):
    network: str = 'tcp'
    security: str = 'none'
    external_proxy: List[str] = field(default_factory=list)
    tls: TlsStreamSettings = field(default_factory=TlsStreamSettings)
    reality: RealityStreamSettings = field(default_factory=RealityStreamSettings)
    tcp: TcpStreamSettings = field(default_factory=TcpStreamSettings)
    kcp: KcpStreamSettings = field(default_factory=KcpStreamSettings)
    ws: WsStreamSettings = field(default_factory=WsStreamSettings)
    grpc: GrpcStreamSettings = field(default_factory=GrpcStreamSettings)
    httpupgrade: HTTPUpgradeStreamSettings = field(default_factory=HTTPUpgradeStreamSettings)
    xhttp: xHTTPStreamSettings = field(default_factory=xHTTPStreamSettings)
    sockopt: Optional[SockoptStreamSettings] = None

    @property
    def is_tls(self) -> bool:
        return self.security == "tls"

    @is_tls.setter
    def is_tls(self, value: bool) -> None:
        if value:
            self.security = "tls"
        else:
            self.security = "none"

    @property
    def is_reality(self) -> bool:
        return self.security == "reality"

    @is_reality.setter
    def is_reality(self, value: bool) -> None:
        if value:
            self.security = "reality"
        else:
            self.security = "none"

    @property
    def sockopt_switch(self) -> bool:
        return self.sockopt is not None

    @sockopt_switch.setter
    def sockopt_switch(self, value: bool) -> None:
        self.sockopt = SockoptStreamSettings() if value else None

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'StreamSettings':
        if json_data is None:
            json_data = {}
        
        return cls(
            network=json_data.get("network", "tcp"),
            security=json_data.get("security", "none"),
            external_proxy=json_data.get("externalProxy", []),
            tls=TlsStreamSettings.from_json(json_data.get("tlsSettings")),
            reality=RealityStreamSettings.from_json(json_data.get("realitySettings")),
            tcp=TcpStreamSettings.from_json(json_data.get("tcpSettings")),
            kcp=KcpStreamSettings.from_json(json_data.get("kcpSettings")),
            ws=WsStreamSettings.from_json(json_data.get("wsSettings")),
            grpc=GrpcStreamSettings.from_json(json_data.get("grpcSettings")),
            httpupgrade=HTTPUpgradeStreamSettings.from_json(json_data.get("httpupgradeSettings")),
            xhttp=xHTTPStreamSettings.from_json(json_data.get("xhttpSettings")),
            sockopt=SockoptStreamSettings.from_json(json_data.get("sockopt")) if json_data.get("sockopt") else None
        )

    def to_json(self) -> Dict[str, Any]:
        network = self.network
        return {
            "network": network,
            "security": self.security,
            "externalProxy": self.external_proxy,
            "tlsSettings": self.tls.to_json() if self.is_tls else None,
            "realitySettings": self.reality.to_json() if self.is_reality else None,
            "tcpSettings": self.tcp.to_json() if network == 'tcp' else None,
            "kcpSettings": self.kcp.to_json() if network == 'kcp' else None,
            "wsSettings": self.ws.to_json() if network == 'ws' else None,
            "grpcSettings": self.grpc.to_json() if network == 'grpc' else None,
            "httpupgradeSettings": self.httpupgrade.to_json() if network == 'httpupgrade' else None,
            "xhttpSettings": self.xhttp.to_json() if network == 'xhttp' else None,
            "sockopt": self.sockopt.to_json() if self.sockopt is not None else None,
        }

@dataclass
class Sniffing(XrayCommonClass):
    enabled: bool = False
    dest_override: List[str] = field(default_factory=lambda: ['http', 'tls', 'quic', 'fakedns'])
    metadata_only: bool = False
    route_only: bool = False

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'Sniffing':
        if json_data is None:
            json_data = {}

        dest_override = json_data.get("destOverride", ['http', 'tls', 'quic', 'fakedns']).copy()
        if dest_override and isinstance(dest_override, list):
            # Ensure all elements are strings and valid sniffing options
            dest_override = [str(x) for x in dest_override if str(x) in [opt.value for opt in SniffingOption]]
        
        return cls(
            enabled=bool(json_data.get("enabled", False)),
            dest_override=dest_override,
            metadata_only=json_data.get("metadataOnly", False),
            route_only=json_data.get("routeOnly", False),
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "destOverride": self.dest_override.copy(),
            "metadataOnly": self.metadata_only,
            "routeOnly": self.route_only,
        }

@dataclass
class Allocate(XrayCommonClass):
    strategy: str = "always"
    refresh: int = 5
    concurrency: int = 3

    @classmethod
    def from_json(cls, json_data: Optional[Dict[str, Any]] = None) -> 'Allocate':
        if json_data is None:
            json_data = {}

        return cls(
            strategy=json_data.get("strategy", "always"),
            refresh=json_data.get("refresh", 5),
            concurrency=json_data.get("concurrency", 3)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy,
            "refresh": self.refresh,
            "concurrency": self.concurrency,
        }

class InboundSettings(XrayCommonClass):
    def __init__(self, protocol: str):
        self._protocol = protocol

    @staticmethod
    def get_settings(protocol: str) -> Optional['InboundSettings']:
        if protocol == Protocols.VMESS:
            return VmessSettings(protocol)
        elif protocol == Protocols.VLESS:
            return VlessSettings(protocol)
        elif protocol == Protocols.TROJAN:
            return TrojanSettings(protocol)
        elif protocol == Protocols.SHADOWSOCKS:
            return ShadowsocksSettings(protocol)
        elif protocol == Protocols.DOKODEMO:
            return DokodemoSettings(protocol)
        elif protocol == Protocols.SOCKS:
            return SocksSettings(protocol)
        elif protocol == Protocols.HTTP:
            return HttpSettings(protocol)
        elif protocol == Protocols.WIREGUARD:
            return WireguardSettings(protocol)
        return None

    @staticmethod
    def from_json(protocol: str, json_data: Optional[Dict[str, Any]] = None) -> Optional['InboundSettings']:
        if protocol == Protocols.VMESS:
            return VmessSettings.from_json(json_data)
        elif protocol == Protocols.VLESS:
            return VlessSettings.from_json(json_data)
        elif protocol == Protocols.TROJAN:
            return TrojanSettings.from_json(json_data)
        elif protocol == Protocols.SHADOWSOCKS:
            return ShadowsocksSettings.from_json(json_data)
        elif protocol == Protocols.DOKODEMO:
            return DokodemoSettings.from_json(json_data)
        elif protocol == Protocols.SOCKS:
            return SocksSettings.from_json(json_data)
        elif protocol == Protocols.HTTP:
            return HttpSettings.from_json(json_data)
        elif protocol == Protocols.WIREGUARD:
            return WireguardSettings.from_json(json_data)
        return None

    def to_json(self) -> Dict[str, Any]:
        """Must be implemented by subclasses"""
        raise NotImplementedError


@dataclass
class VmessSettings(InboundSettings):
    clients: List[Dict[str, Any]] = field(default_factory=list)
    disableInsecureEncryption: bool = False

    def __init__(self, protocol: str, clients: Optional[List[Dict[str, Any]]] = None, 
                 disable_insecure_encryption: bool = False):
        super().__init__(protocol)
        self.clients = clients or []
        self.disableInsecureEncryption = disable_insecure_encryption

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'VmessSettings':
        data = json_data or {}
        return VmessSettings(
            protocol=Protocols.VMESS,
            clients=data.get('clients', []),
            disable_insecure_encryption=data.get('disableInsecureEncryption', False)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "clients": self.clients,
            "disableInsecureEncryption": self.disableInsecureEncryption
        }


@dataclass
class VlessSettings(InboundSettings):
    clients: List[Dict[str, Any]] = field(default_factory=list)
    decryption: str = "none"
    fallbacks: List[Dict[str, Any]] = field(default_factory=list)

    def __init__(self, protocol: str, clients: Optional[List[Dict[str, Any]]] = None, 
                 decryption: str = "none", fallbacks: Optional[List[Dict[str, Any]]] = None):
        super().__init__(protocol)
        self.clients = clients or []
        self.decryption = decryption
        self.fallbacks = fallbacks or []

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'VlessSettings':
        data = json_data or {}
        return VlessSettings(
            protocol=Protocols.VLESS,
            clients=data.get('clients', []),
            decryption=data.get('decryption', 'none'),
            fallbacks=data.get('fallbacks', [])
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "clients": self.clients,
            "decryption": self.decryption,
            "fallbacks": self.fallbacks
        }


@dataclass
class TrojanSettings(InboundSettings):
    clients: List[Dict[str, Any]] = field(default_factory=list)
    fallbacks: List[Dict[str, Any]] = field(default_factory=list)

    def __init__(self, protocol: str, clients: Optional[List[Dict[str, Any]]] = None,
                 fallbacks: Optional[List[Dict[str, Any]]] = None):
        super().__init__(protocol)
        self.clients = clients or []
        self.fallbacks = fallbacks or []

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'TrojanSettings':
        data = json_data or {}
        return TrojanSettings(
            protocol=Protocols.TROJAN,
            clients=data.get('clients', []),
            fallbacks=data.get('fallbacks', [])
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "clients": self.clients,
            "fallbacks": self.fallbacks
        }


@dataclass
class ShadowsocksSettings(InboundSettings):
    method: str = ""
    password: str = ""
    network: str = "tcp,udp"

    def __init__(self, protocol: str, method: str = "", password: str = "", 
                 network: str = "tcp,udp"):
        super().__init__(protocol)
        self.method = method
        self.password = password
        self.network = network

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'ShadowsocksSettings':
        data = json_data or {}
        return ShadowsocksSettings(
            protocol=Protocols.SHADOWSOCKS,
            method=data.get('method', ''),
            password=data.get('password', ''),
            network=data.get('network', 'tcp,udp')
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "method": self.method,
            "password": self.password,
            "network": self.network
        }


@dataclass
class DokodemoSettings(InboundSettings):
    address: str = ""
    port: int = 0
    network: str = "tcp,udp"
    timeout: int = 300
    followRedirect: bool = False
    userLevel: int = 0

    def __init__(self, protocol: str, address: str = "", port: int = 0, 
                 network: str = "tcp,udp", timeout: int = 300, 
                 follow_redirect: bool = False, user_level: int = 0):
        super().__init__(protocol)
        self.address = address
        self.port = port
        self.network = network
        self.timeout = timeout
        self.followRedirect = follow_redirect
        self.userLevel = user_level

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'DokodemoSettings':
        data = json_data or {}
        return DokodemoSettings(
            protocol=Protocols.DOKODEMO,
            address=data.get('address', ''),
            port=data.get('port', 0),
            network=data.get('network', 'tcp,udp'),
            timeout=data.get('timeout', 300),
            follow_redirect=data.get('followRedirect', False),
            user_level=data.get('userLevel', 0)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "address": self.address,
            "port": self.port,
            "network": self.network,
            "timeout": self.timeout,
            "followRedirect": self.followRedirect,
            "userLevel": self.userLevel
        }


@dataclass
class SocksSettings(InboundSettings):
    auth: str = "password"
    accounts: List[Dict[str, str]] = field(default_factory=list)
    udp: bool = False
    ip: str = "127.0.0.1"
    userLevel: int = 0

    def __init__(self, protocol: str, auth: str = "password", 
                 accounts: Optional[List[Dict[str, str]]] = None,
                 udp: bool = False, ip: str = "127.0.0.1", user_level: int = 0):
        super().__init__(protocol)
        self.auth = auth
        self.accounts = accounts or []
        self.udp = udp
        self.ip = ip
        self.userLevel = user_level

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'SocksSettings':
        data = json_data or {}
        return SocksSettings(
            protocol=Protocols.SOCKS,
            auth=data.get('auth', 'password'),
            accounts=data.get('accounts', []),
            udp=data.get('udp', False),
            ip=data.get('ip', '127.0.0.1'),
            user_level=data.get('userLevel', 0)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "auth": self.auth,
            "accounts": self.accounts,
            "udp": self.udp,
            "ip": self.ip,
            "userLevel": self.userLevel
        }


@dataclass
class HttpSettings(InboundSettings):
    accounts: List[Dict[str, str]] = field(default_factory=list)
    allowTransparent: bool = False
    userLevel: int = 0

    def __init__(self, protocol: str, accounts: Optional[List[Dict[str, str]]] = None,
                 allow_transparent: bool = False, user_level: int = 0):
        super().__init__(protocol)
        self.accounts = accounts or []
        self.allowTransparent = allow_transparent
        self.userLevel = user_level

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'HttpSettings':
        data = json_data or {}
        return HttpSettings(
            protocol=Protocols.HTTP,
            accounts=data.get('accounts', []),
            allow_transparent=data.get('allowTransparent', False),
            user_level=data.get('userLevel', 0)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "accounts": self.accounts,
            "allowTransparent": self.allowTransparent,
            "userLevel": self.userLevel
        }


@dataclass
class WireguardSettings(InboundSettings):
    secretKey: str = ""
    address: List[str] = field(default_factory=list)
    peers: List[Dict[str, Any]] = field(default_factory=list)
    mtu: int = 1420
    workers: int = 2

    def __init__(self, protocol: str, secret_key: str = "", address: Optional[List[str]] = None,
                 peers: Optional[List[Dict[str, Any]]] = None, mtu: int = 1420, workers: int = 2):
        super().__init__(protocol)
        self.secretKey = secret_key
        self.address = address or []
        self.peers = peers or []
        self.mtu = mtu
        self.workers = workers

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'WireguardSettings':
        data = json_data or {}
        return WireguardSettings(
            protocol=Protocols.WIREGUARD,
            secret_key=data.get('secretKey', ''),
            address=data.get('address', []),
            peers=data.get('peers', []),
            mtu=data.get('mtu', 1420),
            workers=data.get('workers', 2)
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "secretKey": self.secretKey,
            "address": self.address,
            "peers": self.peers,
            "mtu": self.mtu,
            "workers": self.workers
        }


@dataclass
class Inbound(XrayCommonClass):
    def __init__(self, port: int = 0, listen: str = '', protocol: str = Protocols.VLESS, settings: Optional[InboundSettings] = None,
                 stream_settings: Optional[StreamSettings] = None, tag: str = '', sniffing: Optional[Sniffing] = None,
                 allocate: Optional[Allocate] = None, client_stats: str = ''):
        self.port = port or RandomUtil.random_int_range(10000, 60000)
        self.listen = listen
        self.protocol = protocol
        self.settings = settings if settings is not None else InboundSettings.get_settings(protocol)
        self.stream = stream_settings if stream_settings is not None else StreamSettings()
        self.tag = tag
        self.sniffing = sniffing if sniffing is not None else Sniffing()
        self.allocate = allocate if allocate is not None else Allocate()
        self.client_stats = client_stats



    @property
    def clients(self) -> list:
        # Return clients for protocols that have them
        if hasattr(self.settings, 'clients'):
            return getattr(self.settings, 'clients', []) or []
        return []


    @property
    def network(self):
        return self.stream.network

    @network.setter
    def network(self, network):
        self.stream.network = network

    @property
    def is_tcp(self):
        return self.network == "tcp"

    @property
    def is_ws(self):
        return self.network == "ws"

    @property
    def is_kcp(self):
        return self.network == "kcp"

    @property
    def is_grpc(self):
        return self.network == "grpc"

    @property
    def is_httpupgrade(self):
        return self.network == "httpupgrade"

    @property
    def is_xhttp(self):
        return self.network == "xhttp"

    @property
    def method(self):
        if self.protocol == Protocols.SHADOWSOCKS:
            return getattr(self.settings, 'method', '')
        return ""

    @property
    def is_ss_multi_user(self):
        return self.method != SSMethods.BLAKE3_CHACHA20_POLY1305

    @property
    def is_ss_2022(self):
        return str(self.method).startswith("2022")

    @property
    def server_name(self):
        if getattr(self.stream, 'is_tls', False):
            return getattr(self.stream.tls, 'sni', '')
        if getattr(self.stream, 'is_reality', False):
            return getattr(self.stream.reality, 'server_names', '')
        return ""

    def get_header(self, obj, name):
        for header in getattr(obj, 'headers', []):
            if header.get('name', '').lower() == name.lower():
                return header.get('value', '')
        return ""

    @property
    def host(self):
        if self.is_tcp:
            return self.get_header(self.stream.tcp.request, 'host')
        elif self.is_ws:
            return self.stream.ws.host or self.get_header(self.stream.ws, 'host')
        elif self.is_httpupgrade:
            return self.stream.httpupgrade.host or self.get_header(self.stream.httpupgrade, 'host')
        elif self.is_xhttp:
            return self.stream.xhttp.host or self.get_header(self.stream.xhttp, 'host')
        return None

    @property
    def path(self):
        if self.is_tcp:
            return self.stream.tcp.request.path[0]
        elif self.is_ws:
            return self.stream.ws.path
        elif self.is_httpupgrade:
            return self.stream.httpupgrade.path
        elif self.is_xhttp:
            return self.stream.xhttp.path
        return None

    @property
    def kcp_type(self):
        return self.stream.kcp.type

    @property
    def kcp_seed(self):
        return self.stream.kcp.seed

    @property
    def service_name(self):
        return self.stream.grpc.service_name

    def is_expiry(self, index):
        clients = self.clients or []
        if index < 0 or index >= len(clients):
            return False
        client = clients[index]
        exp = client.get('expiryTime', 0) if isinstance(client, dict) else getattr(client, 'expiryTime', 0)
        return exp > 0 and exp < int(time.time() * 1000)
    @staticmethod
    def random_int_range(start: int, end: int) -> int:
        return random.randint(start, end)

    def can_enable_tls(self):
        return self.protocol in [Protocols.VMESS, Protocols.VLESS, Protocols.TROJAN, Protocols.SHADOWSOCKS] and \
               self.network in ["tcp", "ws", "http", "grpc", "httpupgrade", "xhttp"]

    def can_enable_tls_flow(self):
        return ((getattr(self.stream, 'security', None) in ['tls', 'reality']) and self.network == "tcp" and self.protocol == Protocols.VLESS)

    def can_enable_reality(self):
        return self.protocol in [Protocols.VLESS, Protocols.TROJAN] and self.network in ["tcp", "http", "grpc", "xhttp"]

    def can_enable_stream(self):
        return self.protocol in [Protocols.VMESS, Protocols.VLESS, Protocols.TROJAN, Protocols.SHADOWSOCKS]

    def reset(self):
        self.port = RandomUtil.random_int_range(10000, 60000)
        self.listen = ''
        self.protocol = Protocols.VMESS
        self.settings = InboundSettings.get_settings(Protocols.VMESS)
        self.stream = StreamSettings()
        self.tag = ''
        self.sniffing = Sniffing()
        self.allocate = Allocate()

    def gen_vmess_link(self, address: str = '', port: Optional[int] = None, force_tls: Optional[str] = None, remark: str = '', client_id: str = '', security: str = '') -> str:
        if self.protocol != Protocols.VMESS:
            return ''
        tls = self.stream.security if force_tls == 'same' or force_tls is None else force_tls
        obj = {
            'v': '2',
            'ps': remark,
            'add': address,
            'port': port or self.port,
            'id': client_id,
            'scy': security,
            'net': self.stream.network,
            'type': 'none',
            'tls': tls,
        }
        network = self.stream.network
        if network == 'tcp':
            tcp = self.stream.tcp
            obj['type'] = tcp.type
            if tcp.type == 'http':
                request = tcp.request
                obj['path'] = ','.join(request.path)
                host = self.get_header(request, 'host')
                if host:
                    obj['host'] = host
        elif network == 'kcp':
            kcp = self.stream.kcp
            obj['type'] = kcp.type
            obj['path'] = kcp.seed
        elif network == 'ws':
            ws = self.stream.ws
            obj['path'] = ws.path
            obj['host'] = ws.host or self.get_header(ws, 'host')
        elif network == 'grpc':
            obj['path'] = self.stream.grpc.service_name
            obj['authority'] = self.stream.grpc.authority
            if self.stream.grpc.multi_mode:
                obj['type'] = 'multi'
        elif network == 'httpupgrade':
            httpupgrade = self.stream.httpupgrade
            obj['path'] = httpupgrade.path
            obj['host'] = httpupgrade.host or self.get_header(httpupgrade, 'host')
        elif network == 'xhttp':
            xhttp = self.stream.xhttp
            obj['path'] = xhttp.path
            obj['host'] = xhttp.host or self.get_header(xhttp, 'host')
            obj['mode'] = xhttp.mode
        if tls == 'tls':
            if getattr(self.stream.tls, 'sni', None):
                obj['sni'] = self.stream.tls.sni
            if getattr(self.stream.tls.settings, 'fingerprint', None):
                obj['fp'] = self.stream.tls.settings.fingerprint
            if getattr(self.stream.tls, 'alpn', []):
                obj['alpn'] = ','.join(self.stream.tls.alpn)
            if getattr(self.stream.tls.settings, 'allow_insecure', False):
                obj['allowInsecure'] = self.stream.tls.settings.allow_insecure
        return 'vmess://' + base64.urlsafe_b64encode(json.dumps(obj, ensure_ascii=False).encode()).decode().rstrip('=')

    def gen_vless_link(self, address: str = '', port: Optional[int] = None, force_tls: Optional[str] = None, remark: str = '', client_id: str = '', flow: str = '') -> str:
        uuid = client_id
        type_ = self.stream.network
        security = self.stream.security if force_tls == 'same' or force_tls is None else force_tls
        params = {}
        params['type'] = self.stream.network
        if type_ == 'tcp':
            tcp = self.stream.tcp
            if tcp.type == 'http':
                request = tcp.request
                params['path'] = ','.join(request.path)
                host = self.get_header(request, 'host')
                if host:
                    params['host'] = host
                params['headerType'] = 'http'
        elif type_ == 'kcp':
            kcp = self.stream.kcp
            params['headerType'] = kcp.type
            params['seed'] = kcp.seed
        elif type_ == 'ws':
            ws = self.stream.ws
            params['path'] = ws.path
            params['host'] = ws.host or self.get_header(ws, 'host')
        elif type_ == 'grpc':
            grpc = self.stream.grpc
            params['serviceName'] = grpc.service_name
            params['authority'] = grpc.authority
            if grpc.multi_mode:
                params['mode'] = 'multi'
        elif type_ == 'httpupgrade':
            httpupgrade = self.stream.httpupgrade
            params['path'] = httpupgrade.path
            params['host'] = httpupgrade.host or self.get_header(httpupgrade, 'host')
        elif type_ == 'xhttp':
            xhttp = self.stream.xhttp
            params['path'] = xhttp.path
            params['host'] = xhttp.host or self.get_header(xhttp, 'host')
            params['mode'] = xhttp.mode
        if security == 'tls':
            params['security'] = 'tls'
            if getattr(self.stream.tls.settings, 'fingerprint', None):
                params['fp'] = self.stream.tls.settings.fingerprint
            if getattr(self.stream.tls, 'alpn', []):
                params['alpn'] = ','.join(self.stream.tls.alpn)
            if getattr(self.stream.tls.settings, 'allow_insecure', False):
                params['allowInsecure'] = '1'
            if getattr(self.stream.tls, 'sni', None):
                params['sni'] = self.stream.tls.sni
            if type_ == 'tcp' and flow:
                params['flow'] = flow
        elif security == 'reality':
            params['security'] = 'reality'
            params['pbk'] = getattr(self.stream.reality.settings, 'public_key', '')
            params['fp'] = getattr(self.stream.reality.settings, 'fingerprint', '')
            if getattr(self.stream.reality, 'server_names', ''):
                params['sni'] = self.stream.reality.server_names.split(",")[0]
            if getattr(self.stream.reality, 'short_ids', []):
                params['sid'] = self.stream.reality.short_ids[0] if self.stream.reality.short_ids else ''
            if getattr(self.stream.reality.settings, 'spider_x', ''):
                params['spx'] = self.stream.reality.settings.spider_x
            if type_ == 'tcp' and flow:
                params['flow'] = flow
        else:
            params['security'] = 'none'
        link = f"vless://{uuid}@{address}:{port or self.port}"
        query = urlencode(params)
        url = f"{link}?{query}#{quote(remark)}"
        return url

    def gen_ss_link(self, address: str = '', port: Optional[int] = None, force_tls: Optional[str] = None, remark: str = '', client_password: str = '') -> str:
        settings = self.settings
        type_ = self.stream.network
        security = self.stream.security if force_tls == 'same' or force_tls is None else force_tls
        params = {}
        params['type'] = self.stream.network
        if type_ == 'tcp':
            tcp = self.stream.tcp
            if tcp.type == 'http':
                request = tcp.request
                params['path'] = ','.join(request.path)
                host = self.get_header(request, 'host')
                if host:
                    params['host'] = host
                params['headerType'] = 'http'
        elif type_ == 'kcp':
            kcp = self.stream.kcp
            params['headerType'] = kcp.type
            params['seed'] = kcp.seed
        elif type_ == 'ws':
            ws = self.stream.ws
            params['path'] = ws.path
            params['host'] = ws.host or self.get_header(ws, 'host')
        elif type_ == 'grpc':
            grpc = self.stream.grpc
            params['serviceName'] = grpc.service_name
            params['authority'] = grpc.authority
            if grpc.multi_mode:
                params['mode'] = 'multi'
        elif type_ == 'httpupgrade':
            httpupgrade = self.stream.httpupgrade
            params['path'] = httpupgrade.path
            params['host'] = httpupgrade.host or self.get_header(httpupgrade, 'host')
        elif type_ == 'xhttp':
            xhttp = self.stream.xhttp
            params['path'] = xhttp.path
            params['host'] = xhttp.host or self.get_header(xhttp, 'host')
            params['mode'] = xhttp.mode
        if security == 'tls':
            params['security'] = 'tls'
            if getattr(self.stream.tls.settings, 'fingerprint', None):
                params['fp'] = self.stream.tls.settings.fingerprint
            if getattr(self.stream.tls, 'alpn', []):
                params['alpn'] = ','.join(self.stream.tls.alpn)
            if getattr(self.stream.tls.settings, 'allow_insecure', False):
                params['allowInsecure'] = '1'
            if getattr(self.stream.tls, 'sni', None):
                params['sni'] = self.stream.tls.sni
        password = []
        if hasattr(settings, 'password'):
            password.append(getattr(settings, 'password', ''))
        if self.is_ss_multi_user:
            password.append(client_password)
        method = getattr(settings, 'method', '') if hasattr(settings, 'method') else ''
        userinfo = f"{method}:{':'.join(password)}"
        link = f"ss://{base64.urlsafe_b64encode(userinfo.encode()).decode().rstrip('=')}@{address}:{port or self.port}"
        query = urlencode(params)
        url = f"{link}?{query}#{quote(remark)}"
        return url

    def gen_trojan_link(self, address: str = '', port: Optional[int] = None, force_tls: Optional[str] = None, remark: str = '', client_password: str = '') -> str:
        security = self.stream.security if force_tls == 'same' or force_tls is None else force_tls
        type_ = self.stream.network
        params = {}
        params['type'] = self.stream.network
        if type_ == 'tcp':
            tcp = self.stream.tcp
            if tcp.type == 'http':
                request = tcp.request
                params['path'] = ','.join(request.path)
                host = self.get_header(request, 'host')
                if host:
                    params['host'] = host
                params['headerType'] = 'http'
        elif type_ == 'kcp':
            kcp = self.stream.kcp
            params['headerType'] = kcp.type
            params['seed'] = kcp.seed
        elif type_ == 'ws':
            ws = self.stream.ws
            params['path'] = ws.path
            params['host'] = ws.host or self.get_header(ws, 'host')
        elif type_ == 'grpc':
            grpc = self.stream.grpc
            params['serviceName'] = grpc.service_name
            params['authority'] = grpc.authority
            if grpc.multi_mode:
                params['mode'] = 'multi'
        elif type_ == 'httpupgrade':
            httpupgrade = self.stream.httpupgrade
            params['path'] = httpupgrade.path
            params['host'] = httpupgrade.host or self.get_header(httpupgrade, 'host')
        elif type_ == 'xhttp':
            xhttp = self.stream.xhttp
            params['path'] = xhttp.path
            params['host'] = xhttp.host or self.get_header(xhttp, 'host')
            params['mode'] = xhttp.mode
        if security == 'tls':
            params['security'] = 'tls'
            if getattr(self.stream.tls.settings, 'fingerprint', None):
                params['fp'] = self.stream.tls.settings.fingerprint
            if getattr(self.stream.tls, 'alpn', []):
                params['alpn'] = ','.join(self.stream.tls.alpn)
            if getattr(self.stream.tls.settings, 'allow_insecure', False):
                params['allowInsecure'] = '1'
            if getattr(self.stream.tls, 'sni', None):
                params['sni'] = self.stream.tls.sni
        elif security == 'reality':
            params['security'] = 'reality'
            params['pbk'] = getattr(self.stream.reality.settings, 'public_key', '')
            params['fp'] = getattr(self.stream.reality.settings, 'fingerprint', '')
            if getattr(self.stream.reality, 'server_names', ''):
                params['sni'] = self.stream.reality.server_names.split(",")[0]
            if getattr(self.stream.reality, 'short_ids', []):
                params['sid'] = self.stream.reality.short_ids[0] if self.stream.reality.short_ids else ''
            if getattr(self.stream.reality.settings, 'spider_x', ''):
                params['spx'] = self.stream.reality.settings.spider_x
        else:
            params['security'] = 'none'
        link = f"trojan://{client_password}@{address}:{port or self.port}"
        query = urlencode(params)
        url = f"{link}?{query}#{quote(remark)}"
        return url

    def get_wireguard_link(self, address: str, port: int, remark: str, peer_id: int) -> str:
        s = self.settings
        peers = getattr(s, 'peers', [])
        if not peers or peer_id >= len(peers):
            return ''
        peer = peers[peer_id]
        txt = f"[Interface]\n"
        txt += f"PrivateKey = {peer.get('privateKey', '')}\n"
        allowed_ips = peer.get('allowedIPs', [''])
        txt += f"Address = {allowed_ips[0]}\n"
        txt += f"DNS = 1.1.1.1, 1.0.0.1\n"
        mtu = getattr(s, 'mtu', None)
        if mtu:
            txt += f"MTU = {mtu}\n"
        txt += f"\n# {remark}\n"
        txt += f"[Peer]\n"
        txt += f"PublicKey = {getattr(s, 'pubKey', '')}\n"
        txt += f"AllowedIPs = 0.0.0.0/0, ::/0\n"
        txt += f"Endpoint = {address}:{port}"
        if peer.get('psk'):
            txt += f"\nPresharedKey = {peer['psk']}"
        if peer.get('keepAlive'):
            txt += f"\nPersistentKeepalive = {peer['keepAlive']}\n"
        return txt

    def gen_link(self, address: str = '', port: Optional[int] = None, force_tls: str = 'same', remark: str = '', client: Any = None) -> str:
        if self.protocol == Protocols.VMESS:
            return self.gen_vmess_link(address, port, force_tls, remark, getattr(client, 'id', ''), getattr(client, 'security', ''))
        elif self.protocol == Protocols.VLESS:
            return self.gen_vless_link(address, port, force_tls, remark, getattr(client, 'id', ''), getattr(client, 'flow', ''))
        elif self.protocol == Protocols.SHADOWSOCKS:
            return self.gen_ss_link(address, port, force_tls, remark, getattr(client, 'password', '') if self.is_ss_multi_user else '')
        elif self.protocol == Protocols.TROJAN:
            return self.gen_trojan_link(address, port, force_tls, remark, getattr(client, 'password', ''))
        return ''

    def gen_all_links(self, remark: str = '', remark_model: str = '-ieo', client: Any = None) -> list:
        result = []
        email = getattr(client, 'email', '') if client else ''
        addr = self.listen if self.listen and self.listen != "0.0.0.0" else 'localhost'
        port = self.port
        separation_char = remark_model[0]
        order_chars = remark_model[1:]
        orders = {'i': remark, 'e': email, 'o': ''}
        external_proxy = getattr(self.stream, 'external_proxy', [])
        if not external_proxy:
            r = separation_char.join([orders[c] for c in order_chars if orders[c]])
            result.append({'remark': r, 'link': self.gen_link(addr, port, 'same', r, client)})
        else:
            for ep in external_proxy:
                ep_remark = ep.get('remark', '') if isinstance(ep, dict) else getattr(ep, 'remark', '')
                ep_dest = ep.get('dest', '') if isinstance(ep, dict) else getattr(ep, 'dest', '')
                ep_port = ep.get('port', 0) if isinstance(ep, dict) else getattr(ep, 'port', 0)
                ep_force_tls = ep.get('forceTls', 'same') if isinstance(ep, dict) else getattr(ep, 'forceTls', 'same')
                orders['o'] = ep_remark
                r = separation_char.join([orders[c] for c in order_chars if orders[c]])
                result.append({'remark': r, 'link': self.gen_link(ep_dest, ep_port, ep_force_tls, r, client)})
        return result

    def gen_inbound_links(self, remark: str = '', remark_model: str = '-ieo') -> str:
        addr = self.listen if self.listen and self.listen != "0.0.0.0" else 'localhost'
        clients = self.clients
        if clients:
            links = []
            for client in clients:
                for l in self.gen_all_links(remark, remark_model, client):
                    links.append(l['link'])
            return '\r\n'.join(links)
        else:
            if self.protocol == Protocols.SHADOWSOCKS and not self.is_ss_multi_user:
                return self.gen_ss_link(addr, self.port, 'same', remark)
            if self.protocol == Protocols.WIREGUARD:
                links = []
                for idx, _ in enumerate(getattr(self.settings, 'peers', [])):
                    links.append(self.get_wireguard_link(addr, self.port, remark + remark_model[0] + str(idx + 1), idx))
                return '\r\n'.join(links)
            return ''


    def to_json(self) -> Dict[str, Any]:
        stream_settings = self.stream.to_json() if self.can_enable_stream() else None
        return {
            "port": self.port,
            "listen": self.listen,
            "protocol": self.protocol,
            "settings": self.settings.to_json() if isinstance(self.settings, XrayCommonClass) else self.settings,
            "streamSettings": stream_settings,
            "tag": self.tag,
            "sniffing": self.sniffing.to_json() if self.sniffing else None,
            "allocate": self.allocate.to_json() if self.allocate else None,
            "clientStats": getattr(self, 'client_stats', '')
        }

    @staticmethod
    def from_json(json_data: Optional[Dict[str, Any]] = None) -> 'Inbound':
        if not json_data:
            return Inbound()

        protocol = json_data.get('protocol', Protocols.VMESS)
        settings = InboundSettings.from_json(protocol, json_data.get('settings'))
        stream_settings = StreamSettings.from_json(json_data.get('streamSettings')) if json_data.get('streamSettings') else None
        sniffing = Sniffing.from_json(json_data.get('sniffing')) if json_data.get('sniffing') else None
        allocate = Allocate.from_json(json_data.get('allocate')) if json_data.get('allocate') else None

        return Inbound(
            port=json_data.get('port', 0),
            protocol=protocol,
            settings=settings,
            tag=json_data.get('tag', ''),
            listen=json_data.get('listen', '0.0.0.0'),
            stream_settings=stream_settings,
            sniffing=sniffing,
            allocate=allocate
        )

