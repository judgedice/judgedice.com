/* global React */
// Sticky top bar: wordmark + oblique nav. Now links between separate pages;
// `current` marks the active one.
const NAV_PAGES = [
  { id: 'work', index: '01', label: 'Work Life', href: 'work.html' },
  { id: 'home', index: '02', label: 'Home Life', href: 'home.html' },
  { id: 'exciting', index: '03', label: 'The Exciting Stuff', href: 'exciting.html' },
  { id: 'connect', index: '04', label: 'Connect', href: 'connect.html' },
];

function Header({ current }) {
  const { NavItem } = window.NAVJudgeDesignSystem_020eb9;
  return (
    <header
      style={{
        position: 'sticky', top: 0, zIndex: 20,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '20px clamp(1.5rem, 6vw, 6rem)',
        background: 'color-mix(in srgb, var(--paper) 88%, transparent)',
        backdropFilter: 'blur(6px)',
        borderBottom: '1px solid var(--line)',
      }}
    >
      <a
        href="index.html"
        style={{ fontFamily: 'var(--font-serif)', fontSize: 26, color: 'var(--ink)', textDecoration: 'none', letterSpacing: '-0.01em' }}
      >
        Judge<span style={{ color: 'var(--vermilion)' }}>.</span>
      </a>
      <nav style={{ display: 'flex', gap: 'clamp(18px, 3vw, 40px)', flexWrap: 'wrap' }}>
        {NAV_PAGES.map((s) => (
          <NavItem key={s.id} index={s.index} href={s.href} active={current === s.id}>
            {s.label}
          </NavItem>
        ))}
      </nav>
    </header>
  );
}
window.Header = Header;
window.NAV_PAGES = NAV_PAGES;
