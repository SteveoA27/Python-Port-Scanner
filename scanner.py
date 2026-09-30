import socket
import sys
import time


def scan_port(target, port):
    """Check whether a TCP port is open."""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            return sock.connect_ex((target, port)) == 0

    except socket.error:
        return False

def get_service(port):
    """Return the registered TCP service for a port."""

    try:
        service = socket.getservbyport(port, "tcp")
        return service
    except OSError:
        return "Unknown"
    
def grab_banner(target, port):
    """Attempt to retrieve a banner from an open port."""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((target, port))

            request = (
            f"GET / HTTP/1.0\r\n"
            f"Host: {target}\r\n"
            f"Connection: close\r\n\r\n"
            ).encode()
            sock.sendall(request)

            banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()

            
            if banner:
                return banner

            return "No banner received"

    except (socket.timeout, socket.error):
        return "No banner received"
def validate_ports(start_port, end_port):
    """Validate the supplied port range."""

    if not 1 <= start_port <= 65535:
        return False, "Start port must be between 1 and 65535."
    if not 1 <= end_port <= 65535:
        return False, "End port must be between 1 and 65535."

    if start_port > end_port:
        return False, "Start port cannot be greater than end port."

    return True, ""

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

    valid, error_message = validate_ports(start_port, end_port)

    if not valid:
        print(error_message)
        sys.exit(1)

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Unable to resolve hostname: {target}")
        sys.exit(1)

    print("=" * 60)
    print("Python Network Port Scanner")
    print("=" * 60)
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