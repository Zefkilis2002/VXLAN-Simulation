# Importazioni necessarie da Ryu
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import udp

# Controller Ryu per gestire il tunnel VXLAN
class VXLANController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Costruttore del controller
    def __init__(self, *args, **kwargs):
        super(VXLANController, self).__init__(*args, **kwargs) # Inizializzazione del controller

    # Metodo per gestire l'evento di connessione di uno switch Openflow
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath #Identificativo dello switch
        ofproto = datapath.ofproto # Protocollo OpenFlow utilizzato dallo switch
        parser = datapath.ofproto_parser

        # Aggiunta di una regola di default per il table-miss
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    # Metodo per aggiungere una regola di flusso (instradamento) allo switch
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # Definizione dell'azione da applicare ai pacchetti che soddisfano la regola
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        # Creiamo un messaggio per aggiungere una nuova regola di instradamento
        # - `datapath`: lo switch che riceverà la regola
        # - `priority`: la priorità della regola (più alto significa più importante)
        # - `match`: i criteri che i pacchetti devono soddisfare per attivare questa regola
        # - `instructions`: le azioni da eseguire sui pacchetti corrispondenti
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod) # Inviamo il messaggio allo switch per installare la regola

    # Metodo per gestire l'evento di ricezione di un pacchetto da uno switch (packet-in)
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg # Messaggio ricevuto dallo switch
        datapath = msg.datapath # Switch che ha inviato il messaggio
        in_port = msg.match['in_port'] # Porta di ingresso del pacchetto

        pkt = packet.Packet(msg.data) # Estraiamo il pacchetto dal messaggio
        eth = pkt.get_protocol(ethernet.ethernet) # Estraiamo l'header Ethernet dal pacchetto

        # Verifichiamo che il pacchetto sia un pacchetto VXLAN
        if eth.ethertype == 0x0800:  # IPv4
            ip_pkt = pkt.get_protocol(ipv4.ipv4)
            if ip_pkt.proto == 17:  # UDP
                udp_pkt = pkt.get_protocol(udp.udp)
                self.logger.info("VXLAN Packet: src_ip=%s dst_ip=%s src_port=%d dst_port=%d", 
                                 ip_pkt.src, ip_pkt.dst, udp_pkt.src_port, udp_pkt.dst_port)

        actions = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_FLOOD)]
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)
