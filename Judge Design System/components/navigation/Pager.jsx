import React from 'react';

/**
 * Pager — NAV / Judge
 * Prev / next page navigation for the foot of a standalone page. Two ends of
 * a hairline-topped row: a faint uppercase serif direction label and the
 * destination page title in Anton. Either end may be omitted.
 */
function PagerEnd({ dir, item, align }) {
  const [hover, setHover] = React.useState(false);
  const isNext = dir === 'next';
  return (
    <a
      href={item.href}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: 'inline-flex',
        flexDirection: 'column',
        gap: '8px',
        textDecoration: 'none',
        textAlign: align,
        alignItems: isNext ? 'flex-end' : 'flex-start',
      }}
    >
      <span
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: 'var(--text-meta)',
          textTransform: 'uppercase',
          letterSpacing: 'var(--tracking-label)',
          color: 'var(--ink-faint)',
        }}
      >
        {isNext ? 'Next' : 'Previous'}
      </span>
      <span
        style={{
          display: 'inline-flex',
          alignItems: 'baseline',
          gap: '10px',
          fontFamily: 'var(--font-display)',
          textTransform: 'uppercase',
          fontSize: 'clamp(1.375rem, 3vw, 2rem)',
          lineHeight: 1.0,
          letterSpacing: '-0.005em',
          color: hover ? 'var(--vermilion)' : 'var(--ink)',
          transition: 'color var(--dur-fast) var(--ease-out)',
        }}
      >
        {!isNext && <span style={{ color: 'var(--vermilion)' }}>←</span>}
        <span>{item.label}</span>
        {isNext && <span style={{ color: 'var(--vermilion)' }}>→</span>}
      </span>
    </a>
  );
}

export function Pager({ prev, next, style = {}, ...rest }) {
  return (
    <nav
      {...rest}
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        gap: '24px',
        padding: 'clamp(2rem, 5vw, 3rem) clamp(1.5rem, 6vw, 6rem)',
        borderTop: '1px solid var(--line)',
        ...style,
      }}
    >
      <div>{prev && <PagerEnd dir="prev" item={prev} align="left" />}</div>
      <div>{next && <PagerEnd dir="next" item={next} align="right" />}</div>
    </nav>
  );
}
