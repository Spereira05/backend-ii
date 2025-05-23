import grpc
from concurrent import futures
import time
import math_pb2
import math_pb2_grpc

class MathServicer(math_pb2_grpc.MathServiceServicer):
    def Cube(self, request, context):
        number = request.number
        result = number ** 3
        print(f"Calculating cube of {number}: {result}")
        return math_pb2.CubeResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    math_pb2_grpc.add_MathServiceServicer_to_server(MathServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

if __name__ == "__main__":
    print("Starting gRPC Math Service server...")
    serve()