# Backend II
## Session 1: Fundamentals of Big O Notation in Python Performance

**Goal:**
Understand how algorithm complexity is measured with Big O notation and why it matters for performance in Python.

**Definition:**
Big O notation expresses the upper bound of an algorithm’s runtime relative to its input size. It helps you compare algorithms and identify potential bottlenecks. Use cases include analysing search, sort, or any iterative processes. In Python, knowing Big O is essential for writing efficient code when dealing with large datasets.

**Documentation Reference:**
- https://docs.python.org/3/tutorial/datastructures.html
- https://en.wikipedia.org/wiki/Big_O_notation
- https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/
- https://www.bigocheatsheet.com/

### Tutorial:

- Write a simple linear search function:
```py
def linear_search(lst, target):
    for item in lst:
        if item == target:
            return True
    return False
```

- Explanation: This function’s runtime grows linearly with the size of the list, hence O(n).

- Comparison: Briefly discuss how a binary search (O(log n)) differs in performance.

### Exercise:

- Problem: Write a recursive function to calculate factorial and determine its time complexity.
- Steps to Solve:
    - Define the recursive factorial function.
    - Analyse how many times the function is called relative to the input.

### Challenge:

- Problem: Optimise a bubble sort algorithm so that it stops early if the list is already sorted.
> Hint: Use a flag to detect whether a swap occurred.

## Session 2: Implementing Design Patterns in Python for Robust Architecture

**Goal:**
Learn key design patterns and how to implement them in Python to build maintainable and robust applications.

**Definition:**
Design patterns are standard solutions to common software design problems. They promote reusability and cleaner code structure. Use cases include managing shared resources (Singleton), abstracting object creation (Factory), and handling events (Observer). Mastery of these patterns leads to clearer communication among developers and more scalable applications.

**Documentation Reference:**
- https://refactoring.guru/design-patterns/python
- https://www.tutorialspoint.com/python_design_patterns/index.htm

### Tutorial:
- Introduction to Singleton: Explain why you might need only one instance of a class.
```py
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)
```
- Explanation: Both instances refer to the same object.
- Discussion: Briefly mention other patterns (Factory, Observer) for context.

### Exercise:

- Problem: Implement the Factory pattern to create shape objects (e.g., Circle and Square).

- Steps to Solve:
    - Define an abstract Shape class.
    - Create concrete classes for Circle and Square.
    - Write a factory function to return the correct object.

### Challenge:

- Problem: Implement the Observer pattern to notify multiple observers when a subject’s state changes.
- Hint: Create a Subject class that maintains a list of observers.

## Session 3: Mastering Multi-threading in Python

**Goal:**
Learn how to run code concurrently using threads to improve performance for I/O-bound tasks.

**Definition:**
Multi-threading splits a program into multiple threads running in parallel. In Python, this is ideal for I/O-bound operations because threads share the same memory space. Use cases include network operations, file I/O, and handling multiple user requests. Despite the Global Interpreter Lock (GIL), multi-threading remains effective for many practical scenarios.

**Documentation Reference:**
- https://docs.python.org/3/library/threading.html
- https://realpython.com/intro-to-python-threading/
- https://www.tutorialspoint.com/python/python_multithreading.htm

### Tutorial:

- Introduction: Explain the threading module.

```py
import threading
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(1)

thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()
```
- Explanation: This runs the print_numbers function in a separate thread.
- Discussion: Mention when to use threads (e.g., I/O-bound tasks).

### Exercise:

- Problem: Create two threads that print letters and numbers concurrently.
- Steps to Solve:
    - Define two functions—one for letters and one for numbers.
    - Create and start a thread for each function.

### Challenge:

- Problem: Create a multi-threaded program that downloads multiple files concurrently from given URLs.
- Hint: Use the threading module along with urllib.request.urlretrieve.


## Session 4: Multi-processing in Python for Scalability
**Goal:**
Understand how to run tasks concurrently in separate processes to boost performance in CPU-bound tasks.

