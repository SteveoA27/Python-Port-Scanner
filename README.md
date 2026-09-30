# Python Port Scanner

A lightweight network port scanner written in Python. This project was developed to practise Python networking, socket programming, error handling and basic cybersecurity concepts.

The scanner allows a user to specify a target IP address or hostname and a range of ports to check. It identifies open ports and attempts to determine the service running on each open port.

## Features

* Accepts an IP address or hostname as a target
* Scans a user-defined range of TCP ports
* Identifies open ports
* Attempts to identify the service associated with an open port
* Retrieves basic service banners where available
* Displays the target IP address
* Provides clear terminal output
* Includes basic error handling
* Built using Python's standard library

## Example Output

```text
Python Network Port Scanner
==================================================
Target: 127.0.0.1
IP Address: 127.0.0.1
Port range: 8000-8000

[OPEN] Port 8000 - Service: irdmi
       Banner: HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.9.6
```

## Technologies Used

* Python
* Socket programming
* TCP/IP networking
* Python standard library
* Git
* GitHub

## Requirements

Python 3.x is required.
