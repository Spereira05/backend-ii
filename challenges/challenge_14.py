# Challenge 14: Enhanced AI Agent with Keyword Matching

from typing import Dict, List, Tuple, Any, Optional
import re
import json
import random
import time
from datetime import datetime

class EnhancedAgent:
    """
    An enhanced AI agent that handles multiple queries with different responses
    based on keyword matching, context awareness, and state management.
    """
    def __init__(self, name: str, personality: str = "helpful"):
        self.name = name
        self.personality = personality
        self.knowledge_base = {}
        self.conversation_history = []
        self.session_start = datetime.now()
        self.state = {
            "mood": "neutral",
            "topics_discussed": set(),
            "user_preferences": {},
            "context": {}
        }
        
        # Load default responses
        self._load_default_responses()
    
    def _load_default_responses(self):
        """Initialize the agent with default response patterns"""
        self.knowledge_base = {
            "greeting": {
                "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"],
                "responses": [
                    "Hello! How can I assist you today?",
                    "Hi there! What can I help you with?",
                    "Greetings! How may I be of service?",
                    "Hello! I'm here to help. What do you need?"
                ],
                "context_required": False
            },
            "farewell": {
                "keywords": ["bye", "goodbye", "see you", "farewell", "later", "end conversation"],
                "responses": [
                    "Goodbye! Have a great day!",
                    "Farewell! Feel free to return if you have more questions.",
                    "See you later! It was nice chatting with you.",
                    "Until next time! Take care!"
                ],
                "context_required": False
            },
            "gratitude": {
                "keywords": ["thank", "thanks", "appreciate", "grateful"],
                "responses": [
                    "You're welcome! Is there anything else I can help with?",
                    "Happy to help! Let me know if you need anything more.",
                    "My pleasure! Any other questions?",
                    "Glad I could assist! What else would you like to know?"
                ],
                "context_required": False
            },
            "weather": {
                "keywords": ["weather", "temperature", "forecast", "rain", "sunny", "snow", "climate"],
                "responses": [
                    "I don't have access to real-time weather data, but I'd be happy to discuss weather concepts!",
                    "While I can't check the current forecast, I can explain weather phenomena if you're interested.",
                    "I don't have weather information, but I can talk about climate patterns if you'd like.",
                    "I can't provide current weather updates, but I can discuss meteorology topics if that helps."
                ],
                "context_required": False
            },
            "time": {
                "keywords": ["time", "date", "day", "today", "current time"],
                "responses": [
                    f"The current time is {datetime.now().strftime('%H:%M')} and today is {datetime.now().strftime('%A, %B %d, %Y')}.",
                    f"It's {datetime.now().strftime('%H:%M')} on {datetime.now().strftime('%A, %B %d, %Y')}.",
                    f"Today is {datetime.now().strftime('%A, %B %d')} and the time is {datetime.now().strftime('%H:%M')}.",
                    f"Right now it's {datetime.now().strftime('%H:%M %p on %A, %B %d, %Y')}."
                ],
                "context_required": False,
                "dynamic": True
            },
            "help": {
                "keywords": ["help", "assist", "support", "guide", "confused", "how do you work"],
                "responses": [
                    "I can respond to various queries about different topics. Just ask me a question, and I'll try to help!",
                    "I'm designed to understand keywords in your messages and provide relevant responses. What do you need help with?",
                    "I can discuss weather concepts, provide the time, answer questions, and much more. What would you like to know?",
                    "I'm here to assist with information and engage in conversation. Feel free to ask me anything!"
                ],
                "context_required": False
            },
            "capabilities": {
                "keywords": ["what can you do", "your abilities", "your capabilities", "your functions"],
                "responses": [
                    "I can understand context, remember our conversation, recognize keywords, and provide helpful responses on various topics.",
                    "I'm designed to maintain conversation context, remember details you've shared, and respond to a variety of topics based on keywords.",
                    "My capabilities include contextual understanding, conversation memory, keyword recognition, and providing informative responses.",
                    "I can engage in contextual conversations, remember previous exchanges, and respond to various queries based on keyword matching."
                ],
                "context_required": False
            }
        }
    
    def add_topic(self, topic: str, keywords: List[str], responses: List[str], context_required: bool = False, dynamic: bool = False):
        """Add a new topic to the agent's knowledge base"""
        if topic in self.knowledge_base:
            # Update existing topic
            self.knowledge_base[topic]["keywords"].extend([k for k in keywords if k not in self.knowledge_base[topic]["keywords"]])
            self.knowledge_base[topic]["responses"].extend(responses)
        else:
            # Create new topic
            self.knowledge_base[topic] = {
                "keywords": keywords,
                "responses": responses,
                "context_required": context_required,
                "dynamic": dynamic
            }
        return f"Topic '{topic}' has been added to my knowledge base with {len(keywords)} keywords and {len(responses)} responses."
    
    def respond(self, query: str) -> str:
        """Process the query and generate an appropriate response"""
        # Record the query in conversation history
        self.conversation_history.append({"role": "user", "message": query, "timestamp": datetime.now()})
        
        # Normalize the query
        normalized_query = query.lower().strip()
        
        # Check for exact commands
        if normalized_query == "reset conversation":
            self.reset_conversation()
            return "Conversation has been reset. How can I help you today?"
        
        if normalized_query == "list topics":
            return self._list_topics()
        
        if normalized_query.startswith("tell me about your state"):
            return self._report_state()
        
        # Find matching topics based on keywords
        matched_topics = self._match_topics(normalized_query)
        
        # Generate response
        response = self._generate_response(matched_topics, normalized_query)
        
        # Update state
        self._update_state(normalized_query, matched_topics)
        
        # Record the response in conversation history
        self.conversation_history.append({"role": "assistant", "message": response, "timestamp": datetime.now()})
        
        return response
    
    def _match_topics(self, query: str) -> List[Tuple[str, float]]:
        """
        Match the query against topics in the knowledge base and return
        a list of matched topics with confidence scores.
        """
        matched_topics = []
        
        for topic, data in self.knowledge_base.items():
            highest_confidence = 0
            
            # Check each keyword in the topic
            for keyword in data["keywords"]:
                # Direct match
                if keyword in query:
                    confidence = len(keyword) / len(query) * 0.8
                    highest_confidence = max(highest_confidence, confidence)
                
                # Check for partial matches
                elif len(keyword) > 3 and any(part in query for part in keyword.split()):
                    confidence = 0.4
                    highest_confidence = max(highest_confidence, confidence)
            
            # If we have a match with non-zero confidence
            if highest_confidence > 0:
                # Boost confidence for topics in the current context
                if topic in self.state["topics_discussed"]:
                    highest_confidence += 0.1
                
                matched_topics.append((topic, highest_confidence))
        
        # Sort by confidence score in descending order
        return sorted(matched_topics, key=lambda x: x[1], reverse=True)
    
    def _generate_response(self, matched_topics: List[Tuple[str, float]], query: str) -> str:
        """Generate a response based on matched topics and context"""
        # If no topics matched
        if not matched_topics:
            return self._fallback_response(query)
        
        # Get the highest confidence topic
        top_topic, confidence = matched_topics[0]
        
        # If confidence is too low, use fallback
        if confidence < 0.3:
            return self._fallback_response(query)
        
        # Get responses for the top topic
        responses = self.knowledge_base[top_topic]["responses"]
        
        # If the topic has dynamic responses, refresh them
        if self.knowledge_base[top_topic].get("dynamic", False):
            if top_topic == "time":
                responses = [
                    f"The current time is {datetime.now().strftime('%H:%M')} and today is {datetime.now().strftime('%A, %B %d, %Y')}.",
                    f"It's {datetime.now().strftime('%H:%M')} on {datetime.now().strftime('%A, %B %d, %Y')}.",
                    f"Today is {datetime.now().strftime('%A, %B %d')} and the time is {datetime.now().strftime('%H:%M')}.",
                    f"Right now it's {datetime.now().strftime('%H:%M %p on %A, %B %d, %Y')}."
                ]
        
        # Select a response, avoiding the last used response for this topic if possible
        last_response = None
        if self.conversation_history:
            for entry in reversed(self.conversation_history):
                if entry["role"] == "assistant" and top_topic in self.state["topics_discussed"]:
                    last_response = entry["message"]
                    break
        
        if len(responses) > 1 and last_response in responses:
            filtered_responses = [r for r in responses if r != last_response]
            response = random.choice(filtered_responses)
        else:
            response = random.choice(responses)
        
        # Add context-awareness for more natural conversations
        if len(self.conversation_history) >= 4:  # We have some conversation history
            if top_topic == "greeting" and any(topic[0] == "greeting" for topic in matched_topics[1:]):
                # This is a repeated greeting
                return "We've already greeted each other. What can I help you with today?"
        
        return response
    
    def _fallback_response(self, query: str) -> str:
        """Generate a fallback response when no topics match"""
        fallbacks = [
            "I'm not sure I understand. Could you rephrase that?",
            "I don't have specific information about that. Is there something else I can help with?",
            "That's beyond my current capabilities. Would you like to discuss something else?",
            "I don't have enough knowledge to respond to that properly. Can you try a different question?",
            f"I don't have a specific response for '{query}'. Would you like to know what topics I can discuss?"
        ]
        
        # If this is the second consecutive fallback, offer topics
        consecutive_fallbacks = 0
        for entry in reversed(self.conversation_history):
            if entry["role"] == "assistant" and any(fb in entry["message"] for fb in fallbacks):
                consecutive_fallbacks += 1
            else:
                break
        
        if consecutive_fallbacks >= 1:
            return f"I'm still not understanding. Here are topics I can discuss: {', '.join(self.knowledge_base.keys())}. Which would you like to talk about?"
        
        return random.choice(fallbacks)
    
    def _update_state(self, query: str, matched_topics: List[Tuple[str, float]]):
        """Update the agent's state based on the current query and matched topics"""
        # Update topics discussed
        for topic, confidence in matched_topics:
            if confidence > 0.3:
                self.state["topics_discussed"].add(topic)
        
        # Update context based on query content
        # This is a simplified version - in a real system, you'd use NLP to extract entities
        if "favorite" in query.lower():
            parts = query.lower().split("favorite")
            if len(parts) > 1:
                preference_type = parts[1].strip().split()[0]
                self.state["user_preferences"][f"favorite_{preference_type}"] = "mentioned"
        
        # Update mood based on query sentiment (simplified)
        if any(word in query.lower() for word in ["happy", "great", "excellent", "good", "thanks"]):
            self.state["mood"] = "positive"
        elif any(word in query.lower() for word in ["sad", "bad", "terrible", "awful", "sorry"]):
            self.state["mood"] = "negative"
        else:
            self.state["mood"] = "neutral"
    
    def _list_topics(self) -> str:
        """Return a list of available topics"""
        topics = list(self.knowledge_base.keys())
        return f"I can discuss the following topics: {', '.join(topics)}. What would you like to talk about?"
    
    def _report_state(self) -> str:
        """Return a report of the agent's current state"""
        topics = ", ".join(self.state["topics_discussed"]) if self.state["topics_discussed"] else "None yet"
        preferences = ", ".join(f"{k}: {v}" for k, v in self.state["user_preferences"].items()) if self.state["user_preferences"] else "None noted"
        
        conversation_duration = datetime.now() - self.session_start
        minutes = int(conversation_duration.total_seconds() / 60)
        seconds = int(conversation_duration.total_seconds() % 60)
        
        return (
            f"Current State Report:\n"
            f"- Name: {self.name}\n"
            f"- Personality: {self.personality}\n"
            f"- Current mood: {self.state['mood']}\n"
            f"- Topics discussed: {topics}\n"
            f"- User preferences: {preferences}\n"
            f"- Session duration: {minutes} minutes, {seconds} seconds\n"
            f"- Conversation exchanges: {len(self.conversation_history) // 2}"
        )
    
    def reset_conversation(self):
        """Reset the conversation history and state while preserving knowledge"""
        self.conversation_history = []
        self.session_start = datetime.now()
        self.state = {
            "mood": "neutral",
            "topics_discussed": set(),
            "user_preferences": {},
            "context": {}
        }