**Definition:**
Multi-processing uses separate processes with their own memory space, bypassing the Global Interpreter Lock (GIL). This technique is ideal for CPU-intensive tasks such as heavy computations or large data processing, where parallel execution on multiple cores can lead to significant speed improvements. It is commonly used in scenarios that require isolated execution environments.

**Documentation Reference:**

- https://docs.python.org/3/library/multiprocessing.html
- https://realpython.com/python-multiprocessing/
- https://www.geeksforgeeks.org/multiprocessing-python-set-1/

**Tutorial:**
- Introduction: Explain the difference between threading and multi-processing.
- Step-by-Step Example:
    - Import the multiprocessing module.
    -  Define a simple function (e.g., compute a square).
    - Create and start multiple processes.
```py
import multiprocessing
import time

def compute_square(n):
    time.sleep(1)  # Simulate a heavy computation
    print(f"Square of {n} is {n*n}")

if __name__ == "__main__":
    numbers = [2, 3, 4, 5]
    processes = []
    for number in numbers:
        p = multiprocessing.Process(target=compute_square, args=(number,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

```
- Explanation: Each process runs independently, and joining ensures all complete before the script ends.

### Exercise:

- Problem: Create a program that concurrently computes the factorial of several numbers using multi-processing.
- Steps to Solve:
    - Define a recursive factorial function.
    - Spawn a process for each number in a list.

### Challenge:

- Problem: Create a multi-process program that divides a large list of numbers into sublists and computes the sum of squares for each sublist concurrently.
- Hint:
  Use the Pool class from the multiprocessing module.

## Session 5: Asynchronous Programming in Python with asyncio and FastAPI

**Goal:**
Learn to write non-blocking code using asyncio and integrate it into a FastAPI endpoint.

**Definition:**
Asynchronous programming allows concurrent execution of tasks without waiting for each to complete sequentially. In Python, the asyncio library provides tools to write such code, which is especially useful for I/O-bound operations like web requests or database calls. This enables scalable web services by handling multiple requests simultaneously.

**Documentation Reference:**

- https://docs.python.org/3/library/asyncio.html
- https://fastapi.tiangolo.com/async/
- https://realpython.com/async-io-python/

**Tutorial:**
- Setup FastAPI:
```bash
poetry add fastapi uvicorn
```
- Step-by-Step Example:

    - Create an asynchronous function using async def and await.
    - Define a FastAPI endpoint that calls this async function.
```py
    from fastapi import FastAPI
    import asyncio

    app = FastAPI()

    async def simulated_io_task():
        await asyncio.sleep(1)
        return "Data fetched!"

    @app.get("/async-data")
    async def get_data():
        result = await simulated_io_task()
        return {"message": result}

    # Run using: uvicorn filename:app --reload
```
- Explanation: The endpoint /async-data executes the async task without blocking other requests.

### Exercise:

- Problem: Create a FastAPI endpoint that concurrently fetches data from two simulated sources using asyncio.gather.

    - Steps to Solve:
        - Define two async functions that simulate data fetching.
        - Use asyncio.gather to run them concurrently.


### Challenge:

- Problem:Develop an asynchronous web scraper that fetches HTML content from multiple URLs concurrently using aiohttp.
    - Hint: Use the aiohttp library with asyncio.gather.

## Session 6: Advanced Async Patterns and Concurrency Techniques

**Goal:**
Explore advanced asynchronous programming concepts to manage tasks, handle timeouts, and coordinate concurrent operations efficiently.

**Definition:**
Beyond basic async functions, advanced patterns include task scheduling, handling cancellations, and synchronising shared resources with locks or semaphores. These techniques help in building high-load systems and real-time data processing pipelines. They are crucial when developing scalable web applications and services that demand robust concurrency management.

**Documentation Reference:**

- https://docs.python.org/3/library/asyncio-task.html
- https://realpython.com/python-async-features/
- https://medium.com/@kennethreitz/async-await-in-python-3-5-7b580ca64b73

**Tutorial:**
- Creating Tasks:
    - Use asyncio.create_task to run coroutines concurrently.
