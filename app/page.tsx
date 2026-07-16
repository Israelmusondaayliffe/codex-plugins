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
          <span className="wordmark-mark">IA</span>
          <span>CODEX PLUGINS</span>
        </Link>
        <nav aria-label="Primary navigation">
          <a href="#plugins">Plugins</a>
          <a href="#install">Install</a>
          <a href={repositoryUrl}>GitHub</a>
        </nav>
      </header>

      <main>
        <section className="hero shell" aria-labelledby="hero-title">
          <figure className="hero-art" aria-hidden="true">
            <Image
              alt=""
              fill
              priority
              sizes="(max-width: 800px) 100vw, 62vw"
              src="/plugin-constellation.png"
              unoptimized
            />
          </figure>
          <div className="hero-copy">
            <p className="kicker">A public Codex marketplace</p>
            <h1 id="hero-title">
              A working system,
              <br />
              packaged.
            </h1>
            <p className="hero-lede">
              {totals.plugins} field-tested plugins for repeatable research,
              creation, strategy, and operations.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#plugins">
                Browse the registry
              </a>
              <a className="button button-quiet" href={repositoryUrl}>
                View source
              </a>
            </div>
          </div>
        </section>

        <section className="proof-strip shell" aria-label="Marketplace totals">
          <div>
            <strong>{totals.plugins}</strong>
            <span>Public plugins</span>
          </div>
          <div>
            <strong>{totals.skills}</strong>
            <span>Bundled skills</span>
          </div>
          <div>
            <strong>{resourceTotal.toLocaleString("en-US")}</strong>
            <span>Support files</span>
          </div>
          <div>
            <strong>1</strong>
            <span>Copyable marketplace</span>
          </div>
        </section>

        <section className="catalog-section shell" id="plugins">
          <div className="section-heading">
            <h2>Find the capability. Inspect the package. Copy the command.</h2>
            <p>
              Search every plugin and skill, select a record, then install only
              what belongs in your Codex setup.
            </p>
          </div>
          <Catalog />
        </section>

        <section className="install-section" id="install">
          <div className="shell install-layout">
            <div className="install-intro">
              <p className="kicker">Install in Codex</p>
              <h2>One marketplace. Any plugin.</h2>
              <p>
                Add the public source once, install what you need, then open a
                fresh task so Codex can load the new capability inventory.
              </p>
            </div>
            <ol className="install-steps">
              <li>
                <div className="step-heading">
                  <span>01</span>
                  <h3>Add the marketplace</h3>
                </div>
                <CopyCommand command="codex plugin marketplace add Israelmusondaayliffe/codex-plugins --ref main" />
              </li>
              <li>
                <div className="step-heading">
                  <span>02</span>
                  <h3>Install a plugin</h3>
                </div>
                <CopyCommand command="codex plugin add loopkit@israel-codex-plugins" />
              </li>
              <li>
                <div className="step-heading">
                  <span>03</span>
                  <h3>Start a new task</h3>
                </div>
                <p>
                  Fresh tasks load the installed plugin inventory. Existing
                  tasks may retain their earlier capability list.
                </p>
              </li>
            </ol>
          </div>
        </section>

        <section className="inventory-section shell">
          <div className="inventory-statement">
            <h2>Skills first. Claims kept exact.</h2>
            <p>
              This release includes skills, scripts, references, assets, and
              agent definitions. It does not currently bundle MCP servers or
              app connectors.
            </p>
            <Link className="text-link" href="/plugins/capability-operator">
              Inspect a complete plugin record
            </Link>
          </div>
          <dl className="inventory-facts">
            <div>
              <dt>Repository</dt>
              <dd>Public on GitHub</dd>
            </div>
            <div>
              <dt>Marketplace</dt>
              <dd>israel-codex-plugins</dd>
            </div>
            <div>
              <dt>Install surface</dt>
              <dd>Codex CLI</dd>
            </div>
            <div>
              <dt>Discovery</dt>
              <dd>Fresh task required</dd>
            </div>
          </dl>
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
