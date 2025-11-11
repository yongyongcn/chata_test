from mypg.main import say_hello
def test_say_hello():
    assert say_hello("Alice") == "Hello, Alice!"
    print("Test passed for Alice")
    assert say_hello("Bob") == "Hello, Bob!"