```py
import asyncio

async def task_function(name, delay):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def main():
    task1 = asyncio.create_task(task_function("Task 1", 1))
    task2 = asyncio.create_task(task_function("Task 2", 2))
    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())
```

- Handling Timeouts:
    - Use asyncio.wait_for to set timeouts.
```py
    async def timeout_task():
        await asyncio.sleep(2)
        return "Completed"

    async def main_timeout():
        try:
            result = await asyncio.wait_for(timeout_task(), timeout=1)
        except asyncio.TimeoutError:
            result = "Task timed out"
        print(result)

    asyncio.run(main_timeout())
```
- Explanation: This demonstrates cancelling a task if it exceeds the allotted time.

### Exercise:

- Problem: Write an async function that launches several tasks with a timeout and handles cancellations gracefully.
    -Steps to Solve:
        - Create multiple tasks using create_task.
        - Wrap them with asyncio.wait_for and handle possible timeouts.

### Challenge:

- Problem: Implement an asynchronous rate limiter that allows only a fixed number of tasks per second.
    - Hint: Use an asyncio semaphore to control the concurrency.

## Session 7: Implementing Logging Best Practices in Python

**Goal:**
Learn to integrate and configure logging in Python applications for effective debugging and monitoring.

**Definition:**
Logging captures runtime events, errors, and general application flow. Python’s built-in logging module, along with third-party libraries like loguru, provides flexibility and ease of use. It is essential for debugging, performance monitoring, and security auditing in production systems.

**Documentation Reference:**

- https://docs.python.org/3/library/logging.html
- https://loguru.readthedocs.io/en/stable/
- https://realpython.com/python-logging/

**Tutorial:**
- Basic Logging Setup:
    - Configure the built-in logging module.
```py
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log')
logging.info("This is an info message")
logging.error("This is an error message")
```
- Using loguru:
    - Install and use loguru for a simpler logging experience.
```py
    from loguru import logger

    logger.add("file.log", rotation="1 MB")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.error("Error message")
```
    Explanation: The examples show both native and third-party logging configurations.

### Exercise:

- Problem: Create a Python script that logs messages at DEBUG, INFO, WARNING, and ERROR levels.
    - Steps to Solve:
        - Configure logging using the built-in module.
        - Log messages at different severity levels.

### Challenge:

- Problem: Enhance the logging setup to rotate log files daily and include detailed timestamps.
    - Hint: Use TimedRotatingFileHandler from the logging.handlers module.

## Session 8: Introduction to Testing in Python with pytest

**Goal:**
Learn the basics of writing and running tests using pytest to improve code reliability.

**Definition:**
Testing ensures that code behaves as expected. pytest is a powerful testing framework that simplifies writing tests and offers rich features like fixtures and parametrization. It is used for unit testing, integration tests, and continuous integration pipelines to catch errors early in development.

**Documentation Reference:**

- https://docs.pytest.org/en/stable/getting-started.html
- https://realpython.com/pytest-python-testing/
- https://docs.python.org/3/library/unittest.html

**Tutorial:**

- Create a simple function (e.g., addition).
```py
# app.py
def add(a, b):
    return a + b
```
- Write a test for the function.
```py
# test_app.py
from app import add

def test_add():
    assert add(2, 3) == 5
```

- Run tests using:
```bash
    pytest
```

### Exercise:

- Problem: Write a Python function that multiplies two numbers and create a corresponding pytest test.

### Challenge:

- Problem: Write tests for a recursive factorial function using pytest parametrization.
    - Hint: Use the @pytest.mark.parametrize decorator.

## Session 9: Advanced Testing Strategies in Django using pytest

**Goal:**
Explore comprehensive testing techniques in Django projects using pytest to ensure robust web application functionality.

**Definition:**
Advanced testing in Django involves creating tests for models, views, and API endpoints using pytest-django. This approach leverages fixtures, parametrization, and a dedicated test database. It is essential for verifying that all components of a Django application work together as expected, from data models to user interfaces.

