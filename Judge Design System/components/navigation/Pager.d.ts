import React from 'react';

export interface PagerLink {
  /** Destination page title, shown in Anton. */
  label: string;
  href: string;
}

export interface PagerProps extends React.HTMLAttributes<HTMLElement> {
  /** Previous page. Omit on the first page. */
  prev?: PagerLink;
  /** Next page. Omit on the last page. */
  next?: PagerLink;
}

/**
 * Prev / next page navigation for the foot of a standalone page.
 * @startingPoint section="Components" subtitle="Prev / next page pager" viewport="900x180"
 */
export function Pager(props: PagerProps): JSX.Element;
