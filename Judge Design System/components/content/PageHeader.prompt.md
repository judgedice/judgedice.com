# PageHeader

The masthead that opens a standalone page — the separate-page counterpart to `SectionLabel`. Numbered serif kicker with a hairline rule, an Anton uppercase title, and an optional serif italic lead. Drop it at the top of each page.

```jsx
<PageHeader index="01" kicker="Work Life" title="Delivering joy, in production." lead="Twenty-five years of digital architecture, mostly inside the Adobe Experience Cloud." />

// on the dark Connect page:
<PageHeader index="04" kicker="Connect" title="Let's talk." tone="ink" />
```

Props: `index`, `kicker`, `title` (required), `lead`, `tone` (`paper` default · `ink`).
