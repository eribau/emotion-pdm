# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm

IP = "127.0.0.1"
PORT = "6503"

def handlerfunction(s):
    # Will receive message data unpacked in s, x, y
    print("Received message!", s)
    pass

def handlerfunction2(s, x, y):
    print("Received message! 2")
    pass

# Start the system.
osc_startup()

# Make server channels to receive packets.
osc_udp_server(IP, PORT, "aservername")
osc_udp_server("0.0.0.0", 3724, "anotherserver")

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/test/F0", handlerfunction)
osc_method("/test/me", handlerfunction2)
# Too, but request the message address pattern before in argscheme

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    # …
    try:
        osc_process()
    except KeyboardInterrupt():
        osc_terminate()
        pass
    # …

# Properly close the system.
osc_terminate()
