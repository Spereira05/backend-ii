from typing import Protocol 

class PaymentService(Protocol):
    def process(*args, **kwargs):
        
        return NotImplementedError
            
class MbWayService(PaymentService):
    def foo():
        pass
        
    def process(*args, **kwargs):
        raise NotImplementedError
            
class AppleService(PaymentService):
    def foo():
        pass
        
    def process(*args, **kwargs):
        raise NotImplementedError
            
class GPayService(PaymentService):
    def foo():
        pass
        
    def process(*args, **kwargs):
        raise NotImplementedError
            
class PayPalService(PaymentService):
    def foo():
        pass
        
    def process(*args, **kwargs):
        raise NotImplementedError
            
class PaymentGateway:
    registry = {
        "applepay": PayPalService,
        "paypal": AppleService,
    }
    
    @classmethod
    def build(cls, method:str) -> PaymentService:
        return cls.registry.get(method, None)()