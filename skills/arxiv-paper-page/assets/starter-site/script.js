async function loadConfig() {
  const response = await fetch("paper-page.config.json");
  if (!response.ok) {
    throw new Error(`Failed to load paper-page.config.json: ${response.status}`);
  }
  return response.json();
}

function create(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function appendParagraphs(parent, paragraphs) {
  if (!paragraphs || !paragraphs.length) return;
  const prose = create("div", "prose");
  for (const paragraph of paragraphs) {
    prose.appendChild(create("p", "", paragraph));
  }
  parent.appendChild(prose);
}

function appendHighlights(parent, highlights) {
  if (!highlights || !highlights.length) return;
  const list = create("div", "pill-list");
  for (const item of highlights) {
    list.appendChild(create("span", "", item));
  }
  parent.appendChild(list);
}

function buildCard(card) {
  const classes = ["generic-card"];
  if (card.variant === "accent") classes.push("accent");
  const node = create("article", classes.join(" "));

  if (card.label) node.appendChild(create("span", "card-label", card.label));
  if (card.metric) node.appendChild(create("span", "card-metric", card.metric));
  if (card.title) node.appendChild(create("h3", "", card.title));
  if (card.body) node.appendChild(create("p", "", card.body));

  if (card.items && card.items.length) {
    const list = create("ul", "");
    for (const item of card.items) {
      list.appendChild(create("li", "", item));
    }
    node.appendChild(list);
  }

  return node;
}

function appendCards(parent, cards) {
  if (!cards || !cards.length) return;
  const grid = create("div", `card-grid count-${Math.min(cards.length, 4)}`);
  for (const card of cards) {
    grid.appendChild(buildCard(card));
  }
  parent.appendChild(grid);
}

function buildFigure(figure, className = "media-card") {
  if (!figure || !figure.src) return null;
  const node = create("figure", className);
  const img = create("img", "");
  img.src = figure.src;
  img.alt = figure.alt || "";
  node.appendChild(img);
  if (figure.caption) {
    node.appendChild(create("figcaption", "", figure.caption));
  }
  return node;
}

function renderNav(config) {
  const nav = document.getElementById("nav-links");
  nav.innerHTML = "";

  const items = [{ id: "summary", label: "Summary" }];
  for (const section of config.sections || []) {
    items.push({ id: section.id, label: section.kicker || section.title });
  }
  items.push({ id: "citation", label: "Citation" });

  for (const item of items) {
    const link = create("a", "", item.label);
    link.href = `#${item.id}`;
    nav.appendChild(link);
  }
}

function renderHero(config) {
  document.getElementById("brand-title").textContent = config.site.short_title || config.site.title;

  const root = document.getElementById("hero-root");
  const shell = create("div", "shell hero-grid");

  const copy = create("div", "hero-copy");
  copy.appendChild(create("p", "eyebrow", config.site.kicker || ""));
  copy.appendChild(create("h1", "", config.site.title || ""));
  copy.appendChild(create("p", "deck", config.site.subtitle || ""));

  const authorBlock = create("div", "author-block");
  authorBlock.appendChild(create("p", "authors", (config.authors || []).join(", ")));
  authorBlock.appendChild(create("p", "affiliations", config.affiliations || ""));
  copy.appendChild(authorBlock);

  const buttonRow = create("div", "button-row");
  for (const link of config.site.links || []) {
    const button = create("a", `button ${link.primary ? "primary" : "secondary"}`, link.label);
    button.href = link.href;
    if (/^https?:\/\//.test(link.href) || link.href.endsWith(".pdf")) {
      button.target = "_blank";
      button.rel = "noopener";
    }
    buttonRow.appendChild(button);
  }
  copy.appendChild(buttonRow);

  if (config.hero_facts && config.hero_facts.length) {
    const facts = create("div", "hero-facts");
    for (const fact of config.hero_facts) {
      const article = create("article", "");
      article.appendChild(create("span", "fact-label", fact.label));
      article.appendChild(create("strong", "", fact.value));
      facts.appendChild(article);
    }
    copy.appendChild(facts);
  }

  shell.appendChild(copy);

  const figure = buildFigure(config.hero_figure, "hero-figure");
  if (figure) shell.appendChild(figure);

  root.innerHTML = "";
  root.appendChild(shell);
}

function renderSummary(config) {
  const root = document.getElementById("summary-root");
  const shell = create("div", "shell");
  const heading = create("div", "section-heading");
  heading.appendChild(create("p", "kicker", "Summary"));
  heading.appendChild(create("h2", "", config.summary?.title || "What this paper contributes"));
  shell.appendChild(heading);

  appendCards(shell, config.summary?.cards || []);
  root.innerHTML = "";
  root.appendChild(shell);
}

function renderSection(section) {
  const sectionNode = create("section", `section ${section.theme === "soft" ? "band-soft" : ""}`);
  sectionNode.id = section.id;
  const shell = create("div", "shell");

  const heading = create("div", "section-heading");
  heading.appendChild(create("p", "kicker", section.kicker || ""));
  heading.appendChild(create("h2", "", section.title || ""));
  shell.appendChild(heading);

  const hasFigure = section.figure && section.figure.src;
  const hasCards = section.cards && section.cards.length;

  if (hasFigure) {
    const split = create("div", "split-layout");
    const textStack = create("div", "text-stack");
    appendParagraphs(textStack, section.paragraphs || []);
    appendHighlights(textStack, section.highlights || []);
    appendCards(textStack, section.cards || []);

    const figure = buildFigure(section.figure, "media-card");
    if (section.figure_first) {
      split.appendChild(figure);
      split.appendChild(textStack);
    } else {
      split.appendChild(textStack);
      split.appendChild(figure);
    }
    shell.appendChild(split);
  } else {
    appendParagraphs(shell, section.paragraphs || []);
    appendHighlights(shell, section.highlights || []);
    if (hasCards) {
      const wrap = create("div", "lower-split");
      appendCards(wrap, section.cards);
      shell.appendChild(wrap);
    }
  }

  sectionNode.appendChild(shell);
  return sectionNode;
}

function renderSections(config) {
  const root = document.getElementById("sections-root");
  root.innerHTML = "";
  for (const section of config.sections || []) {
    root.appendChild(renderSection(section));
  }
}

function renderCitation(config) {
  const root = document.getElementById("citation");
  const shell = create("div", "shell citation-shell");
  const heading = create("div", "section-heading");
  heading.appendChild(create("p", "kicker", "Citation"));
  heading.appendChild(create("h2", "", config.citation?.title || "Cite the paper directly"));
  shell.appendChild(heading);

  const toolbar = create("div", "citation-toolbar");
  toolbar.appendChild(create("p", "", config.citation?.note || ""));
  const button = create("button", "button secondary");
  button.id = "copy-citation";
  button.type = "button";
  button.textContent = "Copy BibTeX";
  toolbar.appendChild(button);
  shell.appendChild(toolbar);

  const pre = create("pre", "");
  pre.id = "citation-block";
  pre.textContent = config.citation?.bibtex || "";
  shell.appendChild(pre);

  root.innerHTML = "";
  root.appendChild(shell);
}

function renderFooter(config) {
  const root = document.getElementById("footer-root");
  root.innerHTML = "";
  root.appendChild(create("p", "", config.footer?.left || ""));
  root.appendChild(create("p", "", config.footer?.right || ""));
}

function setupCopyCitation() {
  const copyButton = document.getElementById("copy-citation");
  const citationBlock = document.getElementById("citation-block");
  if (!copyButton || !citationBlock) return;

  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(citationBlock.textContent.trim());
      const previous = copyButton.textContent;
      copyButton.textContent = "Copied";
      setTimeout(() => {
        copyButton.textContent = previous;
      }, 1400);
    } catch {
      copyButton.textContent = "Copy failed";
      setTimeout(() => {
        copyButton.textContent = "Copy BibTeX";
      }, 1400);
    }
  });
}

function setupNavObserver() {
  const navLinks = [...document.querySelectorAll(".nav-scroll a")];
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const id = `#${entry.target.id}`;
        for (const link of navLinks) {
          link.classList.toggle("active", link.getAttribute("href") === id);
        }
      }
    },
    {
      rootMargin: "-35% 0px -55% 0px",
      threshold: 0.01,
    },
  );

  for (const section of sections) {
    observer.observe(section);
  }
}

async function main() {
  try {
    const config = await loadConfig();
    document.title = config.site?.title || "Paper project page";
    const description = config.site?.subtitle || "GitHub Pages paper project page";
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) metaDescription.setAttribute("content", description);

    renderNav(config);
    renderHero(config);
    renderSummary(config);
    renderSections(config);
    renderCitation(config);
    renderFooter(config);
    setupCopyCitation();
    setupNavObserver();
  } catch (error) {
    document.body.innerHTML = `<pre style="padding:24px;">${String(error)}</pre>`;
  }
}

main();
