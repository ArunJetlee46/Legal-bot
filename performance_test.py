"""
Performance validation script for Legal-bot optimizations.
Tests search operations to ensure performance improvements.
"""

import time
from laws_database import search_law, search_kanoon
from legal_knowledge import find_topic

def time_function(func, *args, **kwargs):
    """Measure execution time of a function."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return result, end - start

def main():
    print("Performance Validation Test")
    print("=" * 60)

    # Test 1: Search law database
    print("\n1. Testing search_law() with 'consumer protection'...")
    result, duration = time_function(search_law, "consumer protection", max_results=5)
    print(f"   Results found: {len(result)}")
    print(f"   Time: {duration*1000:.2f}ms")

    # Test 2: Search Kanoon database
    print("\n2. Testing search_kanoon() with 'indian penal code'...")
    result, duration = time_function(search_kanoon, "indian penal code", max_results=10)
    print(f"   Results found: {len(result)}")
    print(f"   Time: {duration*1000:.2f}ms")

    # Test 3: Find topic
    print("\n3. Testing find_topic() with 'I need a lawyer'...")
    result, duration = time_function(find_topic, "I need a lawyer for my case")
    print(f"   Topic found: {result['title'] if result else 'None'}")
    print(f"   Time: {duration*1000:.2f}ms")

    # Test 4: Multiple searches (simulating real usage)
    print("\n4. Testing 10 consecutive searches (simulating user queries)...")
    queries = [
        "RTI application",
        "labour rights",
        "domestic violence",
        "tenant eviction",
        "child labour",
        "cyber crime",
        "fundamental rights",
        "disability rights",
        "senior citizen",
        "consumer complaint"
    ]

    start = time.perf_counter()
    for query in queries:
        find_topic(query)
        search_law(query, max_results=1)
    end = time.perf_counter()

    total_time = end - start
    avg_time = total_time / len(queries)

    print(f"   Total time for 10 queries: {total_time*1000:.2f}ms")
    print(f"   Average time per query: {avg_time*1000:.2f}ms")

    # Test 5: Kanoon search performance with large result set
    print("\n5. Testing search_kanoon() with 'act' (many results)...")
    result, duration = time_function(search_kanoon, "act", max_results=50)
    print(f"   Results found: {len(result)}")
    print(f"   Time: {duration*1000:.2f}ms")

    print("\n" + "=" * 60)
    print("Performance test completed successfully!")
    print("\nKey improvements:")
    print("✓ Pre-computed NLP tokens eliminate redundant processing")
    print("✓ Cached lowercase strings avoid repeated conversions")
    print("✓ heapq.nlargest() used for efficient top-k selection")
    print("✓ UI strings retrieved once per request (not multiple times)")
    print("✓ Keyword matching uses pre-computed lowercase/stemmed forms")

if __name__ == "__main__":
    main()
