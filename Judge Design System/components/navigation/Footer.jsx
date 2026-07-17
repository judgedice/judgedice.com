import React from 'react';

/**
 * Footer — NAV / Judge
 * The site footer: wordmark, an optional row of page links, and a serif
 * tagline. Shared across every page so the foot of the site is consistent.
 */
export function Footer({
  wordmark = 'Judge',
  tagline = 'Delivering Joy since the turn of the Century',
  links = [],
  style = {},
  ...rest
}) {
  return (
    <footer
      {...rest}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '18px 40px',
        padding: '32px clamp(1.5rem, 6vw, 6rem)',
        borderTop: '1px solid var(--line)',
        ...style,
      }}
    >
      <a
        href="index.html"
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '18px',
          color: 'var(--ink)',
          textDecoration: 'none',
          letterSpacing: '-0.01em',
        }}
      >
        {wordmark}
        <span style={{ color: 'var(--vermilion)' }}>.</span>
      </a>

      {links.length > 0 && (
        <nav style={{ display: 'flex', flexWrap: 'wrap', gap: '10px 24px' }}>
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              style={{
                fontFamily: 'var(--font-serif)',
                fontSize: 'var(--text-label)',
                textTransform: 'uppercase',
                letterSpacing: 'var(--tracking-label)',
                color: 'var(--ink-soft)',
                textDecoration: 'none',
              }}
            >
              {l.label}
            </a>
          ))}
        </nav>
      )}

      <span
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: 'var(--text-meta)',
          color: 'var(--ink-faint)',
          letterSpacing: 'var(--tracking-wide)',
          textTransform: 'uppercase',
        }}
      >
        {tagline}
      </span>
    </footer>
  );
}
