def add(a, b):
    print(f"Adding {a} and {b}")
    a = a + 10
    return a + b

if __name__ == "__main__":
    result = add(5, 7)
    print(f"Result is {result}")