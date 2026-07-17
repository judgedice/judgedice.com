import React from 'react';

/**
 * Tag — NAV / Judge
 * A mono chip for the tool lists ("what I work with"). Hairline border,
 * near-sharp corners. `emphasis` fills it in vermilion tint for the
 * ones worth pointing at.
 */
export function Tag({ children, emphasis = false, style = {}, ...rest }) {
  return (
    <span
      {...rest}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        fontFamily: 'var(--font-sans)',
        fontSize: 'var(--text-meta)',
        letterSpacing: 'var(--tracking-wide)',
        lineHeight: 1,
        padding: '6px 10px',
        borderRadius: 'var(--radius-sm)',
        border: '1px solid var(--line-strong)',
        color: emphasis ? 'var(--vermilion-deep)' : 'var(--ink-soft)',
        background: emphasis ? 'var(--accent-wash)' : 'transparent',
        borderColor: emphasis ? 'var(--accent-wash)' : 'var(--line-strong)',
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      {children}
    </span>
  );
}
