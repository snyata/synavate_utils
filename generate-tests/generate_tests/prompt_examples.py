python_examples = """
Example Python tests using pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(3, 2) == 1
    assert subtract(1, -1) == 2
"""

ts_examples = """
Example TypeScript tests using Jest

test('adds 1 + 2 to equal 3', () => {
  expect(add(1, 2)).toBe(3);
});

test('subtracts 5 - 2 to equal 3', () => {
  expect(subtract(5, 2)).toBe(3);
});
"""

rs_examples = """
Example Rust tests using cargo test

#[test]
fn test_add() {
    assert_eq!(add(2, 3), 5);
    assert_eq!(add(-1, 1), 0);
}

#[test]
fn test_subtract() {
    assert_eq!(subtract(3, 2), 1);
    assert_eq!(subtract(1, -1), 2);
}
"""