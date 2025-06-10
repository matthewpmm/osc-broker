# Python OSC Broker
# Designed to extend COGS OSC support to many devices

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# ip and port for THIS DEVICE
# use localhost if only networking with other clients on this computer
ip = "localhost"
port = 1337

class OSCDestination:
    def __init__(self, address, ip, port):
        self.address = address
        self.ip = ip
        self.port = port
        self.client = SimpleUDPClient(self.ip, self.port)

    def __repr__(self):
        return f"{self.address}, {self.ip}, {self.port}"

    def compare_address(self, to_compare):
        address = self.address.split('/')
        to_compare = to_compare.split('/')

        for i in range(len(address)):
            if address[i] == '*' or to_compare[i] == '*':   # if lone select character, then all subtopics after this count as a match
                # print("* FOUND")    # TESTING
                return True
            if address[i] != to_compare[i]:                 # return false as soon as a discrepancy is found
                # print(f"DOES NOT MATCH AT INDEX {i}")   # TESTING
                return False

        return True

    def send_message(self, address, args):
        self.client.send_message(address, args)

# ROUTING TABLE
# specifies which addresss should be directed to which IPs
# format: OSCDestination(address (string), IP (string), port (int))
ROUTING_TABLE = [
    OSCDestination("/cogs/*", "192.168.1.100", 12097)
]
print()
print("Routing Table:")
for i in range(len(ROUTING_TABLE)):
    print(f"\t{ROUTING_TABLE}")


def msg_handler(address, *args):
    print(f"\nReceived message: {address}: {args}")

    # determine the appropriate client(s) to route this message to
    for destination in ROUTING_TABLE:
        print(f"\tChecking for address match to {destination.ip}:{destination.port}")
        if destination.compare_address(address):
            print("\t\t---> SENT!")
            destination.send_message(address, args)

# begin server
print()
print("Beginning server.")
dispatcher = Dispatcher()
dispatcher.set_default_handler(msg_handler)
server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever

print('BROKER TERMINATED')