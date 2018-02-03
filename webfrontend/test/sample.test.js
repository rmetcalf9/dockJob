
function sum(a, b) {
  return a + b;
}

test('sample jest test', () => {
  expect(sum(1, 2)).toBe(3);
});
