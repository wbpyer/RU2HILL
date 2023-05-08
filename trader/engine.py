






class MainEngine:
    """
    Acts as the core of the trading platform.
    """

    def __init__(self, event_engine: EventEngine = None) -> None:
        """"""
        if event_engine:
            self.event_engine: EventEngine = event_engine
        else:
            self.event_engine = EventEngine()
        self.event_engine.start()

        self.gateways: Dict[str, BaseGateway] = {}
        self.engines: Dict[str, BaseEngine] = {}
        self.apps: Dict[str, BaseApp] = {}
        self.exchanges: List[Exchange] = []

        os.chdir(TRADER_DIR)    # Change working directory
        self.init_engines()     # Initialize function engines

    def add_engine(self, engine_class: Any) -> "BaseEngine":
        """
        Add function engine.
        """
        engine: BaseEngine = engine_class(self, self.event_engine)
        self.engines[engine.engine_name] = engine
        return engine

    def add_gateway(self, gateway_class: Type[BaseGateway], gateway_name: str = "") -> BaseGateway:
        """
        Add gateway.
        """
        # Use default name if gateway_name not passed
        if not gateway_name:
            gateway_name: str = gateway_class.default_name

        gateway: BaseGateway = gateway_class(self.event_engine, gateway_name)
        self.gateways[gateway_name] = gateway

        # Add gateway supported exchanges into engine
        for exchange in gateway.exchanges:
            if exchange not in self.exchanges:
                self.exchanges.append(exchange)

        return gateway

    def add_app(self, app_class: Type[BaseApp]) -> "BaseEngine":
        """
        Add app.
        """
        app: BaseApp = app_class()
        self.apps[app.app_name] = app

        engine: BaseEngine = self.add_engine(app.engine_class)
        return engine

    def init_engines(self) -> None:
        """
        Init all engines.
        """
        self.add_engine(LogEngine)
        self.add_engine(OmsEngine)
        self.add_engine(EmailEngine)

    def write_log(self, msg: str, source: str = "") -> None:
        """
        Put log event with specific message.
        """
        log: LogData = LogData(msg=msg, gateway_name=source)
        event: Event = Event(EVENT_LOG, log)
        self.event_engine.put(event)

    def get_gateway(self, gateway_name: str) -> BaseGateway:
        """
        Return gateway object by name.
        """
        gateway: BaseGateway = self.gateways.get(gateway_name, None)
        if not gateway:
            self.write_log(f"找不到底层接口：{gateway_name}")
        return gateway

    def get_engine(self, engine_name: str) -> "BaseEngine":
        """
        Return engine object by name.
        """
        engine: BaseEngine = self.engines.get(engine_name, None)
        if not engine:
            self.write_log(f"找不到引擎：{engine_name}")
        return engine

    def get_default_setting(self, gateway_name: str) -> Optional[Dict[str, Any]]:
        """
        Get default setting dict of a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            return gateway.get_default_setting()
        return None

    def get_all_gateway_names(self) -> List[str]:
        """
        Get all names of gatewasy added in main engine.
        """
        return list(self.gateways.keys())

    def get_all_apps(self) -> List[BaseApp]:
        """
        Get all app objects.
        """
        return list(self.apps.values())

    def get_all_exchanges(self) -> List[Exchange]:
        """
        Get all exchanges.
        """
        return self.exchanges

    def connect(self, setting: dict, gateway_name: str) -> None:
        """
        Start connection of a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            gateway.connect(setting)

    def subscribe(self, req: SubscribeRequest, gateway_name: str) -> None:
        """
        Subscribe tick data update of a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            gateway.subscribe(req)

    def send_order(self, req: OrderRequest, gateway_name: str) -> str:
        """
        Send new order request to a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            return gateway.send_order(req)
        else:
            return ""

    def cancel_order(self, req: CancelRequest, gateway_name: str) -> None:
        """
        Send cancel order request to a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            gateway.cancel_order(req)

    def send_quote(self, req: QuoteRequest, gateway_name: str) -> str:
        """
        Send new quote request to a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            return gateway.send_quote(req)
        else:
            return ""

    def cancel_quote(self, req: CancelRequest, gateway_name: str) -> None:
        """
        Send cancel quote request to a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            gateway.cancel_quote(req)

    def query_history(self, req: HistoryRequest, gateway_name: str) -> Optional[List[BarData]]:
        """
        Query bar history data from a specific gateway.
        """
        gateway: BaseGateway = self.get_gateway(gateway_name)
        if gateway:
            return gateway.query_history(req)
        else:
            return None

    def close(self) -> None:
        """
        Make sure every gateway and app is closed properly before
        programme exit.
        """
        # Stop event engine first to prevent new timer event.
        self.event_engine.stop()

        for engine in self.engines.values():
            engine.close()

        for gateway in self.gateways.values():
            gateway.close()