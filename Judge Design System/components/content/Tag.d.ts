import React from 'react';

export interface TagProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Fill with vermilion tint for a tool worth pointing at. */
  emphasis?: boolean;
  children?: React.ReactNode;
}

/** Mono chip for tool / capability lists. */
export function Tag(props: TagProps): JSX.Element;
