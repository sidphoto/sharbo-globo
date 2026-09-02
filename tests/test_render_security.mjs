import assert from 'node:assert/strict';
import { esc, safeIcon } from '../render_security.js';

assert.equal(
  esc("<script>alert('x')</script>"),
  '&lt;script&gt;alert(&#39;x&#39;)&lt;/script&gt;'
);
assert.equal(safeIcon('⚙'), '⚙');
assert.equal(safeIcon('<img src=x onerror=alert(1)>'), '•');
assert.equal(safeIcon('unknown', '—'), '—');

console.log('render security tests passed');
