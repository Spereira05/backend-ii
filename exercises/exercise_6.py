import asyncio
import random

async def task_with_random_delay(task_id):
    """Simulates a task with random execution time."""
    delay = random.uniform(1, 5)
    print(f"Task {task_id} starting, will take {delay:.2f} seconds")
    try:
        await asyncio.sleep(delay)
        print(f"Task {task_id} completed successfully")
        return f"Result from task {task_id}"
    except asyncio.CancelledError:
        print(f"Task {task_id} was cancelled")
        # Clean up resources if needed
        raise  # Re-raise the cancellation to properly propagate it

async def run_with_timeout(coro, timeout):
    """Run a coroutine with a timeout, handling cancellation gracefully."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Operation timed out after {timeout} seconds")
        return None

async def main():
    # Create multiple tasks
    tasks = [
        run_with_timeout(task_with_random_delay(1), 3.0),
        run_with_timeout(task_with_random_delay(2), 3.0),
        run_with_timeout(task_with_random_delay(3), 3.0),
        run_with_timeout(task_with_random_delay(4), 3.0),
        run_with_timeout(task_with_random_delay(5), 3.0)
    ]
    
    # Run all tasks concurrently
    print("Starting all tasks with a 3 second timeout...")
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    print("\nResults:")
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"Task {i} resulted in an exception: {result}")
        elif result is None:
            print(f"Task {i} timed out")
        else:
            print(f"Task {i} succeeded with result: {result}")

if __name__ == "__main__":
    asyncio.run(main())