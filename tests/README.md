# Tests

This project uses pytest for its unittests

```bash
pytest tests/
```


## Why unittests

Even the simplest of functions can contain errors:

```python
def add(x, y):
  return x + y,
```

The above function will return `tuple(sum)` instead of `sum`. Its easy to spot
this in a single function, but when your systems has dozens or even hundreds
of functions its very useful to have tests even in the simplest functions
to allow you to make big changes with confidence that you did not break a
property.


## Test Structure

Tests need to be as simple as posible, because if they are not there could be
bugs in your tests or it could be hard for your team mates to use and contribute
to your tests.
Having tests that get in the way more than they help is very frustrating and 
can make teams abandon tests all together.

To make it simpler to understand, the tests in this project try to follow the
following structure:

```python
def test_add():
  test_cases = [
    {
      "name":"3+9",
      "x": 3,  "y": 9,
      "out": 12,
    },      
    {
      "name":"12+24",
      "x": 12,  "y": 24,
      "out": 36,
    },
  ]

  for tc in test_cases:
    got = add(tc['x'], tc['y'])
    assert got == tc['out'], f"{tc['name']}: mismatch in output"
```


This structure makes it pretty easy to add new tests of the same type, while
still keeping the assertion logic in a single place.

```python
got = add(tc['x'], tc['y'])
assert got == tc['out'], f"{tc['name']}: mismatch in output"
```

Its very easy to know from these 2 lines what is being tested.
