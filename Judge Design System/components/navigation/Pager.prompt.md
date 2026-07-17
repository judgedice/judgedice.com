# Pager

Prev / next navigation for the foot of a standalone page — the connective tissue once the site is separate pages rather than one scroll. A hairline-topped row with a faint direction label over the destination title in Anton. Omit an end to cap the sequence.

```jsx
<Pager
  prev={{ label: 'Work Life', href: 'work.html' }}
  next={{ label: 'The Exciting Stuff', href: 'exciting.html' }}
/>

// last page — next omitted:
<Pager prev={{ label: 'Home Life', href: 'home.html' }} />
```

Props: `prev`, `next` — each `{ label, href }`.
