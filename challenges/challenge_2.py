from abc import ABC, abstractmethod
class Observer:
    def update(self, state):
        print(f"Observer: state updated to {state}")
        
class AbstractSubject(ABC):
    
    @abstractmethod
    def attach(self, observer) -> None:
        pass
        
    @abstractmethod
    def detach(self, observer) -> None:
       pass
    
    @abstractmethod
    def notify(self) -> None:
        pass
   
class Subject(AbstractSubject):
    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify()
    

subject = Subject()

observer1 = Observer()
observer2 = Observer()

subject.attach(observer1)
subject.attach(observer2)

subject.set_state("New State 1")  
subject.set_state("New State 2")  