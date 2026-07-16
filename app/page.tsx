import Image from "next/image";
import Link from "next/link";
import { Catalog } from "./components/Catalog";
import { CopyCommand } from "./components/CopyCommand";
import { plugins, totals } from "./catalog.generated";

const repositoryUrl =
  "https://github.com/Israelmusondaayliffe/codex-plugins";

export default function Home() {
  const resourceTotal = totals.assets + totals.references + totals.scripts;
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: "Israel's Codex Plugins",
    numberOfItems: plugins.length,
    itemListElement: plugins.map((plugin, index) => ({
      "@type": "ListItem",
      position: index + 1,
      url: repositoryUrl + "/tree/main/plugins/" + plugin.slug,
      name: plugin.name,
    })),
  };

  return (
    <>
      <header className="site-header shell">
        <Link className="wordmark" href="/" aria-label="Israel's Codex Plugins">
          <span>IA</span>
          <span>/</span>
          <span>CODEX</span>
        </Link>
        <nav aria-label="Primary navigation">
          <a href="#plugins">Plugins</a>
          <a href="#install">Install</a>
          <a href={repositoryUrl}>GitHub</a>
        </nav>
      </header>

      <main>
        <section className="hero shell" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">Israel&apos;s Codex Plugins</p>
            <h1 id="hero-title">
              A working system,
              <br />
              packaged.
            </h1>
            <p className="hero-lede">
              {totals.plugins} field-tested plugins for research, strategy,
              creation, operations, and delivery in Codex.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#plugins">
                Browse plugins
              </a>
              <a className="button button-secondary" href={repositoryUrl}>
                View source
              </a>
            </div>
          </div>
          <figure className="hero-art">
            <Image
              alt="Abstract modular forms arranged like a creative system"
              fill
              priority
              sizes="(max-width: 980px) 100vw, 58vw"
              src="/plugin-constellation.png"
              unoptimized
            />
          </figure>
        </section>

        <section className="proof-strip shell" aria-label="Marketplace totals">
          <div>
            <strong>{totals.plugins}</strong>
            <span>Plugins</span>
          </div>
          <div>
            <strong>{totals.skills}</strong>
            <span>Skills</span>
          </div>
          <div>
            <strong>{resourceTotal.toLocaleString("en-US")}</strong>
            <span>Support files</span>
          </div>
          <div>
            <strong>Public</strong>
            <span>Git marketplace</span>
          </div>
        </section>

        <section className="catalog-section shell" id="plugins">
          <div className="section-heading">
            <p className="eyebrow">The collection</p>
            <h2>Choose the capability you need.</h2>
            <p>
              Search the complete catalog, inspect every bundled skill, and
              copy a plugin-specific install command.
            </p>
          </div>
          <Catalog />
        </section>

        <section className="install-section" id="install">
          <div className="shell install-grid">
            <div className="section-heading install-heading">
              <p className="eyebrow">Installation</p>
              <h2>Two commands. Then start a new task.</h2>
              <p>
                Add the public marketplace once. Install only the plugins you
                want. A fresh task makes the new skills visible to Codex.
              </p>
            </div>
            <div className="install-steps">
              <article className="install-card">
                <span className="step-number">01</span>
                <h3>Add the marketplace</h3>
                <CopyCommand command="codex plugin marketplace add Israelmusondaayliffe/codex-plugins --ref main" />
              </article>
              <article className="install-card install-card-shifted">
                <span className="step-number">02</span>
                <h3>Install a plugin</h3>
                <CopyCommand command="codex plugin add knowledge-work-superpowers@israel-codex-plugins" />
              </article>
              <article className="install-card">
                <span className="step-number">03</span>
                <h3>Start a new Codex task</h3>
                <p>
                  Fresh tasks load the newly installed plugin inventory. Your
                  existing task may keep its earlier capability list.
                </p>
              </article>
            </div>
          </div>
        </section>

        <section className="truth-section shell">
          <div className="truth-mark" aria-hidden="true">
            <span>{totals.skills}</span>
            <small>skills</small>
          </div>
          <div className="truth-copy">
            <p className="eyebrow">What is inside</p>
            <h2>Skills first. Claims kept exact.</h2>
            <p>
              This release contains Codex plugins and their skills, scripts,
              references, assets, and agent definitions. It does not currently
              bundle MCP servers or app connectors.
            </p>
            <Link className="text-link" href="/plugins/capability-operator">
              Inspect a full plugin record
            </Link>
          </div>
        </section>
      </main>

      <footer>
        <div className="shell footer-grid">
          <div>
            <p className="footer-name">Israel&apos;s Codex Plugins</p>
            <p>Public packages for repeatable, verifiable work.</p>
          </div>
          <div className="footer-links">
            <a href={repositoryUrl}>Source</a>
            <a href={repositoryUrl + "/blob/main/SECURITY.md"}>Security</a>
            <a href={repositoryUrl + "/blob/main/LEGAL.md"}>Legal</a>
          </div>
        </div>
      </footer>

      <script
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        type="application/ld+json"
      />
    </>
  );
}
