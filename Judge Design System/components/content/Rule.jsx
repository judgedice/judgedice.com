import React from 'react';

/**
 * Rule — NAV / Judge
 * A horizontal divider. Plain hairline by default; `weight="ink"` for the
 * editorial black rule. Optional centered/left label sits on the line.
 */
export function Rule({ label, weight = 'hair', align = 'left', style = {}, ...rest }) {
  const lineColor = weight === 'ink' ? 'var(--ink)' : weight === 'strong' ? 'var(--line-strong)' : 'var(--line)';
  const thickness = weight === 'ink' ? 1 : weight === 'strong' ? 1.5 : 1;

  if (!label) {
    return <hr {...rest} style={{ border: 0, borderTop: `${thickness}px solid ${lineColor}`, margin: 0, ...style }} />;
  }

  return (
    <div
      {...rest}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        flexDirection: align === 'right' ? 'row-reverse' : 'row',
        ...style,
      }}
    >
      {align === 'center' && <span style={{ flex: 1, height: thickness, background: lineColor }} />}
      <span
        style={{
          fontFamily: 'var(--font-sans)',
          fontSize: 'var(--text-meta)',
          textTransform: 'uppercase',
          letterSpacing: 'var(--tracking-label)',
          color: 'var(--ink-faint)',
          whiteSpace: 'nowrap',
        }}
      >
        {label}
      </span>
      <span style={{ flex: 1, height: thickness, background: lineColor }} />
    </div>
  );
}
