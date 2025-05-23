import grpc
from concurrent import futures
import time
import math
from challenge_12_pb2 import PrimeResponse, FibonacciResponse, FactorialResponse
import challenge_12_pb2_grpc

class CalculatorServicer(challenge_12_pb2_grpc.CalculatorServiceServicer):
    def GeneratePrimes(self, request, context):
        """
        Generate prime numbers up to the limit and stream them back to the client.
        """
        limit = request.limit
        print(f"Generating prime numbers up to {limit}")
        
        if limit < 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Limit must be at least 2, got {limit}")
            return
            
        count = 0
        for number in range(2, limit + 1):
            if self._is_prime(number):
                count += 1
                yield PrimeResponse(prime=number, position=count)
                time.sleep(0.1)  # Simulate some processing time
        
        print(f"Generated {count} prime numbers")
    
    def GenerateFibonacci(self, request, context):
        """
        Generate Fibonacci sequence up to the specified number of terms.
        """
        terms = request.terms
        print(f"Generating {terms} Fibonacci numbers")
        
        if terms < 1:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Number of terms must be positive, got {terms}")
            return
            
        if terms == 1:
            yield FibonacciResponse(number=0, position=1)
            return
            
        # First two terms
        a, b = 0, 1
        yield FibonacciResponse(number=a, position=1)
        yield FibonacciResponse(number=b, position=2)
        
        # Generate remaining terms
        for i in range(3, terms + 1):
            a, b = b, a + b
            yield FibonacciResponse(number=b, position=i)
            time.sleep(0.1)  # Simulate some processing time
        
        print(f"Generated {terms} Fibonacci numbers")
    
    def CalculateFactorial(self, request, context):
        """
        Calculate factorial and stream intermediate results.
        """
        number = request.number
        print(f"Calculating factorial of {number}")
        
        if number < 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Cannot calculate factorial of negative number {number}")
            return
            
        if number == 0 or number == 1:
            yield FactorialResponse(result=1, step=number, is_final=True)
            return
            
        result = 1
        for i in range(1, number + 1):
            result *= i
            is_final = (i == number)
            yield FactorialResponse(result=result, step=i, is_final=is_final)
            time.sleep(0.1)  # Simulate some processing time
        
        print(f"Factorial of {number} is {result}")
    
    def _is_prime(self, n):
        """
        Check if a number is prime.
        """
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    challenge_12_pb2_grpc.add_CalculatorServiceServicer_to_server(
        CalculatorServicer(), server
    )
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Calculator streaming server started on port 50052...")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

if __name__ == "__main__":
    serve()