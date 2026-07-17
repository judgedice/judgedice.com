# NavItem

One oblique nav label. Mono uppercase, optional faint `index`, vermilion when `active`, with a thin accent underline that slides in on hover. Lay them in a flex row.

```jsx
<nav style={{ display: 'flex', gap: 40 }}>
  <NavItem index="01" active>Work Life</NavItem>
  <NavItem index="02">Home Life</NavItem>
  <NavItem index="03">The Exciting Stuff</NavItem>
  <NavItem index="04">Connect</NavItem>
</nav>
```

Props: `index`, `href`, `active`.
