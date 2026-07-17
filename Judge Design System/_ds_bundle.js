/* @ds-bundle: {"format":4,"namespace":"NAVJudgeDesignSystem_020eb9","components":[{"name":"Callout","sourcePath":"components/content/Callout.jsx"},{"name":"Card","sourcePath":"components/content/Card.jsx"},{"name":"PageHeader","sourcePath":"components/content/PageHeader.jsx"},{"name":"Rule","sourcePath":"components/content/Rule.jsx"},{"name":"SectionLabel","sourcePath":"components/content/SectionLabel.jsx"},{"name":"Tag","sourcePath":"components/content/Tag.jsx"},{"name":"Button","sourcePath":"components/forms/Button.jsx"},{"name":"TextLink","sourcePath":"components/forms/TextLink.jsx"},{"name":"Footer","sourcePath":"components/navigation/Footer.jsx"},{"name":"NavItem","sourcePath":"components/navigation/NavItem.jsx"},{"name":"Pager","sourcePath":"components/navigation/Pager.jsx"}],"sourceHashes":{"components/content/Callout.jsx":"edd3ccb9f48a","components/content/Card.jsx":"105ca504cbe3","components/content/PageHeader.jsx":"758037479ad5","components/content/Rule.jsx":"f84bcb097abf","components/content/SectionLabel.jsx":"5311f810bdf8","components/content/Tag.jsx":"6a17a10278c4","components/forms/Button.jsx":"701df98bd75b","components/forms/TextLink.jsx":"47336d653026","components/navigation/Footer.jsx":"11711ff502ab","components/navigation/NavItem.jsx":"324ef201a3a2","components/navigation/Pager.jsx":"bbad3aae25ed","ui_kits/nav-site/Connect.jsx":"f1d6b811f34f","ui_kits/nav-site/ExcitingStuff.jsx":"89cc912aadd7","ui_kits/nav-site/Header.jsx":"6795b1b0a746","ui_kits/nav-site/Hero.jsx":"68496ed4c3b1","ui_kits/nav-site/HomeLife.jsx":"416c590671e7","ui_kits/nav-site/Page.jsx":"e360a79747fc","ui_kits/nav-site/Section.jsx":"452d2f548802","ui_kits/nav-site/WorkLife.jsx":"3bc819a8eb4f"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.NAVJudgeDesignSystem_020eb9 = window.NAVJudgeDesignSystem_020eb9 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/content/Callout.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Callout — NAV / Judge
 * The dry aside / pull-quote treatment. A left ink rule and roomy serif
 * text — the place the free-lunch line or "I have stories" lands.
 * `variant="quote"` bumps the size for a standalone pull quote.
 */
function Callout({
  variant = 'aside',
  children,
  cite,
  style = {},
  ...rest
}) {
  const isQuote = variant === 'quote';
  return /*#__PURE__*/React.createElement("div", _extends({}, rest, {
    style: {
      borderLeft: '2px solid var(--vermilion)',
      paddingLeft: 'var(--space-5)',
      margin: 0,
      ...style
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontStyle: 'italic',
      fontSize: isQuote ? 'var(--text-h3)' : 'var(--text-lead)',
      lineHeight: isQuote ? 'var(--leading-snug)' : 1.45,
      color: 'var(--ink)',
      margin: 0
    }
  }, children), cite && /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-meta)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      color: 'var(--ink-faint)',
      marginTop: 'var(--space-3)',
      marginBottom: 0
    }
  }, cite));
}
Object.assign(__ds_scope, { Callout });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Callout.jsx", error: String((e && e.message) || e) }); }

// components/content/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Card — NAV / Judge
 * A restrained content container. Paper-raised surface, hairline border,
 * near-sharp corners. `framed` swaps the hairline for a top ink rule
 * (editorial index-card feel). No heavy shadows — print doesn't cast them.
 */
function Card({
  framed = false,
  hover = false,
  children,
  style = {},
  ...rest
}) {
  const [isHover, setIsHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", _extends({}, rest, {
    onMouseEnter: () => hover && setIsHover(true),
    onMouseLeave: () => hover && setIsHover(false),
    style: {
      background: 'var(--surface-card)',
      border: framed ? 'none' : '1px solid var(--line)',
      borderTop: framed ? '2px solid var(--ink)' : '1px solid var(--line)',
      borderRadius: framed ? '0' : 'var(--radius-card)',
      padding: 'var(--space-6)',
      transition: 'box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)',
      boxShadow: hover && isHover ? 'var(--shadow-card)' : 'none',
      transform: hover && isHover ? 'translateY(-2px)' : 'none',
      ...style
    }
  }), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Card.jsx", error: String((e && e.message) || e) }); }

