/* global React, Section */
// Work Life: earns credibility without performing it. Arc + tools as proof.
function WorkLife({ hideLabel }) {
  const { Tag, Rule, TextLink } = window.NAVJudgeDesignSystem_020eb9;
  const tools = [
    'Adobe Experience Manager', 'Adobe Journey Optimizer', 'Adobe Workfront',
    'Adobe Experience Platform', 'Adobe Target', 'Salesforce', 'Smartsheet',
    'APIs & the integrations nobody else wants to wire up',
  ];
  const p = { fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.0625rem, 2vw, 1.1875rem)', lineHeight: 1.62, color: 'var(--ink-soft)', margin: '0 0 1.1em', maxWidth: '38rem' };
  return (
    <Section id="work" index="01" label="Work Life" hideLabel={hideLabel}>
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr)', gap: 0 }}>
        <p style={{ ...p, fontSize: 'clamp(1.375rem, 3vw, 1.75rem)', lineHeight: 1.4, color: 'var(--ink)', maxWidth: 'none' }}>
          I've been building things on the internet since before it was cool. That sounds like a brag. <em style={{ fontStyle: 'italic', color: 'var(--vermilion-deep)' }}>It's mostly just a fact.</em>
        </p>
        <div style={{ height: 'clamp(1.5rem, 4vw, 2.5rem)' }} />
        <p style={p}>
          What started as Flash development at McKinsey became a 25-year career in digital architecture and marketing technology. I currently work at WillowTree, where I design and build enterprise systems for brands in financial services, real estate, hospitality, and media — mostly inside the Adobe Experience Cloud.
        </p>
        <p style={p}>
          My specialty is the space where strategy meets implementation. Where a roadmap stops being a slide and starts being a thing that works in production. I've done the architecture, run the workshops, led the demos, and when necessary jumped in to fix the integration the night before launch.
        </p>
        <p style={p}>
          I also teach Search Engine Marketing at the Chicago Portfolio School. I believe in passing things forward.
        </p>
      </div>

      <div style={{ marginTop: 'clamp(2.5rem, 6vw, 4.5rem)', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 'clamp(2rem, 5vw, 4rem)' }}>
        <div>
          <Rule label="Career arc" />
          <p style={{ fontFamily: 'var(--font-sans)', fontSize: 13, lineHeight: 1.9, color: 'var(--ink-soft)', marginTop: 20, letterSpacing: '0.01em' }}>
            Flash developer at <b style={{ color: 'var(--ink)', fontWeight: 500 }}>McKinsey &amp; Company</b>
            <span style={{ color: 'var(--vermilion)' }}> → </span>founded <b style={{ color: 'var(--ink)', fontWeight: 500 }}>The Flash Ministry</b>
            <span style={{ color: 'var(--vermilion)' }}> → </span>partner at <b style={{ color: 'var(--ink)', fontWeight: 500 }}>Pixelwelders</b>
            <span style={{ color: 'var(--vermilion)' }}> → </span>Development Director at <b style={{ color: 'var(--ink)', fontWeight: 500 }}>Vertical Inc.</b>
            <span style={{ color: 'var(--vermilion)' }}> → </span>Lead Solutions Architect at <b style={{ color: 'var(--ink)', fontWeight: 500 }}>Hanson Dodge</b>
            <span style={{ color: 'var(--vermilion)' }}> → </span><b style={{ color: 'var(--ink)', fontWeight: 500 }}>Velir</b>
            <span style={{ color: 'var(--vermilion)' }}> → </span>Principal Solutions Architect at <b style={{ color: 'var(--ink)', fontWeight: 500 }}>Maark</b>, acquired by <b style={{ color: 'var(--ink)', fontWeight: 500 }}>WillowTree</b>.
          </p>
        </div>
        <div>
          <Rule label="What I work with" />
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 20 }}>
            {tools.map((t, i) => <Tag key={t} emphasis={i < 4}>{t}</Tag>)}
          </div>
        </div>
      </div>
    </Section>
  );
}
window.WorkLife = WorkLife;
