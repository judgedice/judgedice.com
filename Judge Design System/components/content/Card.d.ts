import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Editorial variant: no border except a 2px ink rule along the top. */
  framed?: boolean;
  /** Lift + soft shadow on hover (for clickable cards). */
  hover?: boolean;
  children?: React.ReactNode;
}

/**
 * Restrained content container.
 * @startingPoint section="Content" subtitle="Paper card, hairline or top-rule framed" viewport="700x260"
 */
export function Card(props: CardProps): JSX.Element;
