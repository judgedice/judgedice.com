import React from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.HTMLAttributes<HTMLElement> {
  /** Visual weight. primary = vermilion fill, secondary = ink outline, ghost = text only. */
  variant?: ButtonVariant;
  /** md is default. */
  size?: ButtonSize;
  /** Render as 'a' for links; passing href does this automatically. */
  as?: 'button' | 'a';
  href?: string;
  disabled?: boolean;
  /** Append a → glyph (mono arrow). */
  arrow?: boolean;
  children?: React.ReactNode;
}

/**
 * Primary call-to-action button in the NAV / Judge system.
 * @startingPoint section="Forms" subtitle="Mono-label editorial button, 3 variants" viewport="700x150"
 */
export function Button(props: ButtonProps): JSX.Element;
