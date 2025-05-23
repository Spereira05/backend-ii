import grpc
import sys
import time
import challenge_12_pb2
import challenge_12_pb2_grpc

def run_primes_client(limit):
    """Client function to request prime numbers"""
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = challenge_12_pb2_grpc.CalculatorServiceStub(channel)
        
        print(f"Requesting prime numbers up to {limit}...")
        request = challenge_12_pb2.PrimeRequest(limit=limit)
        
        try:
            responses = stub.GeneratePrimes(request)
            print(f"Prime numbers up to {limit}:")
            for response in responses:
                print(f"Prime #{response.position}: {response.prime}")
        except grpc.RpcError as e:
            print(f"RPC error: {e.code()}")
            print(f"Details: {e.details()}")

def run_fibonacci_client(terms):
    """Client function to request Fibonacci numbers"""
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = challenge_12_pb2_grpc.CalculatorServiceStub(channel)
        
        print(f"Requesting {terms} Fibonacci numbers...")
        request = challenge_12_pb2.FibonacciRequest(terms=terms)
        
        try:
            responses = stub.GenerateFibonacci(request)
            print(f"Fibonacci sequence ({terms} terms):")
            for response in responses:
                print(f"Fibonacci #{response.position}: {response.number}")
        except grpc.RpcError as e:
            print(f"RPC error: {e.code()}")
            print(f"Details: {e.details()}")

def run_factorial_client(number):
    """Client function to request factorial calculation"""
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = challenge_12_pb2_grpc.CalculatorServiceStub(channel)
        
        print(f"Requesting factorial of {number}...")
        request = challenge_12_pb2.FactorialRequest(number=number)
        
        try:
            responses = stub.CalculateFactorial(request)
            print(f"Factorial calculation steps for {number}!:")
            for response in responses:
                print(f"{response.step}! = {response.result}")
                if response.is_final:
                    print(f"\nFinal result: {number}! = {response.result}")
        except grpc.RpcError as e:
            print(f"RPC error: {e.code()}")
            print(f"Details: {e.details()}")

def print_usage():
    print("Usage:")
    print("  python challenge_12_client.py primes <limit>")
    print("  python challenge_12_client.py fibonacci <terms>")
    print("  python challenge_12_client.py factorial <number>")
    print("\nExamples:")
    print("  python challenge_12_client.py primes 50")
    print("  python challenge_12_client.py fibonacci 10")
    print("  python challenge_12_client.py factorial 5")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        value = int(sys.argv[2])
        
        if command == "primes":
            run_primes_client(value)
        elif command == "fibonacci":
            run_fibonacci_client(value)
        elif command == "factorial":
            run_factorial_client(value)
        else:
            print(f"Unknown command: {command}")
            print_usage()
    except ValueError:
        print(f"Error: '{sys.argv[2]}' is not a valid integer")
        print_usage()