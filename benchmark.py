import time
import tracemalloc

from src.model import load_model
from src.data import FEATURES


def create_transaction():
    """
    Create one privacy-safe simulated transaction for benchmarking.

    Returns:
        Dictionary containing the same features used by the TrustPay model.
    """
    return {
        "amount": 2500.0,
        "hour": 14,
        "new_beneficiary": 0,
        "transaction_count": 2,
        "device_changed": 0,
        "failed_attempts": 0,
        "amount_ratio": 1.0,
        "account_age_days": 365,
    }


def run_benchmark(number_of_samples=100):
    """
    Measure TrustPay model inference performance.

    Args:
        number_of_samples: Number of transactions to predict.

    Returns:
        Dictionary containing measured latency and memory statistics.
    """
    bundle = load_model()
    model = bundle["model"]

    transaction = create_transaction()

    rows = [
        [transaction[feature] for feature in FEATURES]
        for _ in range(number_of_samples)
    ]

    # Warm-up prediction
    model.predict_proba(rows[:1])

    # Measure inference time
    start_time = time.perf_counter()

    model.predict_proba(rows)

    end_time = time.perf_counter()

    total_time = end_time - start_time

    average_latency_ms = (total_time / number_of_samples) * 1000

    throughput = number_of_samples / total_time

    # Measure memory usage
    tracemalloc.start()

    model.predict_proba(rows)

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return {
        "samples": number_of_samples,
        "total_time": total_time,
        "average_latency_ms": average_latency_ms,
        "throughput": throughput,
        "peak_memory_mb": peak_memory / (1024 * 1024),
    }


if __name__ == "__main__":
    print("=" * 45)
    print("TrustPay Inference Benchmark")
    print("=" * 45)

    results = run_benchmark(100)

    print(f"Samples: {results['samples']}")
    print(f"Total inference time: {results['total_time']:.4f} seconds")
    print(f"Average latency: {results['average_latency_ms']:.3f} ms")
    print(f"Throughput: {results['throughput']:.2f} transactions/second")
    print(f"Peak memory: {results['peak_memory_mb']:.2f} MB")

    print("=" * 45)