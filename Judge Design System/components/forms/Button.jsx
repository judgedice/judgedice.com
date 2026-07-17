import React from 'react';

/**
 * Button — NAV / Judge
 * Editorial button. Confident, quiet, never shouty.
 * Variants: primary (vermilion), secondary (ink outline), ghost (text only).
 */
export function Button({
  variant = 'primary',
  size = 'md',
  as = 'button',
  href,
  disabled = false,
  arrow = false,
  children,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: { padding: '8px 16px', fontSize: '12px' },
    md: { padding: '13px 26px', fontSize: '13px' },
    lg: { padding: '17px 34px', fontSize: '14px' },
  };

  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.6em',
    fontFamily: 'var(--font-sans)',
    textTransform: 'uppercase',
    letterSpacing: 'var(--tracking-label)',
    fontWeight: 'var(--weight-medium)',
    lineHeight: 1,
    borderRadius: 'var(--radius-sm)',
    border: '1px solid transparent',
    cursor: disabled ? 'not-allowed' : 'pointer',
    textDecoration: 'none',
    transition: 'background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out), border-color var(--dur-fast) var(--ease-out)',
    opacity: disabled ? 0.45 : 1,
    ...sizes[size],
  };

  const variants = {
    primary: {
      background: 'var(--accent)',
      color: 'var(--text-on-accent)',
      borderColor: 'var(--accent)',
    },
    secondary: {
      background: 'transparent',
      color: 'var(--ink)',
      borderColor: 'var(--ink)',
    },
    ghost: {
      background: 'transparent',
      color: 'var(--ink)',
      borderColor: 'transparent',
      paddingLeft: 0,
      paddingRight: 0,
    },
  };

  const hoverStyles = {
    primary: { background: 'var(--accent-hover)', borderColor: 'var(--accent-hover)' },
    secondary: { background: 'var(--ink)', color: 'var(--paper)' },
    ghost: { color: 'var(--accent)' },
  };

  const [hover, setHover] = React.useState(false);
  const composed = {
    ...base,
    ...variants[variant],
    ...(hover && !disabled ? hoverStyles[variant] : {}),
    ...style,
  };

  const Tag = as === 'a' || href ? 'a' : 'button';
  const extra = Tag === 'a' ? { href } : { disabled };

  return (
    <Tag
      {...extra}
      {...rest}
      style={composed}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      {children}
      {arrow && <span aria-hidden="true" style={{ fontFamily: 'var(--font-sans)' }}>→</span>}
    </Tag>
  );
}
