import React from 'react';

export interface PageHeaderProps extends React.HTMLAttributes<HTMLElement> {
  /** Faint index string before the kicker, e.g. "01". */
  index?: string;
  /** Uppercase serif kicker beside the index. */
  kicker?: string;
  /** The Anton display title (rendered UPPERCASE). */
  title: React.ReactNode;
  /** Optional serif italic lead beneath the title. */
  lead?: React.ReactNode;
  /** paper (default) · ink — flips text colors for the dark background. */
  tone?: 'paper' | 'ink';
}

/**
 * Standalone-page masthead: numbered kicker + Anton title + serif lead.
 * @startingPoint section="Content" subtitle="Page masthead: kicker + Anton title + lead" viewport="900x360"
 */
export function PageHeader(props: PageHeaderProps): JSX.Element;
