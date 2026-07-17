# Button

The editorial call-to-action for NAV / Judge. Mono uppercase label, near-sharp corners, quiet motion. Use `primary` for the one real ask on a view (there is usually only one), `secondary` for alternatives, `ghost` for low-stakes inline actions.

```jsx
<Button variant="primary" arrow>Find 30 minutes</Button>
<Button variant="secondary">Read the arc</Button>
<Button variant="ghost" size="sm">Skip</Button>
<Button as="a" href="mailto:judge@judgedice.com" arrow>Email me</Button>
```

Variants: `primary` (vermilion fill) · `secondary` (ink outline, inverts on hover) · `ghost` (text only).
Sizes: `sm` · `md` (default) · `lg`. `arrow` appends a → glyph. `disabled` dims to 45%.
