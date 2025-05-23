# Exercise 14: Simple AI Agent with CrewAI

from typing import Dict, Any
from crewai import Agent, Task, Crew

class SimpleMessageAgent:
    """
    A simple agent class that returns predefined messages for specific inputs.
    This demonstrates the basic concept without CrewAI dependencies.
    """
    def __init__(self, name: str, responses: Dict[str, str] = None):
        self.name = name
        self.responses = responses or {}
        self.default_message = "I don't have a specific response for that input."
    
    def respond(self, input_text: str) -> str:
        """Return a predefined response based on the input text"""
        # Check if we have a direct match
        if input_text in self.responses:
            return self.responses[input_text]
        
        # Check for partial matches (case insensitive)
        input_lower = input_text.lower()
        for key, response in self.responses.items():
            if key.lower() in input_lower:
                return response
        
        # Return default message if no match found
        return self.default_message

def demonstrate_simple_agent():
    """Demonstrate the simple agent without CrewAI"""
    # Create a simple agent with predefined responses
    assistant = SimpleMessageAgent(
        name="Assistant",
        responses={
            "hello": "Hello! How can I assist you today?",
            "how are you": "I'm functioning well, thank you for asking!",
            "weather": "I don't have access to current weather information.",
            "help": "I can respond to greetings and basic questions. What do you need help with?",
            "bye": "Goodbye! Have a great day!"
        }
    )
    
    # Test the agent with different inputs
    test_inputs = [
        "hello",
        "How are you doing today?",
        "What's the weather like?",
        "I need some help",
        "This is a random statement",
        "bye"
    ]
    
    print("Simple Agent Demo:")
    print("=" * 50)
    for input_text in test_inputs:
        response = assistant.respond(input_text)
        print(f"Input: {input_text}")
        print(f"Response: {response}")
        print("-" * 50)

def demonstrate_crewai_agent():
    """Demonstrate a simple CrewAI agent"""
    try:
        # Define a CrewAI agent
        agent = Agent(
            role="Assistant",
            goal="Provide helpful responses to user queries",
            backstory="I am a helpful AI assistant created to demonstrate basic agent functionality.",
            verbose=True
        )
        
        # Define a task for the agent
        task = Task(
            description="Respond to the user's greeting with a friendly message",
            expected_output="A friendly greeting response",
            agent=agent
        )
        
        # Create a crew with just this agent
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=2
        )
        
        # Run the crew
        result = crew.kickoff()
        
        print("\nCrewAI Agent Demo:")
        print("=" * 50)
        print(f"Task Result: {result}")
        
    except ImportError:
        print("\nCrewAI Agent Demo:")
        print("=" * 50)
        print("CrewAI is not installed. To use CrewAI, install it with:")
        print("pip install crewai")

if __name__ == "__main__":
    # Demonstrate the simple agent
    demonstrate_simple_agent()
    
    # Try to demonstrate the CrewAI agent
    # This will work if CrewAI is installed, otherwise show installation instructions
    print("\n")
    demonstrate_crewai_agent()