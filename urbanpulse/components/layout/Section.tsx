import React from 'react';

interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  children: React.ReactNode;
  className?: string;
  id?: string;
  ref?: React.Ref<HTMLElement>;
}

export default function Section({ children, className = '', id, ref, ...props }: SectionProps) {
  return (
    <section ref={ref} id={id} className={`section ${className}`} {...props}>
      {children}
    </section>
  );
}
