import React from 'react';

export interface CalloutProps extends React.HTMLAttributes<HTMLDivElement> {
  /** aside (lead-size, default) · quote (larger pull quote). */
  variant?: 'aside' | 'quote';
  /** Optional mono attribution line beneath the text. */
  cite?: string;
  children?: React.ReactNode;
}

/**
 * Dry aside / pull-quote with a left vermilion rule.
 * @startingPoint section="Content" subtitle="Italic pull-quote with left accent rule" viewport="700x200"
 */
export function Callout(props: CalloutProps): JSX.Element;
