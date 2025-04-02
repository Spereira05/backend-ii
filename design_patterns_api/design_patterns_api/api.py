from fastapi import FastAPI
from payments import PaymentService, PaymentGateway

api = FastAPI()

@api.get("/")
def index():
    return "Hello"
    
def paypal_payment():
    pass
    
def gpay_payment():
    pass
    
def applepay_payment():
    pass
    
def mbway_payment():
    pass
    
@api.post("/pay")
def process_payment(method:str):
    payment_service: PaymentService = PaymentGateway.build(method=method)
    payment_service.process()
    # match method.lower():
    #     case "paypal":
    #         paypal_payment()
    #     case "gpay":
    #         gpay_payment()
    #     case "applepay":
    #         applepay_payment()
    #     case "mbway":
    #         mbway_payment()
            