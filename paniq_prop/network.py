import network

from paniq_prop.logger import Logger
from paniq_prop.status_leds import StatusLed
from paniq_prop.network_adapters.ethernet import EthernetNetworkAdapter
from paniq_prop.network_adapters.wifi import WifiNetworkAdapter

logger = Logger(__name__)


class Network():
    def __init__(
        self,
        statusLed: StatusLed,

        wifi_ssid: str,
        wifi_password: str,
        wifi_connection_check_period: int,

        eth_dhcp: bool,
        eth_ip: str,
        eth_subnet: str,
        eth_gateway: str,
        eth_dns: str,
        eth_connection_check_period: int,
    ):
        self.statusLed = statusLed

        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.wifi_connection_check_period = wifi_connection_check_period

        self.eth_dhcp = eth_dhcp
        self.eth_ip = eth_ip
        self.eth_subnet = eth_subnet
        self.eth_gateway = eth_gateway
        self.eth_dns = eth_dns
        self.eth_connection_check_period = eth_connection_check_period

        self.network_adapter_class = None
        self.network_adapter = None

        self.detect_network_adapter_class()
        self.init_network_adapter()
        self.connect()
    
    def detect_network_adapter_class(self):
        try:
            if network.WIZNET5K:
                self.network_adapter_class = EthernetNetworkAdapter
        except AttributeError:
            try:
                if network.WLAN:
                    self.network_adapter_class = WifiNetworkAdapter
            except AttributeError:
                logger.critical("Not found a supported network device.")
        
    def init_network_adapter(self):
        if self.network_adapter_class == WifiNetworkAdapter:
            self.network_adapter = WifiNetworkAdapter(
                statusLed=self.statusLed,
                ssid=self.wifi_ssid,
                password=self.wifi_password,
                connection_check_period=self.wifi_connection_check_period,
            )
        elif self.network_adapter_class == EthernetNetworkAdapter:
            self.network_adapter = EthernetNetworkAdapter(
                statusLed=self.statusLed,
                dhcp=self.eth_dhcp,
                ip=self.eth_ip,
                subnet=self.eth_subnet,
                gateway=self.eth_gateway,
                dns=self.eth_dns,
                connection_check_period=self.eth_connection_check_period,
            )
        else:
            logger.critical("Cannot initialise network without a supported network adapter.")

    def connect(self):
        if self.network_adapter_class:
            logger.info(f"Connecting network using {self.network_adapter_class.__name__} adapter...")
            if self.network_adapter:
                self.network_adapter.connect()
            else:
                logger.critical("Network adapter class not initialised")
        else:
            logger.critical("Network adapter class not defined")
    
    def disconnect(self):
        if self.network_adapter:
            self.network_adapter.disconnect()

    def isconnected(self):
        if self.network_adapter:
            self.network_adapter.isconnected()

