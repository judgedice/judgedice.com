# UI Kit — NAV / Judge Personal Site

A high-fidelity, interactive recreation of Judge's single-page personal site: the editorial scroll through **Work Life · Home Life · The Exciting Stuff · Connect**, opening on the hero tagline moment.

## Files
- `index.html` — mounts the app; loads the DS bundle, React, Babel, then each section file.
- `App.jsx` — composition + scroll-driven active-nav (IntersectionObserver) + smooth-scroll nav.
- `Header.jsx` — sticky bar: wordmark + oblique `NavItem` row.
- `Hero.jsx` — the tagline, with one staggered load reveal.
- `Section.jsx` — shared numbered-section shell (`SectionLabel` opener).
- `WorkLife.jsx` — prose + career arc (mono) + tool tags (`Tag`).
- `HomeLife.jsx` — the exhale; the free-lunch `Callout`.
- `ExcitingStuff.jsx` — six framed `Card`s, plain-English capability prose.
- `Connect.jsx` — one ask; ink section, single email `Button`.

## Built from
The NAV/Judge component primitives (`Button`, `TextLink`, `NavItem`, `SectionLabel`, `Tag`, `Card`, `Rule`, `Callout`) and the global tokens in `styles.css`. Copy verbatim from the brand copy brief.

## Interactions
- Nav clicks smooth-scroll to the section (no `scrollIntoView`); the active label tracks scroll position.
- Hover: nav underline slides in, links fill their underline, buttons darken.
- Reduced-motion disables the hero reveal.