**Documentation Reference:**

- https://pytest-django.readthedocs.io/en/latest/
- https://docs.djangoproject.com/en/3.2/topics/testing/overview/
- https://realpython.com/django-testing-guide/

**Tutorial:**
- Setup:
    - Install pytest-django:
```bash
    pip install pytest-django
```
- Step-by-Step Example:
    - Create a simple Django model.
```py
# models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
```
- Write a test to check model creation.
```py
    # test_models.py
    import pytest
    from myapp.models import Item

    @pytest.mark.django_db
    def test_item_creation():
        item = Item.objects.create(name="Test", value=10)
        assert item.name == "Test"
        assert item.value == 10
```
- Explanation: The test uses the Django test database to create and verify an Item instance.

### Exercise:

- Problem: Create a Django model for a BlogPost and write pytest tests to verify its methods.
    - Steps to Solve:
        - Define the BlogPost model with title, content, and published date.
        - Write tests for creating and retrieving BlogPosts.

### Challenge:

- Problem: Develop a full test suite for a Django REST API endpoint (e.g., listing BlogPosts) using pytest fixtures and parametrization.
    - Hint: Create fixtures for BlogPost objects and test the API response structure.


## Session 10: Enhancing Security in Python Applications

**Goal:**
Learn techniques to secure Python web applications against common vulnerabilities.

**Definition:**
Security in Python involves applying best practices to prevent attacks such as SQL injection, XSS, CSRF, and more. It includes validating user input, using secure authentication methods, and implementing proper error handling. These measures are critical in protecting sensitive data and maintaining user trust in web applications.

**Documentation Reference:**

- https://owasp.org/www-project-top-ten/
- https://docs.djangoproject.com/en/3.2/topics/security/
- https://fastapi.tiangolo.com/advanced/security/

**Tutorial:**

- Step-by-Step Example:

    - Discuss common vulnerabilities and secure coding practices.
    - Implement a FastAPI endpoint that uses JWT for authentication.
```py
    from fastapi import FastAPI, Depends, HTTPException
    from fastapi.security import OAuth2PasswordBearer
    from jose import JWTError, jwt

    app = FastAPI()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    SECRET_KEY = "your-secret-key"

    def verify_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @app.get("/secure-data")
    async def secure_data(user=Depends(verify_token)):
        return {"data": "Secure Information"}
```
- Explanation: This endpoint only returns data when a valid JWT token is provided.

### Exercise:

- Problem: Create a FastAPI endpoint that accepts user input, sanitises it, and returns a safe response.
    - Steps to Solve:
        - Define an endpoint that accepts query parameters.
        - Apply input validation and sanitisation.

### Challenge:

- Problem: Secure a Django application by implementing comprehensive security measures: CSRF protection, secure session management, and input validation.
    - Hint: Use Django’s built-in security middleware and forms.

## Session 11: Building GraphQL APIs with Python

**Goal:**
Learn to design and implement a GraphQL API in Python for flexible client data queries.

**Definition:**
GraphQL is a query language that allows clients to request exactly the data they need. In Python, libraries like Strawberry and Graphene simplify building GraphQL APIs. Use cases include mobile and web applications that require efficient and customisable data fetching.

**Documentation Reference:

- https://graphql.org/learn/
- https://graphene-python.org/
- https://strawberry.rocks/docs/

**Tutorial:**
- Step-by-Step Example:

        Install Strawberry:
```bash
pip install strawberry-graphql
```
- Define types and resolvers.

```py
    import strawberry
    from fastapi import FastAPI
    from strawberry.asgi import GraphQL

    @strawberry.type
    class User:
        id: int
        name: str

    @strawberry.type
    class Query:
        @strawberry.field
        def user(self, id: int) -> User:
            return User(id=id, name="John Doe")

    schema = strawberry.Schema(query=Query)
    graphql_app = GraphQL(schema)

    app = FastAPI()
    app.add_route("/graphql", graphql_app)
```
- Explanation: This creates a GraphQL endpoint at /graphql where clients can query for user data.

