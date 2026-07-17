import React from 'react';

export interface SectionLabelProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Optional index string, e.g. "01". Rendered faint before the label. */
  index?: string;
  /** Trailing hairline rule that fills remaining width. */
  rule?: boolean;
  /** accent (vermilion, default) · ink · muted. */
  color?: 'accent' | 'ink' | 'muted';
  children?: React.ReactNode;
}

/**
 * Sans uppercase section kicker.
 * @startingPoint section="Content" subtitle="Sans kicker with index + rule" viewport="700x120"
 */
export function SectionLabel(props: SectionLabelProps): JSX.Element;
