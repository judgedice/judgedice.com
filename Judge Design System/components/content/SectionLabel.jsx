import React from 'react';

/**
 * SectionLabel — NAV / Judge
 * The mono uppercase kicker that opens a section (WORK LIFE, THE EXCITING
 * STUFF). Optional index number, optional trailing hairline rule that
 * runs to the edge of its container.
 */
export function SectionLabel({ index, children, rule = false, color = 'accent', style = {}, ...rest }) {
  const colorMap = {
    accent: 'var(--text-accent)',
    ink: 'var(--ink)',
    muted: 'var(--ink-faint)',
  };
  return (
    <div
      {...rest}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '14px',
        fontFamily: 'var(--font-sans)',
        fontSize: 'var(--text-label)',
        textTransform: 'uppercase',
        letterSpacing: 'var(--tracking-label)',
        fontWeight: 'var(--weight-medium)',
        color: colorMap[color],
        ...style,
      }}
    >
      {index != null && (
        <span style={{ color: 'var(--ink-faint)', fontWeight: 'var(--weight-regular)' }}>{index}</span>
      )}
      <span>{children}</span>
      {rule && (
        <span style={{ flex: 1, height: 1, background: 'var(--line)', minWidth: '24px' }} />
      )}
    </div>
  );
}
