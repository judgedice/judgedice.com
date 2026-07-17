/* global React, Section */
// The Exciting Stuff: what he actually does, in plain English. Dry, direct.
// No icons. No three-word headlines with three bullets. Prose, framed.
function ExcitingStuff({ hideLabel }) {
  const { Card } = window.NAVJudgeDesignSystem_020eb9;
  const items = [
    {
      t: 'Marketing Technology Architecture',
      d: "Designing end-to-end digital marketing systems that hold together under real conditions — across strategy, platform selection, integration design, and build. The kind of architecture that doesn't collapse when a stakeholder changes their mind in month three.",
    },
    {
      t: 'Adobe Experience Cloud',
      d: "AEM, Adobe Journey Optimizer, Workfront, Target, AEP. I've shipped all of it, across industries and client contexts. I know which parts to use, which to skip, and which will require a ticket that becomes a different ticket. I have stories.",
    },
    {
      t: 'Marketing Operations & Automation',
      d: "Building the workflows and integrations that let marketing teams actually use the platforms they've paid for. Approval flows that don't require a PhD. Automations that run without babysitting. The operational layer that makes the strategy real.",
    },
    {
      t: 'Workshop Facilitation',
      d: "I've run a lot of them. Discovery, architecture, stakeholder alignment. I know how to get a room full of people with competing priorities to walk out with decisions made and next steps owned. This is harder than it sounds.",
    },
    {
      t: 'Strategy & Solutions Architecture',
      d: 'The part before the build. What are we trying to do? What does the ecosystem need to look like? What do we build first and what do we defer? This is where 25 years of pattern-matching earns its keep.',
    },
    {
      t: 'Teaching & Consulting',
      d: "Search Engine Marketing at the Chicago Portfolio School. Digital consulting for educational programs. If you're building a curriculum or a team, I can help.",
    },
  ];
  return (
    <Section id="exciting" index="03" label="The Exciting Stuff" hideLabel={hideLabel}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 'clamp(1rem, 2vw, 1.5rem)' }}>
        {items.map((it, i) => (
          <Card key={it.t} framed>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
              <span style={{ fontFamily: 'var(--font-sans)', fontSize: 12, color: 'var(--vermilion)' }}>{String(i + 1).padStart(2, '0')}</span>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.375rem, 2.4vw, 1.625rem)', fontWeight: 400, letterSpacing: '-0.01em', lineHeight: 1.15, margin: 0, color: 'var(--ink)' }}>{it.t}</h3>
            </div>
            <p style={{ fontFamily: 'var(--font-serif)', fontSize: '1.0625rem', lineHeight: 1.6, color: 'var(--ink-soft)', margin: '14px 0 0' }}>{it.d}</p>
          </Card>
        ))}
      </div>
    </Section>
  );
}
window.ExcitingStuff = ExcitingStuff;
