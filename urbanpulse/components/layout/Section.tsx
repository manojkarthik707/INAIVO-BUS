import React from 'react';

interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  children: React.ReactNode;
  className?: string;
  id?: string;
}

export default function Section({ children, className = '', id, ...props }: SectionProps) {
  return (
    <section id={id} className={`section ${className}`} {...props}>
      {children}
    </section>
  );
}