// components/content/PageHeader.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * PageHeader — NAV / Judge
 * The masthead that opens a standalone page. A numbered serif kicker with an
 * optional hairline rule, an Anton display title (always uppercase), and an
 * optional serif lead. Set tone="ink" when it sits on the dark background.
 */
function PageHeader({
  index,
  kicker,
  title,
  lead,
  tone = 'paper',
  style = {},
  ...rest
}) {
  const onInk = tone === 'ink';
  const titleColor = onInk ? 'var(--paper)' : 'var(--ink)';
  const kickerColor = onInk ? 'color-mix(in srgb, var(--paper) 82%, transparent)' : 'var(--vermilion)';
  const ruleColor = onInk ? 'color-mix(in srgb, var(--paper) 30%, transparent)' : 'var(--line)';
  const leadColor = onInk ? 'color-mix(in srgb, var(--paper) 80%, transparent)' : 'var(--ink-soft)';
  return /*#__PURE__*/React.createElement("header", _extends({}, rest, {
    style: {
      padding: 'clamp(3.5rem, 9vw, 6.5rem) clamp(1.5rem, 6vw, 6rem) clamp(1.75rem, 4vw, 2.75rem)',
      ...style
    }
  }), (index != null || kicker) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '14px',
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--text-label)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      fontWeight: 'var(--weight-medium)',
      color: kickerColor,
      marginBottom: '20px'
    }
  }, index != null && /*#__PURE__*/React.createElement("span", {
    style: {
      color: onInk ? kickerColor : 'var(--ink-faint)',
      fontWeight: 'var(--weight-regular)'
    }
  }, index), kicker && /*#__PURE__*/React.createElement("span", null, kicker), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      height: 1,
      background: ruleColor,
      minWidth: '24px'
    }
  })), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 'var(--weight-regular)',
      textTransform: 'uppercase',
      fontSize: 'clamp(2.75rem, 8vw, 6rem)',
      lineHeight: 'var(--leading-tight)',
      letterSpacing: '-0.005em',
      color: titleColor,
      margin: 0,
      maxWidth: '18ch'
    }
  }, title), lead && /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontStyle: 'italic',
      fontSize: 'clamp(1.125rem, 2.4vw, 1.5rem)',
      lineHeight: 1.4,
      color: leadColor,
      margin: '22px 0 0',
      maxWidth: '40rem'
    }
  }, lead));
}
Object.assign(__ds_scope, { PageHeader });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/PageHeader.jsx", error: String((e && e.message) || e) }); }

// components/content/Rule.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Rule — NAV / Judge
 * A horizontal divider. Plain hairline by default; `weight="ink"` for the
 * editorial black rule. Optional centered/left label sits on the line.
 */
function Rule({
  label,
  weight = 'hair',
  align = 'left',
  style = {},
  ...rest
}) {
  const lineColor = weight === 'ink' ? 'var(--ink)' : weight === 'strong' ? 'var(--line-strong)' : 'var(--line)';
  const thickness = weight === 'ink' ? 1 : weight === 'strong' ? 1.5 : 1;
  if (!label) {
    return /*#__PURE__*/React.createElement("hr", _extends({}, rest, {
      style: {
        border: 0,
        borderTop: `${thickness}px solid ${lineColor}`,
        margin: 0,
        ...style
      }
    }));
  }
  return /*#__PURE__*/React.createElement("div", _extends({}, rest, {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      flexDirection: align === 'right' ? 'row-reverse' : 'row',
      ...style
    }
  }), align === 'center' && /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      height: thickness,
      background: lineColor
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-meta)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      color: 'var(--ink-faint)',
      whiteSpace: 'nowrap'
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      height: thickness,
      background: lineColor
    }
  }));
}
Object.assign(__ds_scope, { Rule });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Rule.jsx", error: String((e && e.message) || e) }); }

// components/content/SectionLabel.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * SectionLabel — NAV / Judge
 * The mono uppercase kicker that opens a section (WORK LIFE, THE EXCITING
 * STUFF). Optional index number, optional trailing hairline rule that
 * runs to the edge of its container.
 */
