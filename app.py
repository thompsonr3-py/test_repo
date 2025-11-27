def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference between two numbers (a - b)."""
    return a - b


if __name__ == "__main__":
    # Simple CLI for manual verification
    import argparse
    parser = argparse.ArgumentParser(description="Add two numbers")
    parser.add_argument("a", type=float, help="First number")
    parser.add_argument("b", type=float, help="Second number")
    args = parser.parse_args()
    print(add(args.a, args.b))
