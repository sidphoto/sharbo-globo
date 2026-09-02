// Shared rendering guards for values that cross the JSON → HTML boundary.
// Unknown icons intentionally fall back to a plain text bullet.
const SAFE_ICONS = new Set([
  '🌐', '🏛️', '📈', '🧠', '⌘', '💾', '🏭', '💧', '🧪', '🏢', '👥', '🇹🇼',
  '↗', '•', '⚙', '→'
]);

export function esc(value = '') {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[ch]));
}

export function safeIcon(value, fallback = '•') {
  const icon = String(value ?? '').trim();
  return SAFE_ICONS.has(icon) ? icon : fallback;
}
