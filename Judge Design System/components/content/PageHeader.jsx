import React from 'react';

/**
 * PageHeader — NAV / Judge
 * The masthead that opens a standalone page. A numbered serif kicker with an
 * optional hairline rule, an Anton display title (always uppercase), and an
 * optional serif lead. Set tone="ink" when it sits on the dark background.
 */
export function PageHeader({
  index,
  kicker,
  title,
  lead,
  tone = 'paper',
  style = {},
  ...rest
}) {
  const onInk = tone === 'ink';
  const titleColor = onInk ? 'var(--paper)' : 'var(--ink)';
  const kickerColor = onInk ? 'color-mix(in srgb, var(--paper) 82%, transparent)' : 'var(--vermilion)';
  const ruleColor = onInk ? 'color-mix(in srgb, var(--paper) 30%, transparent)' : 'var(--line)';
  const leadColor = onInk ? 'color-mix(in srgb, var(--paper) 80%, transparent)' : 'var(--ink-soft)';

  return (
    <header
      {...rest}
      style={{
        padding: 'clamp(3.5rem, 9vw, 6.5rem) clamp(1.5rem, 6vw, 6rem) clamp(1.75rem, 4vw, 2.75rem)',
        ...style,
      }}
    >
      {(index != null || kicker) && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '14px',
            fontFamily: 'var(--font-serif)',
            fontSize: 'var(--text-label)',
            textTransform: 'uppercase',
            letterSpacing: 'var(--tracking-label)',
            fontWeight: 'var(--weight-medium)',
            color: kickerColor,
            marginBottom: '20px',
          }}
        >
          {index != null && (
            <span style={{ color: onInk ? kickerColor : 'var(--ink-faint)', fontWeight: 'var(--weight-regular)' }}>{index}</span>
          )}
          {kicker && <span>{kicker}</span>}
          <span style={{ flex: 1, height: 1, background: ruleColor, minWidth: '24px' }} />
        </div>
      )}
      <h1
        style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 'var(--weight-regular)',
          textTransform: 'uppercase',
          fontSize: 'clamp(2.75rem, 8vw, 6rem)',
          lineHeight: 'var(--leading-tight)',
          letterSpacing: '-0.005em',
          color: titleColor,
          margin: 0,
          maxWidth: '18ch',
        }}
      >
        {title}
      </h1>
      {lead && (
        <p
          style={{
            fontFamily: 'var(--font-serif)',
            fontStyle: 'italic',
            fontSize: 'clamp(1.125rem, 2.4vw, 1.5rem)',
            lineHeight: 1.4,
            color: leadColor,
            margin: '22px 0 0',
            maxWidth: '40rem',
          }}
        >
          {lead}
        </p>
      )}
    </header>
  );
}
