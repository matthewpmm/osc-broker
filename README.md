# osc-broker
An extremely bare-bones middleman server that reroutes messages to specified OSC clients based on topic.

This is built to bypass the one-device limit for OSC destinations with a COGS Pro license (and 3 for COGS Premium) by acting as a single point of contact between COGS and other OSC clients on the network.

To adjust this code for your own system, first update the IP address and port to the appropriate ones for your device, as visible to other devices on your network. If you are only trying to interface with other software clients on the same computer as the broker (for instance, if you wanted to interface with Ableton Live and QLab at the same time) you can use the ip "localhost".

Then, update the `ROUTING_TABLE` with the OSC message addresses you want to route to each client, as well as the IP address and port of each client. A sample address for routing OSC messages to COGS with the standard COGS OSC default networking info is provided.