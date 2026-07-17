# TextLink

Inline or standalone link. Vermilion by default with a subtle underline that fills to solid on hover; `muted` renders it ink-grey for links inside body prose that shouldn't shout.

```jsx
<p>Reach me at <TextLink href="mailto:judge@judgedice.com">judge@judgedice.com</TextLink>.</p>
<TextLink href="#connect" arrow>Let's talk</TextLink>
<TextLink href="#" muted>the integration nobody else wants to wire up</TextLink>
```

Props: `href`, `arrow` (trailing →, renders inline-flex), `muted`.
