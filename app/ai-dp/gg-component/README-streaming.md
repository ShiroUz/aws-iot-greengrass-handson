# Image Streaming Server for AI Driving Partner

This component adds image streaming capabilities to the AI Driving Partner application, allowing you to view captured images from the Greengrass Core device directly in a web browser.

## Prerequisites

- Greengrass Core device with SSH access
- Python 3.6+ with required packages (see requirements-streaming.txt)
- Web browser on your PC

## Setup

1. Install required Python packages:

```bash
pip install -r requirements-streaming.txt
```

2. Ensure port forwarding is allowed on the device (port 8080 by default)

## Usage

1. Start the AI Driving Partner application:

```bash
python main.py
```

2. The streaming server starts automatically and displays its URL in the logs:

```
Image streaming server started at http://192.168.x.x:8080
```

3. Access the image viewer in your browser by navigating to the URL displayed in the logs

4. If you need to use a different port, set the environment variable before starting:

```bash
export WEB_SERVER_PORT=9000
python main.py
```

## Features

- Web interface to browse all captured images
- Real-time updates with auto-refresh functionality
- View most recent images at the top of the list
- Clean interface with image preview

## Troubleshooting

If you cannot connect to the streaming server:

1. Verify the server is running by checking the application logs
2. Check if the port is accessible (try `telnet 192.168.x.x 8080` from your PC)
3. Ensure no firewall is blocking the connection
4. Verify the IP address shown in the logs is correct and reachable from your PC
5. Try a different browser if the web interface doesn't load properly

## Security Notes

The image streaming server is intended for development and testing purposes only. It does not implement authentication or encryption. Do not use in production environments without adding appropriate security measures.