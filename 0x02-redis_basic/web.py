import requests
import redis
import time
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(expiration: int = 10):
    '''
    Decorator to cache the result of a page request with an expiration time.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            # Check if the result is already cached
            cached_page = redis_client.get(f"cache:{url}")
            if cached_page:
                return cached_page.decode('utf-8')

            # If not cached, fetch the page
            page_content = func(url)

            # Cache the result with an expiration time
            redis_client.setex(f"cache:{url}", expiration, page_content)

            return page_content
        return wrapper
    return decorator


def count_requests(func):
    '''
    Decorator to count the number of requests made to a particular URL.
    '''
    @wraps(func)
    def wrapper(url: str):
        # Increment the access count for this URL
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper


@count_requests
@cache_page(expiration=10)
def get_page(url: str) -> str:
    '''
    Fetches the content of a URL and returns it as a string.
    The content is cached for 10 seconds,
    and the number of accesses is tracked.
    '''
    response = requests.get(url)
    return response.text
