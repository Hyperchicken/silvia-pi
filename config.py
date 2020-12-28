#!/usr/bin/python

# Raspberry Pi SPI Port and Device
spi_port = 0
spi_dev = 0

# Pin # for relay connected to heating element
he_pin = 7

# Main loop sample rate in seconds
sample_time = 0.1

# PID Proportional, Integral, and Derivative values
pc = 3.4
ic = 0.3
dc = 40.0

pw = 2.9
iw = 0.3
dw = 40.0

# Web/REST Server Options
port = 8080

# Uses emulated hardware if True
testing = False
