#content of test_class.py

class TestClass:
    def test_one(self):
        x = "this"
        assert "s" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")