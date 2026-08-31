import React from 'react';

interface SectionHeaderProps {
  eyebrow?: string;
  title: React.ReactNode;
  description?: React.ReactNode;
  align?: 'left' | 'center';
  className?: string;
}

export default function SectionHeader({
  eyebrow,
  title,
  description,
  align = 'center',
  className = '',
}: SectionHeaderProps) {
  const alignmentClass = align === 'center' ? 'text-center mx-auto' : 'text-left';

  return (
    <div className={`mb-12 ${alignmentClass} ${className}`} style={align === 'center' ? { maxWidth: '850px' } : undefined}>
      {eyebrow && (
        <span className="inline-block px-3 py-1 mb-4 rounded-full bg-cyan-950/40 border border-cyan-800/30 text-cyan-400 text-xs font-mono uppercase tracking-wider">
          {eyebrow}
        </span>
      )}
      
      <h2 className="text-title mb-6 gradient-text">
        {title}
      </h2>
      
      {description && (
        <div className="text-body text-text-secondary">
          {description}
        </div>
      )}
    </div>
  );
}
