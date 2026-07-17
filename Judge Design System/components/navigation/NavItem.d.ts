import React from 'react';

export interface NavItemProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  /** Faint index, e.g. "01". */
  index?: string;
  href?: string;
  active?: boolean;
  children?: React.ReactNode;
}

/** One oblique nav label with index + slide-in accent underline. */
export function NavItem(props: NavItemProps): JSX.Element;
