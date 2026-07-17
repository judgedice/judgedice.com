# Footer

The shared site footer — wordmark on the left, an optional row of page links, and an uppercase serif tagline on the right. Drop the same instance at the foot of every page so the site closes consistently. The wordmark links home.

```jsx
<Footer
  links={[
    { label: 'Work Life', href: 'work.html' },
    { label: 'Home Life', href: 'home.html' },
    { label: 'The Exciting Stuff', href: 'exciting.html' },
    { label: 'Connect', href: 'connect.html' },
  ]}
/>
```

Props: `wordmark` (default "Judge"), `tagline`, `links` (each `{ label, href }`).
