/* global React, Section */
// Home Life: the exhale. Short sentences. Sounds like him at dinner.
function HomeLife({ hideLabel }) {
  const { Callout } = window.NAVJudgeDesignSystem_020eb9;
  const p = { fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.125rem, 2.2vw, 1.3125rem)', lineHeight: 1.6, color: 'var(--ink-soft)', margin: '0 0 1.1em', maxWidth: '40rem' };
  return (
    <Section id="home" index="02" label="Home Life" hideLabel={hideLabel} style={{ background: 'var(--paper-raised)' }}>
      <p style={{ ...p, fontSize: 'clamp(1.375rem, 3vw, 1.75rem)', lineHeight: 1.42, color: 'var(--ink)', maxWidth: '26ch' }}>
        When I'm not untangling enterprise tech stacks, I'm probably driving someone to band practice, arguing about something mundane, or still thinking about work.
      </p>
      <div style={{ height: 'clamp(1.5rem, 4vw, 2.5rem)' }} />
      <p style={p}>
        I have a family that puts up with me. I've been in New England long enough to have opinions about winters.
      </p>

      <div style={{ margin: 'clamp(2rem, 5vw, 3rem) 0', maxWidth: '40rem' }}>
        <Callout>
          I believe strongly in the power of a good lunch — there is no force stronger than the gravity of free lunch, and I will not be argued out of this.
        </Callout>
      </div>

      <p style={p}>
        I got into this work because I liked building things that didn't exist yet. That's still true. The tools have changed — <em style={{ fontStyle: 'italic', color: 'var(--ink)' }}>Flash is dead, long live the API</em> — but the feeling of shipping something that works is the same.
      </p>
    </Section>
  );
}
window.HomeLife = HomeLife;
