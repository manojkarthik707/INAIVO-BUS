import React from 'react';

interface PageContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

export default function PageContainer({ children, className = '', ...props }: PageContainerProps) {
  return (
    <div className={`page-container ${className}`} {...props}>
      {children}
    </div>
  );
}
