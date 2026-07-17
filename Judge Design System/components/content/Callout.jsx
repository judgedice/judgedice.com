import React from 'react';

/**
 * Callout — NAV / Judge
 * The dry aside / pull-quote treatment. A left ink rule and roomy serif
 * text — the place the free-lunch line or "I have stories" lands.
 * `variant="quote"` bumps the size for a standalone pull quote.
 */
export function Callout({ variant = 'aside', children, cite, style = {}, ...rest }) {
  const isQuote = variant === 'quote';
  return (
    <div
      {...rest}
      style={{
        borderLeft: '2px solid var(--vermilion)',
        paddingLeft: 'var(--space-5)',
        margin: 0,
        ...style,
      }}
    >
      <p
        style={{
          fontFamily: 'var(--font-serif)',
          fontStyle: 'italic',
          fontSize: isQuote ? 'var(--text-h3)' : 'var(--text-lead)',
          lineHeight: isQuote ? 'var(--leading-snug)' : 1.45,
          color: 'var(--ink)',
          margin: 0,
        }}
      >
        {children}
      </p>
      {cite && (
        <p
          style={{
            fontFamily: 'var(--font-sans)',
            fontSize: 'var(--text-meta)',
            textTransform: 'uppercase',
            letterSpacing: 'var(--tracking-label)',
            color: 'var(--ink-faint)',
            marginTop: 'var(--space-3)',
            marginBottom: 0,
          }}
        >
          {cite}
        </p>
      )}
    </div>
  );
}
