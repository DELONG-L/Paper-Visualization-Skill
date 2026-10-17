(() => {
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  const panels = [...document.querySelectorAll('[role="tabpanel"]')];
  function select(index, focus = false) {
    tabs.forEach((tab, i) => { tab.setAttribute('aria-selected', String(i === index)); tab.tabIndex = i === index ? 0 : -1; });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', event => {
      let target;
      if (['ArrowDown', 'ArrowRight'].includes(event.key)) target = (index + 1) % tabs.length;
      if (['ArrowUp', 'ArrowLeft'].includes(event.key)) target = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = tabs.length - 1;
      if (target !== undefined) { event.preventDefault(); select(target, true); }
    });
  });
  const dialog = document.getElementById('sources');
  document.querySelectorAll('[data-sources]').forEach(button => button.addEventListener('click', () => dialog.showModal()));
  document.getElementById('close-sources').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target !== dialog) return; const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); });
  const copy = document.getElementById('copy-citation');
  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(document.getElementById('bibtex').textContent);
      document.getElementById('copy-status').textContent = copy.dataset.copied;
    } catch {
      document.getElementById('copy-status').textContent = copy.dataset.error;
    }
  });
  const nav = [...document.querySelectorAll('.nav-links a')];
  const sections = nav.map(link => document.querySelector(link.hash)).filter(Boolean);
  function updatePosition() {
    const full = document.documentElement.scrollHeight - innerHeight;
    document.querySelector('.reading-progress').style.width = `${full > 0 ? Math.min(100, scrollY / full * 100) : 0}%`;
    let active = sections[0];
    sections.forEach(section => { if (section.getBoundingClientRect().top <= Math.max(160, innerHeight * 0.4)) active = section; });
    if (full > 0 && scrollY >= full - 8) active = sections[sections.length - 1];
    nav.forEach(link => { if (active && link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    document.querySelectorAll('[data-language]').forEach(link => { link.hash = location.hash; });
  }
  window.addEventListener('scroll', updatePosition, { passive: true });
  window.addEventListener('resize', updatePosition);
  window.addEventListener('hashchange', updatePosition);
  select(0); updatePosition();
})();
