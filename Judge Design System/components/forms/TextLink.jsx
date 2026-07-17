import React from 'react';

/**
 * TextLink — NAV / Judge
 * Editorial inline / standalone link. Vermilion, subtle underline that
 * fills on hover. Optional trailing arrow for standalone CTAs.
 */
export function TextLink({ href = '#', arrow = false, muted = false, children, style = {}, ...rest }) {
  const [hover, setHover] = React.useState(false);
  const color = muted ? 'var(--ink-soft)' : 'var(--link)';
  const hoverColor = muted ? 'var(--ink)' : 'var(--link-hover)';
  return (
    <a
      href={href}
      {...rest}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        color: hover ? hoverColor : color,
        textDecorationLine: 'underline',
        textDecorationThickness: '1px',
        textUnderlineOffset: '0.18em',
        textDecorationColor: hover ? 'currentColor' : 'color-mix(in srgb, currentColor 35%, transparent)',
        transition: 'color var(--dur-fast) var(--ease-out), text-decoration-color var(--dur-fast) var(--ease-out)',
        display: arrow ? 'inline-flex' : 'inline',
        alignItems: 'center',
        gap: '0.4em',
        ...style,
      }}
    >
      {children}
      {arrow && <span aria-hidden="true" style={{ fontFamily: 'var(--font-sans)', textDecoration: 'none' }}>→</span>}
    </a>
  );
}
