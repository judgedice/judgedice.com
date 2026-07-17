/* global React */
// Hero: the tagline moment. Statement, not description. One staggered reveal.
function Hero() {
  return (
    <section
      id="top"
      style={{
        minHeight: 'calc(100vh - 66px)',
        display: 'flex', flexDirection: 'column', justifyContent: 'center',
        padding: '0 clamp(1.5rem, 6vw, 6rem)',
        maxWidth: '78rem',
      }}
    >
      <div className="reveal" style={{ animationDelay: '80ms' }}>
        <span
          style={{
            fontFamily: 'var(--font-sans)', fontSize: 13, textTransform: 'uppercase',
            letterSpacing: '0.14em', color: 'var(--vermilion)', fontWeight: 500,
          }}
        >
          Judge — Digital Architect
        </span>
      </div>
      <h1
        className="reveal"
        style={{
          animationDelay: '180ms',
          fontFamily: 'var(--font-display)', fontWeight: 400,
          textTransform: 'uppercase',
          fontSize: 'clamp(3rem, 10vw, 7.5rem)', lineHeight: 1.02,
          letterSpacing: '-0.005em', color: 'var(--ink)',
          margin: '28px 0 0', maxWidth: '15ch',
        }}
      >
        Delivering <em style={{ fontStyle: 'normal', color: 'var(--vermilion)' }}>Joy</em> since the turn of the Century.
      </h1>
      <p
        className="reveal"
        style={{
          animationDelay: '320ms',
          fontFamily: 'var(--font-sans)', fontSize: 13, color: 'var(--ink-faint)',
          letterSpacing: '0.04em', marginTop: 40, textTransform: 'uppercase',
        }}
      >
        Work Life · Home Life · The Exciting Stuff · Connect
      </p>
    </section>
  );
}
window.Hero = Hero;
