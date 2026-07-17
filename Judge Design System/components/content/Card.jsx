import React from 'react';

/**
 * Card — NAV / Judge
 * A restrained content container. Paper-raised surface, hairline border,
 * near-sharp corners. `framed` swaps the hairline for a top ink rule
 * (editorial index-card feel). No heavy shadows — print doesn't cast them.
 */
export function Card({ framed = false, hover = false, children, style = {}, ...rest }) {
  const [isHover, setIsHover] = React.useState(false);
  return (
    <div
      {...rest}
      onMouseEnter={() => hover && setIsHover(true)}
      onMouseLeave={() => hover && setIsHover(false)}
      style={{
        background: 'var(--surface-card)',
        border: framed ? 'none' : '1px solid var(--line)',
        borderTop: framed ? '2px solid var(--ink)' : '1px solid var(--line)',
        borderRadius: framed ? '0' : 'var(--radius-card)',
        padding: 'var(--space-6)',
        transition: 'box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)',
        boxShadow: hover && isHover ? 'var(--shadow-card)' : 'none',
        transform: hover && isHover ? 'translateY(-2px)' : 'none',
        ...style,
      }}
    >
      {children}
    </div>
  );
}