### Exercise:

Problem: Create a simple GraphQL API that allows querying and updating a user’s name.

- Steps to Solve: Extend the schema to include a mutation for updating the user’s name.

### Challenge:

Problem: Implement a GraphQL API that supports nested queries and authenticated mutations.
    - Hint: Integrate an authentication check in the resolver.

## Session 12: Developing gRPC Services in Python

**Goal:**
Learn to build and consume gRPC services for efficient inter-service communication.

**Definition:**
gRPC is a high-performance RPC framework that uses Protocol Buffers for data serialization. It facilitates fast communication between microservices. Use cases include real-time data streaming, cross-language services, and distributed systems.

**Documentation Reference:**

- https://grpc.io/docs/languages/python/quickstart/
- https://docs.python.org/3/library/concurrent.futures.html
- https://realpython.com/python-grpc/

**Tutorial:**
- Step-by-Step Example:
    - Define a simple .proto file.
    ```proto
    syntax = "proto3";
    package service;

    service Greeter {
        rpc SayHello (HelloRequest) returns (HelloReply) {}
    }
    message HelloRequest {
        string name = 1;
    }
    message HelloReply {
        string message = 1;
    }
    ```
    - Generate Python code using grpcio-tools.
    ```bash
    pip install grpcio-tools
    ```
    ```bash
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
    ```
    - Implement a server and client.
    ```bash
    pip install grpcio
    ```
    ```py
    from concurrent import futures
    import grpc
    import service_pb2
    import service_pb2_grpc

    class Greeter(service_pb2_grpc.GreeterServicer):
        def SayHello(self, request, context):
            return service_pb2.HelloReply(message=f"Hello, {request.name}!")

    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

    if __name__ == "__main__":
        serve()
    ``` 
### Exercise:

- Problem: Build a basic gRPC service that returns the cube of a number.
    - Steps to Solve:
        -  Define the .proto file, generate code, and implement the server and client.

## Challenge:

- Problem:
    - Create a gRPC service that supports server-side streaming to send multiple messages for a single request.
        - Hint: Modify the .proto definition to use a stream for the response.

## Session 13: Python Web Development Best Practices with Django and FastAPI

**Goal:**
Learn how to structure and optimise web applications using Django and FastAPI effectively.

**Definition:**
Web development best practices include clear code organisation, proper error handling, security measures, and performance optimisation. By following framework-specific guidelines and industry standards, you ensure scalable and maintainable code. This session compares Django’s monolithic approach with FastAPI’s asynchronous design, highlighting key strategies for each.

**Documentation Reference:**

- https://docs.djangoproject.com/en/3.2/
- https://fastapi.tiangolo.com/
- https://realpython.com/django-best-practices/

**Tutorial:**

- Step-by-Step Example:
    - Create a simple Django project and a FastAPI app.
    - Highlight differences in project structure, middleware usage, and error handling.

```py
# Django: views.py example
from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Hello from Django"})

    # FastAPI: main.py example
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def index():
        return {"message": "Hello from FastAPI"}
```

### Exercise:

- Problem: Create a minimal Django project and a FastAPI application that serve a simple "Hello World" endpoint following best practices.
    - Steps to Solve:
        - Set up both projects with proper directory structure.
        - Implement and test the endpoints.

### Challenge:

- Problem: Refactor an existing web application to improve error handling, logging, and performance optimisation.
    - Hint: Consider integrating middleware and asynchronous processing where possible.

## Session 14: Introduction to AI Agents in Python with CrewAI

**Goal:**
Learn the basics of building AI agents using the CrewAI framework to automate tasks and respond intelligently.

**Definition:**
AI agents are autonomous software components that perform tasks based on user input or environmental data. CrewAI simplifies the creation of such agents by providing pre-built modules for conversation, decision-making, and integration with external services. Use cases include chatbots, automated customer support, and data analysis assistants.

**Documentation Reference:**

