"""
Hack script to call the API 10,000 times to demonstrate rate limiting.
This helps visualize how rate limiting works and its impact on request handling.
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000/test"
TOTAL_REQUESTS = 10000
MAX_WORKERS = 50  # Concurrent requests


def make_request(request_num):
    """Make a single API request and return result"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return {
            "request_num": request_num,
            "status_code": response.status_code,
            "data": response.json(),
            "success": True,
        }
    except Exception as e:
        return {
            "request_num": request_num,
            "status_code": None,
            "error": str(e),
            "success": False,
        }


def main():
    print(f"Starting {TOTAL_REQUESTS:,} API calls to {BASE_URL}")
    print(f"Using {MAX_WORKERS} concurrent workers\n")

    start_time = time.time()
    successful = 0
    failed = 0
    errors = {}

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(make_request, i) for i in range(TOTAL_REQUESTS)]

            for idx, future in enumerate(as_completed(futures)):
                result = future.result()

                if result["success"]:
                    successful += 1
                else:
                    failed += 1
                    error = result["error"]
                    errors[error] = errors.get(error, 0) + 1

                # Progress update every 1000 requests
                if (idx + 1) % 1000 == 0:
                    elapsed = time.time() - start_time
                    rate = (idx + 1) / elapsed
                    print(
                        f"Progress: {idx + 1:,}/{TOTAL_REQUESTS:,} | "
                        f"Success: {successful:,} | Failed: {failed:,} | "
                        f"Rate: {rate:.0f} req/s"
                    )

    except KeyboardInterrupt:
        print("\n Interrupted by user")

    # Final results
    elapsed_time = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"RESULTS")
    print(f"{'='*70}")
    print(f"Total Time: {elapsed_time:.2f}s")
    print(f"Successful Requests: {successful:,}")
    print(f"Failed Requests: {failed:,}")
    print(f"Success Rate: {(successful/TOTAL_REQUESTS)*100:.1f}%")
    print(f"Average Rate: {TOTAL_REQUESTS/elapsed_time:.0f} req/s")

    if errors:
        print(f"\nErrors encountered:")
        for error, count in sorted(errors.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {error}: {count}")


if __name__ == "__main__":
    main()
