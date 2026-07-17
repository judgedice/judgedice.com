import React from 'react';

export interface TextLinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  href?: string;
  /** Append a trailing → and render inline-flex. */
  arrow?: boolean;
  /** Ink-grey instead of vermilion; darkens to ink on hover. */
  muted?: boolean;
  children?: React.ReactNode;
}

/** Inline or standalone editorial link with fill-on-hover underline. */
export function TextLink(props: TextLinkProps): JSX.Element;