function SectionLabel({
  index,
  children,
  rule = false,
  color = 'accent',
  style = {},
  ...rest
}) {
  const colorMap = {
    accent: 'var(--text-accent)',
    ink: 'var(--ink)',
    muted: 'var(--ink-faint)'
  };
  return /*#__PURE__*/React.createElement("div", _extends({}, rest, {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '14px',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-label)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      fontWeight: 'var(--weight-medium)',
      color: colorMap[color],
      ...style
    }
  }), index != null && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--ink-faint)',
      fontWeight: 'var(--weight-regular)'
    }
  }, index), /*#__PURE__*/React.createElement("span", null, children), rule && /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      height: 1,
      background: 'var(--line)',
      minWidth: '24px'
    }
  }));
}
Object.assign(__ds_scope, { SectionLabel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/SectionLabel.jsx", error: String((e && e.message) || e) }); }

// components/content/Tag.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Tag — NAV / Judge
 * A mono chip for the tool lists ("what I work with"). Hairline border,
 * near-sharp corners. `emphasis` fills it in vermilion tint for the
 * ones worth pointing at.
 */
function Tag({
  children,
  emphasis = false,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({}, rest, {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-meta)',
      letterSpacing: 'var(--tracking-wide)',
      lineHeight: 1,
      padding: '6px 10px',
      borderRadius: 'var(--radius-sm)',
      border: '1px solid var(--line-strong)',
      color: emphasis ? 'var(--vermilion-deep)' : 'var(--ink-soft)',
      background: emphasis ? 'var(--accent-wash)' : 'transparent',
      borderColor: emphasis ? 'var(--accent-wash)' : 'var(--line-strong)',
      whiteSpace: 'nowrap',
      ...style
    }
  }), children);
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Tag.jsx", error: String((e && e.message) || e) }); }

// components/forms/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Button — NAV / Judge
 * Editorial button. Confident, quiet, never shouty.
 * Variants: primary (vermilion), secondary (ink outline), ghost (text only).
 */
function Button({
  variant = 'primary',
  size = 'md',
  as = 'button',
  href,
  disabled = false,
  arrow = false,
  children,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: {
      padding: '8px 16px',
      fontSize: '12px'
    },
    md: {
      padding: '13px 26px',
      fontSize: '13px'
    },
    lg: {
      padding: '17px 34px',
      fontSize: '14px'
    }
  };
  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.6em',
    fontFamily: 'var(--font-sans)',
    textTransform: 'uppercase',
    letterSpacing: 'var(--tracking-label)',
    fontWeight: 'var(--weight-medium)',
    lineHeight: 1,
    borderRadius: 'var(--radius-sm)',
    border: '1px solid transparent',
    cursor: disabled ? 'not-allowed' : 'pointer',
    textDecoration: 'none',
    transition: 'background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out), border-color var(--dur-fast) var(--ease-out)',
    opacity: disabled ? 0.45 : 1,
    ...sizes[size]
  };
  const variants = {
    primary: {
      background: 'var(--accent)',
      color: 'var(--text-on-accent)',
      borderColor: 'var(--accent)'
    },
    secondary: {
      background: 'transparent',
      color: 'var(--ink)',
      borderColor: 'var(--ink)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--ink)',
      borderColor: 'transparent',
      paddingLeft: 0,
      paddingRight: 0
    }
  };
  const hoverStyles = {
    primary: {
      background: 'var(--accent-hover)',
      borderColor: 'var(--accent-hover)'
    },
    secondary: {
      background: 'var(--ink)',
      color: 'var(--paper)'
    },
    ghost: {
      color: 'var(--accent)'
    }
  };
  const [hover, setHover] = React.useState(false);
  const composed = {
    ...base,
    ...variants[variant],
    ...(hover && !disabled ? hoverStyles[variant] : {}),
    ...style
  };
  const Tag = as === 'a' || href ? 'a' : 'button';
  const extra = Tag === 'a' ? {
    href
  } : {
    disabled
  };
  return /*#__PURE__*/React.createElement(Tag, _extends({}, extra, rest, {
    style: composed,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false)
  }), children, arrow && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      fontFamily: 'var(--font-sans)'
    }
  }, "\u2192"));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Button.jsx", error: String((e && e.message) || e) }); }

// components/forms/TextLink.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * TextLink — NAV / Judge
 * Editorial inline / standalone link. Vermilion, subtle underline that
 * fills on hover. Optional trailing arrow for standalone CTAs.
 */
