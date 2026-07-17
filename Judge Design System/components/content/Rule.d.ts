import React from 'react';

export interface RuleProps extends React.HTMLAttributes<HTMLElement> {
  /** Optional mono label sitting on the line. */
  label?: string;
  /** hair (default) · strong · ink. */
  weight?: 'hair' | 'strong' | 'ink';
  /** Label placement when label is set. */
  align?: 'left' | 'center' | 'right';
}

/** Horizontal divider, optionally with a mono label on the line. */
export function Rule(props: RuleProps): JSX.Element;
