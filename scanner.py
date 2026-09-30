import socket
import sys
import time


def scan_port(target, port):
    """Check whether a TCP port is open."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:
            return True

        return False

    except socket.error:
        return False

    finally:
        sock.close()

def get_service(port):
    try:
        service = socket.getservbyport(port, "tcp")
        return service
    except OSError:
        return "Unknown"
    
def grab_banner(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        sock.connect((target, port))

        request = b"GET / HTTP/1.0\r\nHost: localhost\r\n\r\n"
        sock.sendall(request)

        banner = sock.recv(1024).decode("utf-8", errors="ignore")

        sock.close()

        return banner

    except (socket.timeout, socket.error):
        return "No banner received"

def main():

    if len(sys.argv) != 4:
        print("Usage: python3 scanner.py <target> <start_port> <end_port>")
        sys.exit(1)

    target = sys.argv[1]

    try:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except ValueError:
        print("Ports must be numbers.")
        sys.exit(1)

    if not 1 <= start_port <= 65535:
        print("Start port must be between 1 and 65535.")
        sys.exit(1)

    if not 1 <= end_port <= 65535:
        print("End port must be between 1 and 65535.")
        sys.exit(1)

    if start_port > end_port:
        print("Start port cannot be greater than end port.")
        sys.exit(1)

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Unable to resolve hostname: {target}")
        sys.exit(1)

    print("=" * 50)
    print("Python Network Port Scanner")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"IP Address: {target_ip}")
    print(f"Port range: {start_port}-{end_port}")
    print()

    start_time = time.time()

    open_ports = []

    for port in range(start_port, end_port + 1):

        if scan_port(target_ip, port):
            service = get_service(port)
            banner = grab_banner(target_ip, port)

            print(f"[OPEN] Port {port} - Service: {service}")
            print(f"       Banner: {banner[:100]}")

            open_ports.append(port)

    end_time = time.time()

    print()
    print("=" * 50)
    print(f"Scan completed in {end_time - start_time:.2f} seconds")
    print(f"Open ports found: {len(open_ports)}")
    print("=" * 50)


if __name__ == "__main__":
    main()