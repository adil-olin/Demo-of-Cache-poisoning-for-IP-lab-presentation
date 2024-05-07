from http.server import SimpleHTTPRequestHandler, HTTPServer
import hashlib
import json
from urllib.parse import urlparse, parse_qs


class CachingHandler(SimpleHTTPRequestHandler):
    cache = {}

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Compute a cache key based on the request path and parameters
        cache_key = hashlib.sha256(self.path.encode()).hexdigest()

        # Check if the response is already in the cache
        if cache_key in self.cache:
            # Return the cached response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self.cache[cache_key]).encode())
            print(f"Serving cached response for: {self.path}")
        else:
            # Generate a new response and cache it
            response_data = {
                "message": f"Hello, you accessed {self.path}",
                "status": "success"
            }
            self.cache[cache_key] = response_data

            # Send the response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            print(f"Generated and cached response for: {self.path}")

    def do_PUT(self):
        # Parse the path and query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Compute the cache key based on the request path and parameters
        cache_key = hashlib.sha256(self.path.encode()).hexdigest()

        # Read the length of the content from the headers
        content_length = int(self.headers['Content-Length'])

        # Read the payload from the request body
        post_data = self.rfile.read(content_length)

        # Parse the JSON data
        response_data = json.loads(post_data)

        # Inject the response into the cache
        self.cache[cache_key] = response_data

        # Send a success response
        self.send_response(200)
        self.end_headers()
        print(f"Injected custom response into cache for: {self.path}")


if __name__ == "__main__":
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, CachingHandler)
    print("Starting HTTP server on port 8080...")
    httpd.serve_forever()

