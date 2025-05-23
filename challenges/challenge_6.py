import asyncio
import time
from datetime import datetime
import random

class AsyncRateLimiter:
    def __init__(self, max_calls, time_period):
        """
        Initialize a rate limiter
        
        :param max_calls: Maximum number of calls allowed in the time period
        :param time_period: Time period in seconds
        """
        self.max_calls = max_calls
        self.time_period = time_period
        self.calls = []
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """
        Acquire permission to proceed. If the rate limit is exceeded,
        this will wait until a slot becomes available.
        """
        async with self._lock:
            now = time.time()
            
            # Remove timestamps that are older than our time period
            self.calls = [timestamp for timestamp in self.calls 
                         if timestamp > now - self.time_period]
            
            # If we're at the limit, wait until the oldest call expires
            if len(self.calls) >= self.max_calls:
                oldest_call = self.calls[0]
                wait_time = oldest_call + self.time_period - now
                if wait_time > 0:
                    print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                    await asyncio.sleep(wait_time)
                    # After waiting, we need to clean up old timestamps again
                    now = time.time()
                    self.calls = [timestamp for timestamp in self.calls 
                                 if timestamp > now - self.time_period]
            
            # Add the current timestamp and allow the call
            self.calls.append(now)

async def perform_task(task_id, rate_limiter):
    """Simulated task that requires rate limiting"""
    await rate_limiter.acquire()
    
    # Now we have permission to proceed
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print(f"[{timestamp}] Executing task {task_id}")
    
    # Simulate work being done
    work_time = random.uniform(0.1, 0.5)
    await asyncio.sleep(work_time)
    
    return f"Task {task_id} completed in {work_time:.2f}s"

async def main():
    # Create a rate limiter that allows 5 tasks per 2 seconds
    rate_limiter = AsyncRateLimiter(max_calls=5, time_period=2)
    
    # Create 20 tasks that will compete for rate-limited resources
    tasks = [perform_task(i, rate_limiter) for i in range(1, 21)]
    
    print("Starting 20 tasks with rate limit of 5 requests per 2 seconds...")
    results = await asyncio.gather(*tasks)
    
    print("\nAll tasks completed!")

if __name__ == "__main__":
    asyncio.run(main())