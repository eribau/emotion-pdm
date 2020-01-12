# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

IP = "127.0.0.1"
PORT = "6503"

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client(IP, PORT, "aclientname")

# Build a simple message and send it.
msg = oscbuildparse.OSCMessage("/test/F0", ",f", [1.0])
osc_send(msg, "aclientname")

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    # You can send OSC messages from your event loop too…
    # …
    osc_process()
    # …

# Properly close the system.
osc_terminate()
