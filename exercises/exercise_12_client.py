import grpc
import math_pb2
import math_pb2_grpc
import sys

def run_client(number):
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = math_pb2_grpc.MathServiceStub(channel)
        
        # Create a request
        request = math_pb2.CubeRequest(number=number)
        
        try:
            # Make the call
            response = stub.Cube(request)
            print(f"Result from server: {number}³ = {response.result}")
            return response.result
        except grpc.RpcError as e:
            print(f"RPC error: {e.code()}")
            print(f"Details: {e.details()}")

if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Please provide a number to calculate its cube.")
        print("Usage: python exercise_12_client.py <number>")
        sys.exit(1)
    
    try:
        number = float(sys.argv[1])
        run_client(number)
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid number")