function TextLink({
  href = '#',
  arrow = false,
  muted = false,
  children,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const color = muted ? 'var(--ink-soft)' : 'var(--link)';
  const hoverColor = muted ? 'var(--ink)' : 'var(--link-hover)';
  return /*#__PURE__*/React.createElement("a", _extends({
    href: href
  }, rest, {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      color: hover ? hoverColor : color,
      textDecorationLine: 'underline',
      textDecorationThickness: '1px',
      textUnderlineOffset: '0.18em',
      textDecorationColor: hover ? 'currentColor' : 'color-mix(in srgb, currentColor 35%, transparent)',
      transition: 'color var(--dur-fast) var(--ease-out), text-decoration-color var(--dur-fast) var(--ease-out)',
      display: arrow ? 'inline-flex' : 'inline',
      alignItems: 'center',
      gap: '0.4em',
      ...style
    }
  }), children, arrow && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      fontFamily: 'var(--font-sans)',
      textDecoration: 'none'
    }
  }, "\u2192"));
}
Object.assign(__ds_scope, { TextLink });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/TextLink.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Footer.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Footer — NAV / Judge
 * The site footer: wordmark, an optional row of page links, and a serif
 * tagline. Shared across every page so the foot of the site is consistent.
 */
function Footer({
  wordmark = 'Judge',
  tagline = 'Delivering Joy since the turn of the Century',
  links = [],
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("footer", _extends({}, rest, {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: '18px 40px',
      padding: '32px clamp(1.5rem, 6vw, 6rem)',
      borderTop: '1px solid var(--line)',
      ...style
    }
  }), /*#__PURE__*/React.createElement("a", {
    href: "index.html",
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: '18px',
      color: 'var(--ink)',
      textDecoration: 'none',
      letterSpacing: '-0.01em'
    }
  }, wordmark, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, ".")), links.length > 0 && /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: '10px 24px'
    }
  }, links.map(l => /*#__PURE__*/React.createElement("a", {
    key: l.href,
    href: l.href,
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--text-label)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      color: 'var(--ink-soft)',
      textDecoration: 'none'
    }
  }, l.label))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--text-meta)',
      color: 'var(--ink-faint)',
      letterSpacing: 'var(--tracking-wide)',
      textTransform: 'uppercase'
    }
  }, tagline));
}
Object.assign(__ds_scope, { Footer });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Footer.jsx", error: String((e && e.message) || e) }); }

// components/navigation/NavItem.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NavItem — NAV / Judge
 * One of the oblique nav labels (Work Life, The Exciting Stuff…). Mono
 * uppercase with an optional faint index. Vermilion when active; a thin
 * accent underline slides in on hover.
 */
function NavItem({
  index,
  href = '#',
  active = false,
  children,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const on = active || hover;
  return /*#__PURE__*/React.createElement("a", _extends({
    href: href
  }, rest, {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'inline-flex',
      flexDirection: 'column',
      gap: '5px',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-label)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      fontWeight: 'var(--weight-medium)',
      color: active ? 'var(--vermilion)' : 'var(--ink)',
      textDecoration: 'none',
      transition: 'color var(--dur-fast) var(--ease-out)',
      ...style
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'baseline',
      gap: '7px'
    }
  }, index != null && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)',
      fontSize: 'var(--text-meta)',
      fontWeight: 'var(--weight-regular)'
    }
  }, index), /*#__PURE__*/React.createElement("span", {
    style: {
      color: hover && !active ? 'var(--vermilion)' : undefined
    }
  }, children)), /*#__PURE__*/React.createElement("span", {
    style: {
      height: 1,
      background: 'var(--vermilion)',
      width: on ? '100%' : '0%',
      transition: 'width var(--dur-base) var(--ease-out)'
    }
  }));
}
Object.assign(__ds_scope, { NavItem });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/NavItem.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Pager.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Pager — NAV / Judge
 * Prev / next page navigation for the foot of a standalone page. Two ends of
 * a hairline-topped row: a faint uppercase serif direction label and the
 * destination page title in Anton. Either end may be omitted.
 */
