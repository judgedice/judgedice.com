/* global React */
// Shared section shell: mono numbered label opener + generous vertical rhythm.
function Section({ id, index, label, children, hideLabel = false, style = {} }) {
  const { SectionLabel } = window.NAVJudgeDesignSystem_020eb9;
  return (
    <section
      id={id}
      style={{
        padding: 'clamp(4rem, 10vw, 8rem) clamp(1.5rem, 6vw, 6rem)',
        borderTop: '1px solid var(--line)',
        ...style,
      }}
    >
      <div style={{ maxWidth: '72rem', margin: '0 auto' }}>
        {!hideLabel && <SectionLabel index={index} rule>{label}</SectionLabel>}
        <div style={{ marginTop: hideLabel ? 0 : 'clamp(2rem, 5vw, 4rem)' }}>{children}</div>
      </div>
    </section>
  );
}
window.Section = Section;
