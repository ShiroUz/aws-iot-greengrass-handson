import socket
import logging

logger = logging.getLogger("NetworkUtil")

def get_local_ip():
    """Get the local IP address of the device"""
    try:
        # Create a socket to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use a public DNS server to determine the local IP (doesn't actually send any data)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        logger.error(f"Error getting local IP address: {str(e)}")
        # Fallback to localhost
        return "127.0.0.1"