import type { Metadata } from "next";
import { headers } from "next/headers";
import { IBM_Plex_Mono, Space_Grotesk } from "next/font/google";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
});

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export async function generateMetadata(): Promise<Metadata> {
  const incoming = await headers();
  const host = incoming.get("x-forwarded-host") ?? incoming.get("host");
  const protocol = incoming.get("x-forwarded-proto") ?? "https";
  const origin = host ? protocol + "://" + host : "http://localhost:3000";
  const title = "Israel's Codex Plugins";
  const description =
    "A public Codex marketplace with 15 plugins and 102 skills for research, strategy, creation, operations, and delivery.";

  return {
    metadataBase: new URL(origin),
    title: {
      default: title,
      template: "%s | " + title,
    },
    description,
    icons: {
      icon: "/favicon.svg",
      shortcut: "/favicon.svg",
    },
    openGraph: {
      title,
      description,
      images: [{ url: origin + "/og.png", width: 1536, height: 1024 }],
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [origin + "/og.png"],
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={spaceGrotesk.variable + " " + ibmPlexMono.variable}>
        {children}
      </body>
    </html>
  );
}