# Demo function to test the agent
def demo_enhanced_agent():
    # Create the agent
    agent = EnhancedAgent(name="EnhancedBot")
    
    # Add some additional topics
    agent.add_topic(
        "python", 
        ["python", "programming", "code", "developer", "software"], 
        [
            "Python is a versatile programming language known for its readability and simplicity.",
            "As a developer, you might appreciate Python's extensive library ecosystem.",
            "Python is great for various applications including web development, data science, and automation.",
            "I can discuss Python programming concepts if you're interested in learning more."
        ]
    )
    
    agent.add_topic(
        "ai", 
        ["ai", "artificial intelligence", "machine learning", "ml", "neural network"], 
        [
            "Artificial Intelligence involves creating systems that can perform tasks requiring human intelligence.",
            "Machine Learning is a subset of AI focused on systems that can learn from data.",
            "Neural networks are computing systems inspired by biological neural networks in animal brains.",
            "The field of AI is advancing rapidly, with applications in various domains like healthcare, finance, and transportation."
        ]
    )
    
    # Simulated conversation
    conversation = [
        "Hello there!",
        "What can you do?",
        "Tell me about Python",
        "What about artificial intelligence?",
        "What time is it now?",
        "How's the weather today?",
        "Tell me about your state",
        "Thank you for the information",
        "Goodbye!"
    ]
    
    print("Enhanced Agent Demo:")
    print("=" * 60)
    
    for user_input in conversation:
        print(f"\nUser: {user_input}")
        response = agent.respond(user_input)
        print(f"Agent: {response}")
        time.sleep(1)  # Pause for readability
    
    print("\n" + "=" * 60)
    print("Demo completed!")

# Run the demo if the file is executed directly
if __name__ == "__main__":
    demo_enhanced_agent()