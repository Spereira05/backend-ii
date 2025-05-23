# Exercise 12: Basic gRPC Service for Cube Calculation

import grpc
from concurrent import futures
import time
import math
import sys

# Import the generated protocol buffer code
# In a real implementation, this would be imported from a compiled .proto file
# For this exercise, we'll define the service directly in Python

# Define service methods
class MathServicer:
    def Cube(self, request, context):
        number = request.number
        result = number ** 3
        return CubeResponse(result=result)

# Simple request/response classes to simulate protobuf messages
class CubeRequest:
    def __init__(self, number):
        self.number = number

class CubeResponse:
    def __init__(self, result):
        self.result = result

# Server implementation
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # In a real implementation, add_servicer_to_server would be used here
    # For this exercise, we'll implement a simple server manually
    
    print("gRPC Server starting on port 50051...")
    server.add_insecure_port('[::]:50051')
    server.start()
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

# Client implementation
def run_client(number):
    # In a real implementation, this would use actual gRPC channel
    # For this exercise, we'll simulate the client-server interaction
    
    print(f"Sending request to calculate cube of {number}")
    
    # Create servicer instance
    servicer = MathServicer()
    
    # Create request
    request = CubeRequest(number=number)
    
    # Call method directly (in real gRPC this would go through the network)
    response = servicer.Cube(request, None)
    
    print(f"Received response: {number}³ = {response.result}")
    return response.result

def main():
    # Parse command-line arguments
    args = sys.argv[1:]
    
    if not args or args[0] == "server":
        print("Starting gRPC server...")
        print("In a real implementation, this would start a proper gRPC server.")
        print("Press Ctrl+C to stop the server.")
        serve()
    elif args[0] == "client":
        if len(args) < 2:
            print("Please provide a number to calculate its cube.")
            print("Usage: python exercise_12.py client <number>")
            return
        
        try:
            number = float(args[1])
            run_client(number)
        except ValueError:
            print(f"Error: '{args[1]}' is not a valid number")
    else:
        print("Unknown command. Use 'server' or 'client <number>'")

if __name__ == "__main__":
    print("gRPC Cube Calculator")
    print("This is a simplified implementation for demonstration purposes.")
    print("In a real implementation, protobuf and actual gRPC libraries would be used.")
    print("--------------------------------------------")
    print("Commands:")
    print("  - Run server: python exercise_12.py server")
    print("  - Run client: python exercise_12.py client <number>")
    print("--------------------------------------------")
    
    main()