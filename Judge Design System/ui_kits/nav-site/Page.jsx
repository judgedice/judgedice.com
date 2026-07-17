/* global React, Header, NAV_PAGES */
// Per-page shell: sticky Header + <main> + auto prev/next Pager + shared Footer.
// `current` is the page id (null on the hero landing). Pager order follows
// NAV_PAGES; the landing (index.html) is treated as the step before Work Life.
function Page({ current, children }) {
  const { Pager, Footer } = window.NAVJudgeDesignSystem_020eb9;

  const seq = [{ id: 'top', label: 'Home', href: 'index.html' }, ...NAV_PAGES];
  const i = seq.findIndex((p) => p.id === (current || 'top'));
  const prevItem = i > 0 ? seq[i - 1] : null;
  const nextItem = i >= 0 && i < seq.length - 1 ? seq[i + 1] : null;

  return (
    <React.Fragment>
      <Header current={current} />
      <main>{children}</main>
      {(prevItem || nextItem) && (
        <Pager
          prev={prevItem && { label: prevItem.label, href: prevItem.href }}
          next={nextItem && { label: nextItem.label, href: nextItem.href }}
        />
      )}
      <Footer links={NAV_PAGES.map((p) => ({ label: p.label, href: p.href }))} />
    </React.Fragment>
  );
}
window.Page = Page;
