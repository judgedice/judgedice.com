import React from 'react';

/**
 * NavItem — NAV / Judge
 * One of the oblique nav labels (Work Life, The Exciting Stuff…). Mono
 * uppercase with an optional faint index. Vermilion when active; a thin
 * accent underline slides in on hover.
 */
export function NavItem({ index, href = '#', active = false, children, style = {}, ...rest }) {
  const [hover, setHover] = React.useState(false);
  const on = active || hover;
  return (
    <a
      href={href}
      {...rest}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: 'inline-flex',
        flexDirection: 'column',
        gap: '5px',
        fontFamily: 'var(--font-sans)',
        fontSize: 'var(--text-label)',
        textTransform: 'uppercase',
        letterSpacing: 'var(--tracking-label)',
        fontWeight: 'var(--weight-medium)',
        color: active ? 'var(--vermilion)' : 'var(--ink)',
        textDecoration: 'none',
        transition: 'color var(--dur-fast) var(--ease-out)',
        ...style,
      }}
    >
      <span style={{ display: 'inline-flex', alignItems: 'baseline', gap: '7px' }}>
        {index != null && (
          <span style={{ color: 'var(--vermilion)', fontSize: 'var(--text-meta)', fontWeight: 'var(--weight-regular)' }}>{index}</span>
        )}
        <span style={{ color: hover && !active ? 'var(--vermilion)' : undefined }}>{children}</span>
      </span>
      <span
        style={{
          height: 1,
          background: 'var(--vermilion)',
          width: on ? '100%' : '0%',
          transition: 'width var(--dur-base) var(--ease-out)',
        }}
      />
    </a>
  );
}