function PagerEnd({
  dir,
  item,
  align
}) {
  const [hover, setHover] = React.useState(false);
  const isNext = dir === 'next';
  return /*#__PURE__*/React.createElement("a", {
    href: item.href,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'inline-flex',
      flexDirection: 'column',
      gap: '8px',
      textDecoration: 'none',
      textAlign: align,
      alignItems: isNext ? 'flex-end' : 'flex-start'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 'var(--text-meta)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-label)',
      color: 'var(--ink-faint)'
    }
  }, isNext ? 'Next' : 'Previous'), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'baseline',
      gap: '10px',
      fontFamily: 'var(--font-display)',
      textTransform: 'uppercase',
      fontSize: 'clamp(1.375rem, 3vw, 2rem)',
      lineHeight: 1.0,
      letterSpacing: '-0.005em',
      color: hover ? 'var(--vermilion)' : 'var(--ink)',
      transition: 'color var(--dur-fast) var(--ease-out)'
    }
  }, !isNext && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, "\u2190"), /*#__PURE__*/React.createElement("span", null, item.label), isNext && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, "\u2192")));
}
function Pager({
  prev,
  next,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("nav", _extends({}, rest, {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      gap: '24px',
      padding: 'clamp(2rem, 5vw, 3rem) clamp(1.5rem, 6vw, 6rem)',
      borderTop: '1px solid var(--line)',
      ...style
    }
  }), /*#__PURE__*/React.createElement("div", null, prev && /*#__PURE__*/React.createElement(PagerEnd, {
    dir: "prev",
    item: prev,
    align: "left"
  })), /*#__PURE__*/React.createElement("div", null, next && /*#__PURE__*/React.createElement(PagerEnd, {
    dir: "next",
    item: next,
    align: "right"
  })));
}
Object.assign(__ds_scope, { Pager });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Pager.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/Connect.jsx
try { (() => {
/* global React, Section */
// Connect: one ask, made obvious. Here's how, here's why, here's the address.
function Connect({
  hideLabel
}) {
  const {
    Button
  } = window.NAVJudgeDesignSystem_020eb9;
  return /*#__PURE__*/React.createElement(Section, {
    id: "connect",
    index: "04",
    label: "Connect",
    hideLabel: hideLabel,
    style: {
      background: 'var(--ink)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: '44rem'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 'clamp(1.125rem, 2.4vw, 1.5rem)',
      lineHeight: 1.5,
      color: 'color-mix(in srgb, var(--paper) 82%, transparent)',
      margin: 0,
      maxWidth: '36rem'
    }
  }, "I'm responsive on email, better on a call, and genuinely bad at LinkedIn DMs."), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 'clamp(1.0625rem, 2vw, 1.25rem)',
      lineHeight: 1.6,
      color: 'color-mix(in srgb, var(--paper) 66%, transparent)',
      margin: '20px 0 0',
      maxWidth: '38rem'
    }
  }, "If you're working on something in the Adobe Experience Cloud space and need a senior architect \u2014 or just need someone to talk through a hairy integration \u2014 I'm interested. Find 30 minutes."), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'clamp(2.5rem, 6vw, 3.5rem)',
      display: 'flex',
      alignItems: 'center',
      gap: 28,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    as: "a",
    href: "mailto:judge@judgedice.com",
    variant: "primary",
    size: "lg",
    arrow: true
  }, "judge@judgedice.com"))));
}
window.Connect = Connect;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/Connect.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/ExcitingStuff.jsx
try { (() => {
/* global React, Section */
// The Exciting Stuff: what he actually does, in plain English. Dry, direct.
// No icons. No three-word headlines with three bullets. Prose, framed.
function ExcitingStuff({
  hideLabel
}) {
  const {
    Card
  } = window.NAVJudgeDesignSystem_020eb9;
  const items = [{
    t: 'Marketing Technology Architecture',
    d: "Designing end-to-end digital marketing systems that hold together under real conditions — across strategy, platform selection, integration design, and build. The kind of architecture that doesn't collapse when a stakeholder changes their mind in month three."
  }, {
    t: 'Adobe Experience Cloud',
    d: "AEM, Adobe Journey Optimizer, Workfront, Target, AEP. I've shipped all of it, across industries and client contexts. I know which parts to use, which to skip, and which will require a ticket that becomes a different ticket. I have stories."
  }, {
    t: 'Marketing Operations & Automation',
    d: "Building the workflows and integrations that let marketing teams actually use the platforms they've paid for. Approval flows that don't require a PhD. Automations that run without babysitting. The operational layer that makes the strategy real."
  }, {
    t: 'Workshop Facilitation',
    d: "I've run a lot of them. Discovery, architecture, stakeholder alignment. I know how to get a room full of people with competing priorities to walk out with decisions made and next steps owned. This is harder than it sounds."
  }, {
    t: 'Strategy & Solutions Architecture',
    d: 'The part before the build. What are we trying to do? What does the ecosystem need to look like? What do we build first and what do we defer? This is where 25 years of pattern-matching earns its keep.'
  }, {
    t: 'Teaching & Consulting',
    d: "Search Engine Marketing at the Chicago Portfolio School. Digital consulting for educational programs. If you're building a curriculum or a team, I can help."
  }];
  return /*#__PURE__*/React.createElement(Section, {
    id: "exciting",
    index: "03",
    label: "The Exciting Stuff",
    hideLabel: hideLabel
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
      gap: 'clamp(1rem, 2vw, 1.5rem)'
    }
  }, items.map((it, i) => /*#__PURE__*/React.createElement(Card, {
    key: it.t,
    framed: true
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 12,
      color: 'var(--vermilion)'
    }
  }, String(i + 1).padStart(2, '0')), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 'clamp(1.375rem, 2.4vw, 1.625rem)',
      fontWeight: 400,
      letterSpacing: '-0.01em',
      lineHeight: 1.15,
      margin: 0,
      color: 'var(--ink)'
    }
  }, it.t)), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: '1.0625rem',
      lineHeight: 1.6,
      color: 'var(--ink-soft)',
      margin: '14px 0 0'
    }
  }, it.d)))));
}
window.ExcitingStuff = ExcitingStuff;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/ExcitingStuff.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/Header.jsx
try { (() => {
/* global React */
// Sticky top bar: wordmark + oblique nav. Now links between separate pages;
// `current` marks the active one.
const NAV_PAGES = [{
  id: 'work',
  index: '01',
  label: 'Work Life',
  href: 'work.html'
}, {
  id: 'home',
  index: '02',
  label: 'Home Life',
  href: 'home.html'
}, {
  id: 'exciting',
  index: '03',
  label: 'The Exciting Stuff',
  href: 'exciting.html'
}, {
  id: 'connect',
  index: '04',
  label: 'Connect',
  href: 'connect.html'
}];
function Header({
  current
}) {
  const {
    NavItem
  } = window.NAVJudgeDesignSystem_020eb9;
  return /*#__PURE__*/React.createElement("header", {
    style: {
      position: 'sticky',
      top: 0,
      zIndex: 20,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '20px clamp(1.5rem, 6vw, 6rem)',
      background: 'color-mix(in srgb, var(--paper) 88%, transparent)',
      backdropFilter: 'blur(6px)',
      borderBottom: '1px solid var(--line)'
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "index.html",
    style: {
      fontFamily: 'var(--font-serif)',
      fontSize: 26,
      color: 'var(--ink)',
      textDecoration: 'none',
      letterSpacing: '-0.01em'
    }
  }, "Judge", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, ".")), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: 'clamp(18px, 3vw, 40px)',
      flexWrap: 'wrap'
    }
  }, NAV_PAGES.map(s => /*#__PURE__*/React.createElement(NavItem, {
    key: s.id,
    index: s.index,
    href: s.href,
    active: current === s.id
  }, s.label))));
}
window.Header = Header;
window.NAV_PAGES = NAV_PAGES;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/Header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/Hero.jsx
try { (() => {
/* global React */
// Hero: the tagline moment. Statement, not description. One staggered reveal.
function Hero() {
  return /*#__PURE__*/React.createElement("section", {
    id: "top",
    style: {
      minHeight: 'calc(100vh - 66px)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      padding: '0 clamp(1.5rem, 6vw, 6rem)',
      maxWidth: '78rem'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "reveal",
    style: {
      animationDelay: '80ms'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 13,
      textTransform: 'uppercase',
      letterSpacing: '0.14em',
      color: 'var(--vermilion)',
      fontWeight: 500
    }
  }, "Judge \u2014 Digital Architect")), /*#__PURE__*/React.createElement("h1", {
    className: "reveal",
    style: {
      animationDelay: '180ms',
      fontFamily: 'var(--font-display)',
      fontWeight: 400,
      textTransform: 'uppercase',
      fontSize: 'clamp(3rem, 10vw, 7.5rem)',
      lineHeight: 1.02,
      letterSpacing: '-0.005em',
      color: 'var(--ink)',
      margin: '28px 0 0',
      maxWidth: '15ch'
    }
  }, "Delivering ", /*#__PURE__*/React.createElement("em", {
    style: {
      fontStyle: 'normal',
      color: 'var(--vermilion)'
    }
  }, "Joy"), " since the turn of the Century."), /*#__PURE__*/React.createElement("p", {
    className: "reveal",
    style: {
      animationDelay: '320ms',
      fontFamily: 'var(--font-sans)',
      fontSize: 13,
      color: 'var(--ink-faint)',
      letterSpacing: '0.04em',
      marginTop: 40,
      textTransform: 'uppercase'
    }
  }, "Work Life \xB7 Home Life \xB7 The Exciting Stuff \xB7 Connect"));
}
window.Hero = Hero;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/Hero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/HomeLife.jsx
try { (() => {
/* global React, Section */
// Home Life: the exhale. Short sentences. Sounds like him at dinner.
function HomeLife({
  hideLabel
}) {
  const {
    Callout
  } = window.NAVJudgeDesignSystem_020eb9;
  const p = {
    fontFamily: 'var(--font-serif)',
    fontSize: 'clamp(1.125rem, 2.2vw, 1.3125rem)',
    lineHeight: 1.6,
    color: 'var(--ink-soft)',
    margin: '0 0 1.1em',
    maxWidth: '40rem'
  };
  return /*#__PURE__*/React.createElement(Section, {
    id: "home",
    index: "02",
    label: "Home Life",
    hideLabel: hideLabel,
    style: {
      background: 'var(--paper-raised)'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      ...p,
      fontSize: 'clamp(1.375rem, 3vw, 1.75rem)',
      lineHeight: 1.42,
      color: 'var(--ink)',
      maxWidth: '26ch'
    }
  }, "When I'm not untangling enterprise tech stacks, I'm probably driving someone to band practice, arguing about something mundane, or still thinking about work."), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 'clamp(1.5rem, 4vw, 2.5rem)'
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: p
  }, "I have a family that puts up with me. I've been in New England long enough to have opinions about winters."), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: 'clamp(2rem, 5vw, 3rem) 0',
      maxWidth: '40rem'
    }
  }, /*#__PURE__*/React.createElement(Callout, null, "I believe strongly in the power of a good lunch \u2014 there is no force stronger than the gravity of free lunch, and I will not be argued out of this.")), /*#__PURE__*/React.createElement("p", {
    style: p
  }, "I got into this work because I liked building things that didn't exist yet. That's still true. The tools have changed \u2014 ", /*#__PURE__*/React.createElement("em", {
    style: {
      fontStyle: 'italic',
      color: 'var(--ink)'
    }
  }, "Flash is dead, long live the API"), " \u2014 but the feeling of shipping something that works is the same."));
}
window.HomeLife = HomeLife;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/HomeLife.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/Page.jsx
try { (() => {
/* global React, Header, NAV_PAGES */
// Per-page shell: sticky Header + <main> + auto prev/next Pager + shared Footer.
// `current` is the page id (null on the hero landing). Pager order follows
// NAV_PAGES; the landing (index.html) is treated as the step before Work Life.
function Page({
  current,
  children
}) {
  const {
    Pager,
    Footer
  } = window.NAVJudgeDesignSystem_020eb9;
  const seq = [{
    id: 'top',
    label: 'Home',
    href: 'index.html'
  }, ...NAV_PAGES];
  const i = seq.findIndex(p => p.id === (current || 'top'));
  const prevItem = i > 0 ? seq[i - 1] : null;
  const nextItem = i >= 0 && i < seq.length - 1 ? seq[i + 1] : null;
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    current: current
  }), /*#__PURE__*/React.createElement("main", null, children), (prevItem || nextItem) && /*#__PURE__*/React.createElement(Pager, {
    prev: prevItem && {
      label: prevItem.label,
      href: prevItem.href
    },
    next: nextItem && {
      label: nextItem.label,
      href: nextItem.href
    }
  }), /*#__PURE__*/React.createElement(Footer, {
    links: NAV_PAGES.map(p => ({
      label: p.label,
      href: p.href
    }))
  }));
}
window.Page = Page;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/Page.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/Section.jsx
try { (() => {
/* global React */
// Shared section shell: mono numbered label opener + generous vertical rhythm.
function Section({
  id,
  index,
  label,
  children,
  hideLabel = false,
  style = {}
}) {
  const {
    SectionLabel
  } = window.NAVJudgeDesignSystem_020eb9;
  return /*#__PURE__*/React.createElement("section", {
    id: id,
    style: {
      padding: 'clamp(4rem, 10vw, 8rem) clamp(1.5rem, 6vw, 6rem)',
      borderTop: '1px solid var(--line)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: '72rem',
      margin: '0 auto'
    }
  }, !hideLabel && /*#__PURE__*/React.createElement(SectionLabel, {
    index: index,
    rule: true
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: hideLabel ? 0 : 'clamp(2rem, 5vw, 4rem)'
    }
  }, children)));
}
window.Section = Section;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/Section.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nav-site/WorkLife.jsx
try { (() => {
/* global React, Section */
// Work Life: earns credibility without performing it. Arc + tools as proof.
function WorkLife({
  hideLabel
}) {
  const {
    Tag,
    Rule,
    TextLink
  } = window.NAVJudgeDesignSystem_020eb9;
  const tools = ['Adobe Experience Manager', 'Adobe Journey Optimizer', 'Adobe Workfront', 'Adobe Experience Platform', 'Adobe Target', 'Salesforce', 'Smartsheet', 'APIs & the integrations nobody else wants to wire up'];
  const p = {
    fontFamily: 'var(--font-serif)',
    fontSize: 'clamp(1.0625rem, 2vw, 1.1875rem)',
    lineHeight: 1.62,
    color: 'var(--ink-soft)',
    margin: '0 0 1.1em',
    maxWidth: '38rem'
  };
  return /*#__PURE__*/React.createElement(Section, {
    id: "work",
    index: "01",
    label: "Work Life",
    hideLabel: hideLabel
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'minmax(0, 1fr)',
      gap: 0
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      ...p,
      fontSize: 'clamp(1.375rem, 3vw, 1.75rem)',
      lineHeight: 1.4,
      color: 'var(--ink)',
      maxWidth: 'none'
    }
  }, "I've been building things on the internet since before it was cool. That sounds like a brag. ", /*#__PURE__*/React.createElement("em", {
    style: {
      fontStyle: 'italic',
      color: 'var(--vermilion-deep)'
    }
  }, "It's mostly just a fact.")), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 'clamp(1.5rem, 4vw, 2.5rem)'
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: p
  }, "What started as Flash development at McKinsey became a 25-year career in digital architecture and marketing technology. I currently work at WillowTree, where I design and build enterprise systems for brands in financial services, real estate, hospitality, and media \u2014 mostly inside the Adobe Experience Cloud."), /*#__PURE__*/React.createElement("p", {
    style: p
  }, "My specialty is the space where strategy meets implementation. Where a roadmap stops being a slide and starts being a thing that works in production. I've done the architecture, run the workshops, led the demos, and when necessary jumped in to fix the integration the night before launch."), /*#__PURE__*/React.createElement("p", {
    style: p
  }, "I also teach Search Engine Marketing at the Chicago Portfolio School. I believe in passing things forward.")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'clamp(2.5rem, 6vw, 4.5rem)',
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
      gap: 'clamp(2rem, 5vw, 4rem)'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Rule, {
    label: "Career arc"
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 13,
      lineHeight: 1.9,
      color: 'var(--ink-soft)',
      marginTop: 20,
      letterSpacing: '0.01em'
    }
  }, "Flash developer at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "McKinsey & Company"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, " \u2192 "), "founded ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "The Flash Ministry"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, " \u2192 "), "partner at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "Pixelwelders"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, " \u2192 "), "Development Director at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "Vertical Inc."), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, " \u2192 "), "Lead Solutions Architect at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "Hanson Dodge"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, " \u2192 "), /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "Velir"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--vermilion)'
    }
  }, " \u2192 "), "Principal Solutions Architect at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "Maark"), ", acquired by ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: 'var(--ink)',
      fontWeight: 500
    }
  }, "WillowTree"), ".")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Rule, {
    label: "What I work with"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 8,
      marginTop: 20
    }
  }, tools.map((t, i) => /*#__PURE__*/React.createElement(Tag, {
    key: t,
    emphasis: i < 4
  }, t))))));
}
window.WorkLife = WorkLife;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nav-site/WorkLife.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Callout = __ds_scope.Callout;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.PageHeader = __ds_scope.PageHeader;

__ds_ns.Rule = __ds_scope.Rule;

__ds_ns.SectionLabel = __ds_scope.SectionLabel;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.TextLink = __ds_scope.TextLink;

__ds_ns.Footer = __ds_scope.Footer;

__ds_ns.NavItem = __ds_scope.NavItem;

__ds_ns.Pager = __ds_scope.Pager;

})();
