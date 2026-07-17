/* global React, Section */
// Connect: one ask, made obvious. Here's how, here's why, here's the address.
function Connect({ hideLabel }) {
  const { Button } = window.NAVJudgeDesignSystem_020eb9;
  return (
    <Section id="connect" index="04" label="Connect" hideLabel={hideLabel} style={{ background: 'var(--ink)' }}>
      <div style={{ maxWidth: '44rem' }}>
        <p style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.125rem, 2.4vw, 1.5rem)', lineHeight: 1.5, color: 'color-mix(in srgb, var(--paper) 82%, transparent)', margin: 0, maxWidth: '36rem' }}>
          I'm responsive on email, better on a call, and genuinely bad at LinkedIn DMs.
        </p>
        <p style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.0625rem, 2vw, 1.25rem)', lineHeight: 1.6, color: 'color-mix(in srgb, var(--paper) 66%, transparent)', margin: '20px 0 0', maxWidth: '38rem' }}>
          If you're working on something in the Adobe Experience Cloud space and need a senior architect — or just need someone to talk through a hairy integration — I'm interested. Find 30 minutes.
        </p>

        <div style={{ marginTop: 'clamp(2.5rem, 6vw, 3.5rem)', display: 'flex', alignItems: 'center', gap: 28, flexWrap: 'wrap' }}>
          <Button as="a" href="mailto:judge@judgedice.com" variant="primary" size="lg" arrow>
            judge@judgedice.com
          </Button>
        </div>
      </div>
    </Section>
  );
}
window.Connect = Connect;
