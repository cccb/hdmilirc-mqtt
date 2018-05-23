# hdmimatrix-mqtt

This project is ongoing for a while.
First attempt was to wire up a cheap 4 input 2 output HDMI matrix
to an esp32. This was abandoned after it was kind of unstable.

The current approach is to use a: Ligawo 3080026 4x1 HDMI
switch acquired from Amazon which has a serial interface.

We reimplemented the serial protocol, as the windows software
is a) well a windows software, b) a shitty one.

Now we have some nice bridge between MQTT and the HDMI-switch.