- https://crew.ai/docs
- https://github.com/crew-ai/crewai-python
- https://en.wikipedia.org/wiki/Intelligent_agent

**Tutorial:**
- Step-by-Step Example:
    - Install CrewAI (follow the documentation).
    - Create a simple AI agent that responds to a fixed query.
```py
    # Example pseudocode using CrewAI
    from crewai import Agent

    agent = Agent(name="SimpleAgent")
    response = agent.respond("Hello")
    print(response)
```
- Explanation: This example demonstrates initializing an agent and obtaining a response.

### Exercise:

- Problem: Build a simple AI agent that returns a predefined message when given a specific input.
    - Steps to Solve:
        - Initialise the agent.
        - Define a response logic for a specific query.

### Challenge:

- Problem: Enhance the agent to handle multiple queries with different responses based on keywords.
    - Hint: Use conditional statements or a mapping dictionary.

## Session 15: Advanced AI Agent Development with CrewAI

**Goal:**
Deepen your knowledge in AI agent development by integrating state management and external API data into CrewAI agents.

**Definition:**
Advanced AI agents not only respond to queries but also maintain context and learn from interactions. Integrating state management and external API calls allows agents to deliver dynamic, personalised responses. Use cases include chatbots that track user history and recommendation engines that adjust responses based on real-time data.

**Documentation Reference:**

- https://crew.ai/docs/advanced
- https://github.com/crew-ai/crewai-python
- https://en.wikipedia.org/wiki/Artificial_intelligence

**Tutorial:**
- Step-by-Step Example:
    - Extend the basic agent to store conversation history.
    ```py
    from crewai import Agent

    class StatefulAgent(Agent):
        def __init__(self, name):
            super().__init__(name)
            self.history = []

        def respond(self, query):
            self.history.append(query)
            if query.lower() == "history":
                return f"Your queries: {', '.join(self.history)}"
            return f"Echo: {query}"

    agent = StatefulAgent("StatefulAgent")
    print(agent.respond(query="query"))
    ```
- Explanation: This agent keeps track of previous queries and can respond with the history.

### Exercise

- Problem: Create an AI agent that fetches real-time weather data from an external API and responds with the current temperature.
    - Steps to Solve:
        - Integrate an API call within the agent’s response logic.

### Challenge

- Problem: Develop an AI agent that can handle complex queries and respond with relevant information, possibly using external APIs for data enrichment.
    - Hint: Implement a more sophisticated response logic that can parse and respond to structured queries.

## Session 16: Building CI/CD Pipelines for Python Projects with GitHub Actions

**Goal:**
Learn how to automate testing, building, and deploying your Python projects using GitHub Actions.

**Definition:**
CI/CD stands for Continuous Integration and Continuous Deployment. It automates testing and deployment so that every code change is verified and delivered seamlessly. In Python projects, CI/CD pipelines help run tests (using pytest), build the application, and deploy to a target environment without manual intervention. This process reduces errors and accelerates development cycles.

**Documentation Reference:**

- https://docs.github.com/en/actions
- https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions
- https://docs.pytest.org/en/stable/

**Tutorial:**

- Create Workflow Directory: In your repository, create a folder named .github/workflows.
- Create Workflow File: Add a file named ci.yml with the following content:
```yaml
    name: CI Pipeline
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - name: Set up Python
            uses: actions/setup-python@v2
            with:
              python-version: '3.9'
          - name: Install dependencies
            run: |
              pip install pytest
              pip install -r requirements.txt
          - name: Run tests
            run: pytest
```
- Commit and Push: Commit the file and push to GitHub to trigger the workflow. Explanation: This workflow checks out your code, sets up Python, installs dependencies, and runs tests using pytest.

### Exercise:

- Problem: Create a GitHub Actions workflow that tests your project on multiple Python versions.
    - Steps to Solve: Modify the YAML file to include a matrix strategy for Python versions.

### Challenge:

- Problem: Extend the CI/CD pipeline to include a deployment step that runs only when code is pushed to the main branch.
    - Hint: Use conditional steps and job dependencies.
