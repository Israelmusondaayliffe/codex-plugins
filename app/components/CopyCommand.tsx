"use client";

import { useState } from "react";

type CopyCommandProps = {
  command: string;
  compact?: boolean;
};

export function CopyCommand({ command, compact = false }: CopyCommandProps) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
    try {
      if (!navigator.clipboard) throw new Error("Clipboard API unavailable");
      await navigator.clipboard.writeText(command);
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = command;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
    }
  }

  return (
    <div className={"copy-command" + (compact ? " copy-command-compact" : "")}>
      <code>{command}</code>
      <button
        aria-label={copied ? "Command copied" : "Copy command: " + command}
        onClick={copy}
        type="button"
      >
        {copied ? "Copied" : "Copy"}
      </button>
      <span className="sr-only" aria-live="polite">
        {copied ? "Command copied to clipboard" : ""}
      </span>
    </div>
  );
}
