# Challenge 15: Advanced AI Agent with Multiple Data Sources

import requests
import os
import json
import re
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import random

class MultiSourceAgent:
    """
    An advanced AI agent that can handle complex queries and respond with relevant information
    from multiple external data sources.
    """
    
    def __init__(self, name: str = "MultiAgent"):
        self.name = name
        self.api_keys = {}
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 30 * 60  # 30 minutes default
        self.conversation_history = []
        self.sources = {
            "weather": self._get_weather_data,
            "news": self._get_news_data,
            "stocks": self._get_stock_data,
            "crypto": self._get_crypto_data,
            "wikipedia": self._get_wikipedia_data,
            "translation": self._translate_text
        }
        
    def set_api_key(self, service: str, api_key: str) -> None:
        """Set API key for a specific service"""
        self.api_keys[service] = api_key
        print(f"API key for {service} has been set.")
    
    def set_cache_duration(self, seconds: int) -> None:
        """Set how long to cache responses"""
        self.cache_duration = seconds
        print(f"Cache duration set to {seconds} seconds.")
    
    def respond(self, query: str) -> str:
        """
        Main method to respond to user queries by analyzing the query,
        identifying the required data sources, fetching data, and
        generating a comprehensive response.
        """
        # Log the query
        query_time = datetime.now()
        self.conversation_history.append({"role": "user", "message": query, "timestamp": query_time})
        
        # Process the query
        query_analysis = self._analyze_query(query)
        if query_analysis["type"] == "error":
            response = query_analysis["message"]
        elif query_analysis["type"] == "help":
            response = self._get_help_message()
        elif query_analysis["type"] == "data":
            response = self._process_data_query(query_analysis)
        else:
            response = "I'm not sure how to process your query. Try asking about weather, news, stocks, cryptocurrency, or information from Wikipedia."
        
        # Log the response
        self.conversation_history.append({"role": "assistant", "message": response, "timestamp": datetime.now()})
        
        return response
    
    def _get_help_message(self) -> str:
        """Generate a help message explaining the agent's capabilities"""
        return (
            "I'm a multi-source information agent that can help you with various types of data. Here's what I can do:\n\n"
            "🌤️ Weather Information: Ask about weather in any location\n"
            "📰 News Updates: Get the latest headlines, optionally filtered by topic\n"
            "📈 Stock Market Data: Check current prices and changes for stocks\n"
            "🪙 Cryptocurrency Information: Get prices and trends for major cryptocurrencies\n"
            "📚 General Knowledge: Get information about various topics from Wikipedia\n"
            "🌐 Translation: Translate text between different languages\n\n"
            "You can ask me things like:\n"
            "- \"What's the weather in Paris?\"\n"
            "- \"Tell me the latest technology news\"\n"
            "- \"What's the current price of AAPL stock?\"\n"
            "- \"How much is Bitcoin worth right now?\"\n"
            "- \"What is quantum computing?\"\n"
            "- \"Translate 'hello' to Spanish\"\n\n"
            "You can also ask for combinations like \"What's the weather in London and give me the latest news\""
        )
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze the query to determine its type and relevant data sources"""
        query = query.lower().strip()
        
        # Check for help queries
        if re.search(r'\b(help|assist|support|what can you do|your capabilities)\b', query):
            return {"type": "help"}
        
        # Check for weather queries
        if re.search(r'\b(weather|temperature|forecast|rain|sunny|snow|climate)\b', query):
            location_match = re.search(r'(?:in|at|for)\s+([a-zA-Z\s,]+)(?:\?)?$', query)
            location = location_match.group(1).strip() if location_match else None
            
            if not location:
                location_match = re.search(r'\b([a-zA-Z]+(?:\s+[a-zA-Z]+)*)\s+weather\b', query)
                location = location_match.group(1).strip() if location_match else None
            
            if not location:
                return {"type": "error", "message": "I couldn't determine which location you want weather information for. Please specify a city or location."}
            
            return {
                "type": "data",
                "sources": ["weather"],
                "params": {"location": location}
            }
        
        # Check for news queries
        if re.search(r'\b(news|headlines|current events|latest articles)\b', query):
            topic_match = re.search(r'(?:about|on|regarding)\s+([a-zA-Z\s]+)(?:\?)?$', query)
            topic = topic_match.group(1).strip() if topic_match else None
            
            return {
                "type": "data",
                "sources": ["news"],
                "params": {"topic": topic}
            }
        
        # Check for stock market queries
        if re.search(r'\b(stock|stocks|share price|market|ticker|nyse|nasdaq)\b', query):
            symbol_match = re.search(r'\b([A-Z]{1,5})\b', query)
            symbol = symbol_match.group(1) if symbol_match else None
            
            if not symbol:
                company_match = re.search(r'(?:for|of)\s+([a-zA-Z\s]+)(?:\?)?$', query)
                company = company_match.group(1).strip() if company_match else None
                
                if company:
                    # In a real implementation, you would look up the company symbol
                    symbol = "EXAMPLE"
            
            if not symbol:
                return {"type": "error", "message": "I couldn't determine which stock symbol you're interested in. Please specify a stock symbol like AAPL for Apple."}
            
            return {
                "type": "data",
                "sources": ["stocks"],
                "params": {"symbol": symbol}
            }
        
        # Check for cryptocurrency queries
        if re.search(r'\b(crypto|cryptocurrency|bitcoin|ethereum|coin|token|blockchain)\b', query):
            coin_match = re.search(r'\b(bitcoin|btc|ethereum|eth|dogecoin|doge|litecoin|ltc|cardano|ada|ripple|xrp)\b', query, re.IGNORECASE)
            coin = coin_match.group(1).lower() if coin_match else None
            
            if not coin:
                return {"type": "error", "message": "I couldn't determine which cryptocurrency you're interested in. Please specify one like Bitcoin or Ethereum."}
            
            # Standardize coin identifiers
            coin_map = {
                "bitcoin": "btc", "btc": "btc", 
                "ethereum": "eth", "eth": "eth",
                "dogecoin": "doge", "doge": "doge",
                "litecoin": "ltc", "ltc": "ltc",
                "cardano": "ada", "ada": "ada",
                "ripple": "xrp", "xrp": "xrp"
            }
            
            return {
                "type": "data",
                "sources": ["crypto"],
                "params": {"coin": coin_map.get(coin, coin)}
            }
        
        # Check for Wikipedia/information queries
        if re.search(r'\b(what is|who is|tell me about|information on|wikipedia|define|meaning of)\b', query):
            topic_match = re.search(r'(?:what is|who is|tell me about|information on|define|meaning of)\s+([a-zA-Z0-9\s]+)(?:\?)?$', query)
            topic = topic_match.group(1).strip() if topic_match else None
            
            if not topic:
                return {"type": "error", "message": "I couldn't determine what topic you're asking about. Please clarify your question."}
            
            return {
                "type": "data",
                "sources": ["wikipedia"],
                "params": {"topic": topic}
            }
        
        # Check for translation queries
        if re.search(r'\b(translate|translation|convert|say in)\b', query):
            text_match = re.search(r'translate\s+"([^"]+)"\s+(?:from\s+([a-zA-Z]+)\s+)?(?:to|into)\s+([a-zA-Z]+)', query)
            if not text_match:
                text_match = re.search(r'translate\s+([^"]+)\s+(?:from\s+([a-zA-Z]+)\s+)?(?:to|into)\s+([a-zA-Z]+)', query)
            
            if text_match:
                text = text_match.group(1).strip()
                source_lang = text_match.group(2) if text_match.group(2) else "auto"
                target_lang = text_match.group(3)
                
                return {
                    "type": "data",
                    "sources": ["translation"],
                    "params": {
                        "text": text,
                        "source_lang": source_lang,
                        "target_lang": target_lang
                    }
                }
            else:
                return {"type": "error", "message": "I couldn't understand your translation request. Please use a format like 'translate \"hello\" to Spanish'."}
        
        # Multi-source queries (complex)
        if re.search(r'\b(compare|both|combination|together|and also)\b', query):
            if re.search(r'\b(weather|temperature).+\b(news|headlines)\b', query) or re.search(r'\b(news|headlines).+\b(weather|temperature)\b', query):
                location_match = re.search(r'(?:in|at|for)\s+([a-zA-Z\s,]+)(?:\?)?$', query)
                location = location_match.group(1).strip() if location_match else "New York"
                
                return {
                    "type": "data",
                    "sources": ["weather", "news"],
                    "params": {"location": location}
                }
        
        # Default fallback
        return {"type": "error", "message": "I'm not sure what information you're looking for. Try asking about weather, news, stocks, cryptocurrency, or information from Wikipedia."}
    
    def _process_data_query(self, query_analysis: Dict[str, Any]) -> str:
        """Process a data query by fetching from required sources and formatting a response"""
        sources = query_analysis["sources"]
        params = query_analysis.get("params", {})
        
        results = {}
        for source in sources:
            if source in self.sources:
                results[source] = self.sources[source](params)
        
        # Combine results into a coherent response
        if len(results) == 1:
            # Single source response
            source = sources[0]
            if "error" in results[source]:
                return f"Sorry, I couldn't retrieve {source} information: {results[source]['error']}"
            
            if source == "weather":
                return self._format_weather_response(results[source])
            elif source == "news":
                return self._format_news_response(results[source])
            elif source == "stocks":
                return self._format_stock_response(results[source])
            elif source == "crypto":
                return self._format_crypto_response(results[source])
            elif source == "wikipedia":
                return self._format_wikipedia_response(results[source])
            elif source == "translation":
                return self._format_translation_response(results[source])
        else:
            # Multi-source response
            response_parts = []
            
            if "weather" in results and "news" in results:
                weather_data = results["weather"]
                news_data = results["news"]
                
                if "error" not in weather_data:
                    location = params.get("location", "the requested location")
                    response_parts.append(self._format_weather_response(weather_data))
                
                if "error" not in news_data:
                    response_parts.append("\n\nHere are some recent headlines:")
                    response_parts.append(self._format_news_response(news_data, brief=True))
            
            return "\n".join(response_parts)
        
        return "I couldn't process your request properly. Please try a different question."
    
    def _get_weather_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch weather data from OpenWeatherMap API or cache"""
        location = params.get("location")
        if not location:
            return {"error": "No location provided"}
        
        cache_key = f"weather_{location}"
        
        # Check cache first
        if cache_key in self.cache and datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
            return self.cache[cache_key]
        
        # In a real implementation, you would use an actual API key and request
        # This is a simulated implementation
        api_key = self.api_keys.get("openweathermap")
        if not api_key:
            # Simulate weather data for demonstration
            weather_conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy", "snowy", "windy", "foggy"]
            temperature = round(random.uniform(0, 35), 1)  # Random temperature between 0 and 35°C
            humidity = random.randint(30, 95)
            wind_speed = round(random.uniform(0, 30), 1)
            
            result = {
                "location": location,
                "country": "Simulated Country",
                "temperature": temperature,
                "feels_like": temperature + random.uniform(-3, 3),
                "conditions": random.choice(weather_conditions),
                "humidity": humidity,
                "wind_speed": wind_speed,
                "timestamp": datetime.now().timestamp(),
                "simulated": True
            }
            
            # Cache the result
            self.cache[cache_key] = result
            self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
            
            return result
        
        # With a real API key, you would make an actual API request
        # For example:
        """
        try:
            base_url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": api_key,
                "units": "metric"
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            result = {
                "location": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "conditions": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "timestamp": data["dt"]
            }
            
            # Cache the result
            self.cache[cache_key] = result
            self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
            
            return result
        except Exception as e:
            return {"error": str(e)}
        """
        
        return {"error": "API key required for actual weather data"}
    
    def _get_news_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch news data from News API or simulate it"""
        topic = params.get("topic")
        cache_key = f"news_{topic}" if topic else "news_general"
        
        # Check cache first
        if cache_key in self.cache and datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
            return self.cache[cache_key]
        
        # Simulate news data for demonstration
        general_headlines = [
            "Global Leaders Meet to Discuss Climate Change Solutions",
            "New Technology Breakthrough Could Revolutionize Renewable Energy",
            "Stock Markets Reach Record Highs Amid Economic Recovery",
            "Scientists Discover Potential New Treatment for Common Disease",
            "Major Sports Championship Results in Unexpected Upset",
            "Tech Company Announces Revolutionary New Product Line",
            "Study Shows Significant Changes in Consumer Behavior Post-Pandemic",
            "International Space Mission Makes Historic Discovery"
        ]
        
        topic_headlines = {
            "technology": [
                "New Quantum Computing Breakthrough Could Transform Data Processing",
                "Tech Giant Unveils Next-Generation Smartphone with Revolutionary Features",
                "Artificial Intelligence System Achieves Human-Level Performance in Complex Task",
                "Major Cybersecurity Vulnerability Discovered in Popular Software",
                "Virtual Reality Technology Shows Promise in Educational Applications"
            ],
            "business": [
                "Global Markets Respond to Changes in Interest Rates",
                "Major Merger Creates New Industry Leader in Financial Services",
                "Startup Secures Record Funding Round for Innovative Business Model",
                "Changes in Consumer Spending Patterns Impact Retail Industry",
                "New Economic Policies Announced to Stimulate Growth"
            ],
            "health": [
                "New Study Reveals Benefits of Mediterranean Diet for Heart Health",
                "Breakthrough in Medical Research Could Lead to Treatment for Rare Disease",
                "Health Authorities Update Guidelines for Preventive Care",
                "Mental Health Awareness Campaign Launches Nationwide",
                "New Fitness Trend Gains Popularity Among Health Enthusiasts"
            ],
            "science": [
                "Astronomers Discover New Exoplanet with Potential for Habitability",
                "Breakthrough in Particle Physics Challenges Existing Theories",
                "Research Team Develops New Method for Carbon Capture",
                "Fossil Discovery Provides Insight into Ancient Ecosystem",
                "New Mathematical Model Helps Predict Complex Natural Phenomena"
            ]
        }
        
        if topic and topic.lower() in topic_headlines:
            headlines = random.sample(topic_headlines[topic.lower()], min(3, len(topic_headlines[topic.lower()])))
        else:
            headlines = random.sample(general_headlines, min(3, len(general_headlines)))
        
        result = {
            "headlines": headlines,
            "topic": topic if topic else "general",
            "timestamp": datetime.now().timestamp(),
            "simulated": True
        }
        
        # Cache the result
        self.cache[cache_key] = result
        self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
        
        return result
    
    def _get_stock_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch stock market data or simulate it"""
        symbol = params.get("symbol")
        if not symbol:
            return {"error": "No stock symbol provided"}
        
        cache_key = f"stock_{symbol}"
        
        # Check cache first
        if cache_key in self.cache and datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
            return self.cache[cache_key]
        
        # Simulate stock data for demonstration
        base_price = random.uniform(50, 500)
        change_percentage = random.uniform(-5, 5)
        
        result = {
            "symbol": symbol,
            "company_name": f"{symbol} Corporation",
            "price": round(base_price, 2),
            "change": round(base_price * change_percentage / 100, 2),
            "change_percent": round(change_percentage, 2),
            "volume": random.randint(100000, 10000000),
            "market_cap": round(base_price * random.randint(1000000, 1000000000), 2),
            "timestamp": datetime.now().timestamp(),
            "simulated": True
        }
        
        # Cache the result
        self.cache[cache_key] = result
        self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
        
        return result
    
    def _get_crypto_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch cryptocurrency data or simulate it"""
        coin = params.get("coin")
        if not coin:
            return {"error": "No cryptocurrency specified"}
        
        cache_key = f"crypto_{coin}"
        
        # Check cache first
        if cache_key in self.cache and datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
            return self.cache[cache_key]
        
        # Base prices for simulation
        base_prices = {
            "btc": 30000,
            "eth": 2000,
            "doge": 0.1,
            "ltc": 100,
            "ada": 0.5,
            "xrp": 0.5
        }
        
        base_price = base_prices.get(coin.lower(), random.uniform(0.1, 100))
        change_percentage = random.uniform(-10, 10)
        
        # Simulate crypto data
        coin_names = {
            "btc": "Bitcoin",
            "eth": "Ethereum",
            "doge": "Dogecoin",
            "ltc": "Litecoin",
            "ada": "Cardano",
            "xrp": "Ripple"
        }
        
        result = {
            "symbol": coin.upper(),
            "name": coin_names.get(coin.lower(), f"{coin.upper()} Coin"),
            "price_usd": round(base_price, 2),
            "change_24h": round(change_percentage, 2),
            "market_cap": round(base_price * random.randint(1000000, 100000000), 2),
            "volume_24h": round(base_price * random.randint(100000, 10000000), 2),
            "timestamp": datetime.now().timestamp(),
            "simulated": True
        }
        
        # Cache the result
        self.cache[cache_key] = result
        self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
        
        return result
    
    def _get_wikipedia_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch data from Wikipedia API or simulate it"""
        topic = params.get("topic")
        if not topic:
            return {"error": "No topic provided"}
        
        cache_key = f"wiki_{topic}"
        
        # Check cache first
        if cache_key in self.cache and datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
            return self.cache[cache_key]
        
        # Simulate Wikipedia data
        simulated_summaries = {
            "python programming": "Python is a high-level, interpreted programming language known for its readability and simplicity. Created by Guido van Rossum and first released in 1991, Python emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented, and functional programming.",
            "artificial intelligence": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving. The ideal characteristic of artificial intelligence is its ability to rationalize and take actions that have the best chance of achieving a specific goal. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.",
            "quantum computing": "Quantum computing is a type of computation that harnesses the collective properties of quantum states, such as superposition, interference, and entanglement, to perform calculations. The devices that perform quantum computations are known as quantum computers. Though current quantum computers are too small to outperform usual (classical) computers for practical applications, they are believed to be capable of solving certain computational problems, such as integer factorization, substantially faster than classical computers.",
            "climate change": "Climate change refers to significant, long-term changes in the global climate. The global climate is the connected system of sun, earth and oceans, wind, rain and snow, forests, deserts and savannas, and everything people do. The climate of a place, say New York, can be described as its rainfall, changing temperatures during the year and so on. But the global climate is more than the climate in one location. Global warming is often used interchangeably with the term climate change, though the latter refers to both human- and naturally-produced warming and the effects it has on our planet."
        }
        
        # Generate a simulated response based on the topic or a generic one
        if topic.lower() in simulated_summaries:
            summary = simulated_summaries[topic.lower()]
        else:
            summary = f"{topic} is a topic of significance in its field. While detailed information would typically be available from Wikipedia, this is a simulated response providing general information about the concept. In a complete implementation, this would include a comprehensive summary from a knowledge source like Wikipedia."
        
        result = {
            "topic": topic,
            "summary": summary,
            "url": f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}",
            "timestamp": datetime.now().timestamp(),
            "simulated": True
        }
        
        # Cache the result
        self.cache[cache_key] = result
        self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
        
        return result
    
    def _translate_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Translate text between languages or simulate translation"""
        text = params.get("text")
        source_lang = params.get("source_lang", "auto")
        target_lang = params.get("target_lang")
        
        if not text:
            return {"error": "No text provided for translation"}
        
        if not target_lang:
            return {"error": "No target language specified"}
        
        cache_key = f"translate_{source_lang}_{target_lang}_{text}"
        
        # Check cache first
        if cache_key in self.cache and datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
            return self.cache[cache_key]
        
        # Simulate translations
        simulated_translations = {
            "hello": {
                "spanish": "Hola",
                "french": "Bonjour",
                "german": "Hallo",
                "italian": "Ciao",
                "portuguese": "Olá",
                "japanese": "こんにちは",
                "chinese": "你好",
                "russian": "Привет"
            },
            "goodbye": {
                "spanish": "Adiós",
                "french": "Au revoir",
                "german": "Auf Wiedersehen",
                "italian": "Arrivederci",
                "portuguese": "Adeus",
                "japanese": "さようなら",
                "chinese": "再见",
                "russian": "До свидания"
            },
            "thank you": {
                "spanish": "Gracias",
                "french": "Merci",
                "german": "Danke",
                "italian": "Grazie",
                "portuguese": "Obrigado",
                "japanese": "ありがとう",
                "chinese": "谢谢",
                "russian": "Спасибо"
            }
        }
        
        # Try to find a simulated translation
        text_lower = text.lower()
        if text_lower in simulated_translations and target_lang.lower() in simulated_translations[text_lower]:
            translated_text = simulated_translations[text_lower][target_lang.lower()]
        else:
            # For other text, just append the target language to simulate translation
            translated_text = f"{text} [{target_lang} translation]"
        
        result = {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "timestamp": datetime.now().timestamp(),
            "simulated": True
        }
        
        # Cache the result
        self.cache[cache_key] = result
        self.cache_expiry[cache_key] = datetime.now() + timedelta(seconds=self.cache_duration)
        
        return result
    
    def _format_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a readable response"""
        if "error" in weather_data:
            return f"Sorry, I couldn't retrieve weather information: {weather_data['error']}"
        
        location = weather_data["location"]
        temperature = weather_data["temperature"]
        conditions = weather_data["conditions"]
        humidity = weather_data["humidity"]
        wind_speed = weather_data["wind_speed"]
        
        return (
            f"Weather in {location}:\n"
            f"🌡️ Temperature: {temperature}°C\n"
            f"🌤️ Conditions: {conditions.capitalize()}\n"
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind Speed: {wind_speed} m/s"
        )
    
    def _format_news_response(self, news_data: Dict[str, Any], brief: bool = False) -> str:
        """Format news data into a readable response"""
        if "error" in news_data:
            return f"Sorry, I couldn't retrieve news information: {news_data['error']}"
        
        headlines = news_data["headlines"]
        topic = news_data["topic"]
        
        if brief:
            headline_text = "\n".join([f"• {headline}" for headline in headlines[:2]])
            return f"{headline_text}"
        else:
            headline_text = "\n".join([f"• {headline}" for headline in headlines])
            return f"Here are the latest {topic} headlines:\n\n{headline_text}"
    
    def _format_stock_response(self, stock_data: Dict[str, Any]) -> str:
        """Format stock data into a readable response"""
        if "error" in stock_data:
            return f"Sorry, I couldn't retrieve stock information: {stock_data['error']}"
        
        symbol = stock_data["symbol"]
        company = stock_data["company_name"]
        price = stock_data["price"]
        change = stock_data["change"]
        change_percent = stock_data["change_percent"]
        
        # Determine emoji based on stock performance
        emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
        change_sign = "+" if change > 0 else ""
        
        return (
            f"Stock information for {company} ({symbol}):\n"
            f"💰 Current Price: ${price}\n"
            f"{emoji} Change: {change_sign}{change} ({change_sign}{change_percent}%)"
        )
    
    def _format_crypto_response(self, crypto_data: Dict[str, Any]) -> str:
        """Format cryptocurrency data into a readable response"""
        if "error" in crypto_data:
            return f"Sorry, I couldn't retrieve cryptocurrency information: {crypto_data['error']}"
        
        symbol = crypto_data["symbol"]
        name = crypto_data["name"]
        price = crypto_data["price_usd"]
        change = crypto_data["change_24h"]
        
        # Determine emoji based on performance
        emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
        change_sign = "+" if change > 0 else ""
        
        return (
            f"Cryptocurrency information for {name} ({symbol}):\n"
            f"💰 Current Price: ${price}\n"
            f"{emoji} 24h Change: {change_sign}{change}%"
        )
    
    def _format_wikipedia_response(self, wiki_data: Dict[str, Any]) -> str:
        """Format Wikipedia data into a readable response"""
        if "error" in wiki_data:
            return f"Sorry, I couldn't retrieve information: {wiki_data['error']}"
        
        topic = wiki_data["topic"]
        summary = wiki_data["summary"]
        url = wiki_data["url"]
        
        return (
            f"Here's information about {topic}:\n\n"
            f"{summary}\n\n"
            f"Learn more: {url}"
        )
    
    def _format_translation_response(self, translation_data: Dict[str, Any]) -> str:
        """Format translation data into a readable response"""
        if "error" in translation_data:
            return f"Sorry, I couldn't translate the text: {translation_data['error']}"
        
        original = translation_data["original_text"]
        translated = translation_data["translated_text"]
        source_lang = translation_data["source_language"]
        target_lang = translation_data["target_language"]
        
        return (
            f"Translation:\n"
            f"📝 Original ({source_lang}): {original}\n"
            f"🔄 Translated ({target_lang}): {translated}"
        )


# Demo function to test the agent
def demo_multi_source_agent():
    """Run a demonstration of the MultiSourceAgent with sample queries"""
    agent = MultiSourceAgent(name="DataAgent")
    
    print("=" * 60)
    print("Multi-Source AI Agent Demo")
    print("=" * 60)
    print("This agent can handle complex queries across multiple data sources")
    print("Note: All responses are simulated for demonstration purposes")
    print("=" * 60)
    
    # Sample queries to demonstrate capabilities
    sample_queries = [
        "What's the weather in London?",
        "Tell me the latest technology news",
        "What's the current price of Bitcoin?",
        "What is artificial intelligence?",
        "Translate 'hello' to Spanish",
        "What's the weather in Tokyo and give me the latest news",
        "Help me understand what you can do"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 50)
        response = agent.respond(query)
        print(f"Response:\n{response}")
        print("=" * 60)
        time.sleep(1)  # Pause between queries for readability
    
    print("\nDemo completed!")


if __name__ == "__main__":
    demo_multi_source_agent()