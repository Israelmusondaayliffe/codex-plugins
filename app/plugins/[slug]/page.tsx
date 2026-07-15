import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CopyCommand } from "../../components/CopyCommand";
import { marketplaceName, plugins } from "../../catalog.generated";

type PluginPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return plugins.map((plugin) => ({ slug: plugin.slug }));
}

export async function generateMetadata({
  params,
}: PluginPageProps): Promise<Metadata> {
  const { slug } = await params;
  const plugin = plugins.find((item) => item.slug === slug);
  if (!plugin) return {};
  return {
    title: plugin.name,
    description: plugin.longDescription,
  };
}

export default async function PluginPage({ params }: PluginPageProps) {
  const { slug } = await params;
  const plugin = plugins.find((item) => item.slug === slug);
  if (!plugin) notFound();

  return (
    <>
      <header className="site-header shell detail-header">
        <Link className="wordmark" href="/" aria-label="Back to plugin catalog">
          <span>IA</span>
          <span>/</span>
          <span>CODEX</span>
        </Link>
        <Link className="back-link" href="/#plugins">
          Back to catalog
        </Link>
      </header>

      <main className="plugin-detail shell">
        <section className="detail-hero">
          <div>
            <p className="eyebrow">{plugin.category}</p>
            <h1>{plugin.name}</h1>
            <p>{plugin.longDescription}</p>
          </div>
          <dl className="detail-stats">
            <div>
              <dt>Version</dt>
              <dd>{plugin.version}</dd>
            </div>
            <div>
              <dt>Skills</dt>
              <dd>{plugin.counts.skills}</dd>
            </div>
            <div>
              <dt>Files</dt>
              <dd>{plugin.counts.files}</dd>
            </div>
          </dl>
        </section>

        <section className="detail-install">
          <p className="eyebrow">Install this plugin</p>
          <CopyCommand
            command={
              "codex plugin add " + plugin.slug + "@" + marketplaceName
            }
          />
          <p className="install-note">
            Add the marketplace first if you have not already, then start a new
            Codex task after installation.
          </p>
        </section>

        <section className="skill-list-section">
          <div className="section-heading">
            <p className="eyebrow">Bundled capabilities</p>
            <h2>Every skill in this plugin.</h2>
          </div>
          <div className="skill-list">
            {plugin.skills.map((skill, index) => (
              <article key={skill.name}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <div>
                  <h3>{skill.name}</h3>
                  <p>{skill.description}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="package-facts">
          <div>
            <span>{plugin.counts.assets}</span>
            <p>Asset files</p>
          </div>
          <div>
            <span>{plugin.counts.references}</span>
            <p>Reference files</p>
          </div>
          <div>
            <span>{plugin.counts.scripts}</span>
            <p>Script files</p>
          </div>
          <div>
            <span>{plugin.license ?? "See legal"}</span>
            <p>License status</p>
          </div>
        </section>
      </main>

      <footer>
        <div className="shell footer-grid">
          <p className="footer-name">Israel&apos;s Codex Plugins</p>
          <Link href="/">Browse all plugins</Link>
        </div>
      </footer>
    </>
  );
}
