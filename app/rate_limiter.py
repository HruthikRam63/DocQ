from time import time
from fastapi import HTTPException

# In-memory rate limiter (For simplicity, in a real-world scenario, you can use a more robust solution)
requests = {}

def rate_limiter(func):
    """Rate limiting decorator to limit requests to 5 per minute per IP."""
    def wrapper(websocket, *args, **kwargs):
        client_ip = websocket.client.host  # Get the client's IP address
        current_time = time()
        
        # Initialize the request count if it's the first time
        if client_ip not in requests:
            requests[client_ip] = []
        
        # Clean up old requests (older than 60 seconds)
        requests[client_ip] = [t for t in requests[client_ip] if current_time - t < 60]
        
        # Check if the request count exceeds the limit
        if len(requests[client_ip]) >= 5:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
        
        # Record the new request time
        requests[client_ip].append(current_time)
        
        return func(websocket, *args, **kwargs)
    
    return wrapper
