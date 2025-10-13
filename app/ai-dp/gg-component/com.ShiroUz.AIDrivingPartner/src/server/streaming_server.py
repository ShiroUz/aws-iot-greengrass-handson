import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import io
import time
import json

logger = logging.getLogger("StreamingServer")

# Global variable to store the latest frame for streaming
latest_frame = None
frame_lock = threading.Lock()

class ImageHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for serving images"""
    
    def __init__(self, *args, **kwargs):
        self.images_dir = kwargs.pop('images_dir', "/app/images/")
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self._serve_index()
        elif self.path == '/stream':
            self._serve_stream()
        elif self.path == '/list':
            self._serve_image_list()
        elif self.path.startswith('/image/'):
            # Remove '/image/' prefix and handle query parameters
            image_path = self.path[7:]
            if '?' in image_path:
                image_name = image_path.split('?')[0]  # Remove query parameters
            else:
                image_name = image_path
            self._serve_image(image_name)
        else:
            self._serve_404()
    
    def _serve_index(self):
        """Serve the HTML index page with image viewer"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Greengrass Device Image Viewer</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                #image-container { margin: 20px 0; }
                #image-list { height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; }
                .image-item { cursor: pointer; padding: 5px; margin: 2px; background: #f0f0f0; }
                .image-item:hover { background: #e0e0e0; }
                #main-image { max-width: 100%; max-height: 600px; border: 1px solid #ddd; }
                .controls { margin: 10px 0; }
                button { padding: 5px 10px; }
            </style>
        </head>
        <body>
            <h1>Greengrass Device Image Viewer</h1>
            <div class="controls">
                <button onclick="refreshImageList()">Refresh Image List</button>
                <button onclick="startAutoRefresh()">Start Auto Refresh (5s)</button>
                <button onclick="stopAutoRefresh()">Stop Auto Refresh</button>
            </div>
            <div style="display: flex; flex-direction: row;">
                <div style="flex: 1;">
                    <h3>Available Images</h3>
                    <div id="image-list"></div>
                </div>
                <div style="flex: 2; margin-left: 20px;">
                    <h3>Selected Image</h3>
                    <div id="image-container">
                        <img id="main-image" src="" alt="Select an image to view">
                    </div>
                    <p id="image-info"></p>
                    
                    <h3>Live Stream</h3>
                    <div style="margin-top: 20px;">
                        <img id="live-stream" src="/stream" alt="Live camera stream" 
                             style="max-width: 100%; max-height: 400px; border: 1px solid #ddd;">
                    </div>
                </div>
            </div>
            
            <script>
                let autoRefreshInterval;
                
                // Function to load and display the image list
                function refreshImageList() {
                    fetch('/list')
                        .then(response => response.json())
                        .then(data => {
                            const listElement = document.getElementById('image-list');
                            listElement.innerHTML = '';
                            
                            if (data.images.length === 0) {
                                listElement.innerHTML = '<p>No images available</p>';
                                return;
                            }
                            
                            // Sort by name descending (newest first assuming timestamp in name)
                            data.images.sort((a, b) => b.localeCompare(a));
                            
                            data.images.forEach(image => {
                                const item = document.createElement('div');
                                item.className = 'image-item';
                                item.textContent = image;
                                item.onclick = () => loadImage(image);
                                listElement.appendChild(item);
                            });
                            
                            // Load the newest image by default
                            if (data.images.length > 0) {
                                loadImage(data.images[0]);
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching image list:', error);
                            document.getElementById('image-list').innerHTML = 
                                '<p>Error loading image list. Please try refreshing.</p>';
                        });
                }
                
                // Function to load a specific image
                function loadImage(imageName) {
                    const img = document.getElementById('main-image');
                    const info = document.getElementById('image-info');
                    
                    // Add timestamp to prevent caching
                    img.src = `/image/${imageName}?t=${new Date().getTime()}`;
                    info.textContent = `Viewing: ${imageName}`;
                    
                    // Highlight the selected image in the list
                    const items = document.getElementsByClassName('image-item');
                    for (let i = 0; i < items.length; i++) {
                        if (items[i].textContent === imageName) {
                            items[i].style.background = '#b8d0e8';
                        } else {
                            items[i].style.background = '#f0f0f0';
                        }
                    }
                }
                
                // Auto-refresh functions
                function startAutoRefresh() {
                    stopAutoRefresh();  // Clear any existing interval
                    autoRefreshInterval = setInterval(refreshImageList, 5000);
                    console.log('Auto-refresh started (every 5 seconds)');
                }
                
                function stopAutoRefresh() {
                    if (autoRefreshInterval) {
                        clearInterval(autoRefreshInterval);
                        autoRefreshInterval = null;
                        console.log('Auto-refresh stopped');
                    }
                }
                
                // Initialize the page
                document.addEventListener('DOMContentLoaded', refreshImageList);
            </script>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
    
    def _serve_stream(self):
        """Serve live camera stream as MJPEG"""
        self.send_response(200)
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        try:
            while True:
                with frame_lock:
                    if latest_frame is not None:
                        # Encode frame as JPEG
                        import cv2
                        _, buffer = cv2.imencode('.jpg', latest_frame)
                        frame_bytes = buffer.tobytes()
                        
                        # Send frame in MJPEG format
                        self.wfile.write(b'\r\n--frame\r\n')
                        self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                        self.wfile.write(frame_bytes)
                        self.wfile.write(b'\r\n')
                    else:
                        # Send placeholder if no frame available
                        self.wfile.write(b'\r\n--frame\r\n')
                        self.wfile.write(b'Content-Type: text/plain\r\n\r\n')
                        self.wfile.write(b'No frame available')
                        self.wfile.write(b'\r\n')
                
                time.sleep(0.1)  # 10 FPS
                
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
    
    def _serve_image_list(self):
        """Serve a JSON list of available images"""
        try:
            images_dir = self.server.images_dir
            image_files = []
            
            if os.path.exists(images_dir) and os.path.isdir(images_dir):
                # Recursively search for image files in subdirectories
                for root, dirs, files in os.walk(images_dir):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            # Get relative path from images_dir
                            rel_path = os.path.relpath(os.path.join(root, file), images_dir)
                            image_files.append(rel_path.replace(os.sep, '/'))
            
            # Send the JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'images': image_files,
                'count': len(image_files),
                'timestamp': time.time(),
                'images_dir': images_dir
            }
            
            logger.info(f"Found {len(image_files)} images in {images_dir}: {image_files}")
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            logger.error(f"Error listing images: {str(e)}")
            self._serve_500(str(e))
    
    def _serve_image(self, image_name):
        """Serve a specific image file"""
        try:
            images_dir = self.server.images_dir
            logger.info(f"Serving image: {image_name} from {images_dir}")
            
            # Handle URL encoding and convert forward slashes to OS path separators
            image_name = image_name.replace('/', os.sep)
            file_path = os.path.join(images_dir, image_name)
            logger.info(f"Full file path: {file_path}")
            
            # Security check - prevent directory traversal
            if not os.path.normpath(file_path).startswith(os.path.normpath(images_dir)):
                logger.warning(f"Security check failed for path: {file_path}")
                self._serve_403()
                return
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                logger.warning(f"File not found: {file_path}")
                self._serve_404()
                return
                
            # Determine content type based on file extension
            content_type = 'image/jpeg'  # Default
            if image_name.lower().endswith('.png'):
                content_type = 'image/png'
            elif image_name.lower().endswith('.gif'):
                content_type = 'image/gif'
            
            # Send the image
            with open(file_path, 'rb') as f:
                image_data = f.read()
            
            logger.info(f"Serving image {image_name}, size: {len(image_data)} bytes")
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', str(len(image_data)))
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.end_headers()
            self.wfile.write(image_data)
            
        except Exception as e:
            logger.error(f"Error serving image {image_name}: {str(e)}")
            self._serve_500(str(e))
    
    def _serve_404(self):
        """Serve a 404 Not Found error"""
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'404 Not Found')
    
    def _serve_403(self):
        """Serve a 403 Forbidden error"""
        self.send_response(403)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'403 Forbidden')
    
    def _serve_500(self, error_msg="Server error"):
        """Serve a 500 Internal Server Error"""
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"500 Internal Server Error: {error_msg}".encode('utf-8'))

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    def __init__(self, server_address, RequestHandlerClass, images_dir):
        super().__init__(server_address, RequestHandlerClass)
        self.images_dir = images_dir

def start_server(host='0.0.0.0', port=8000, images_dir='/app/images/'):
    """Start the HTTP server for streaming images"""
    try:
        # Create custom server with additional parameters
        server = ThreadedHTTPServer((host, port), ImageHandler, images_dir)
        
        # Start server in a separate thread
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True  # Exit when main thread exits
        server_thread.start()
        
        logger.info(f"Image streaming server started on http://{host}:{port}")
        return server
        
    except Exception as e:
        logger.error(f"Failed to start streaming server: {str(e)}")
        return None

def update_latest_frame(frame):
    """Update the latest frame for streaming"""
    global latest_frame
    with frame_lock:
        latest_frame = frame.copy()

def stop_server(server):
    """Stop the HTTP server"""
    if server:
        server.shutdown()
        server.server_close()
        logger.info("Image streaming server stopped")