import React from 'react';

export interface FooterLink {
  label: string;
  href: string;
}

export interface FooterProps extends React.HTMLAttributes<HTMLElement> {
  /** Wordmark text; a vermilion period is appended. Default "Judge". */
  wordmark?: string;
  /** Uppercase serif tagline on the right. */
  tagline?: string;
  /** Optional row of page links between wordmark and tagline. */
  links?: FooterLink[];
}

/**
 * Shared site footer: wordmark + optional page links + serif tagline.
 * @startingPoint section="Components" subtitle="Site footer with wordmark + links" viewport="1100x120"
 */
export function Footer(props: FooterProps): JSX.Element;
