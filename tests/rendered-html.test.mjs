import assert from "node:assert/strict";
import test from "node:test";

async function render(pathname = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", process.pid + "-" + Date.now());
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost" + pathname, {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the public marketplace homepage", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Israel&#x27;s Codex Plugins<\/title>/i);
  assert.match(html, /A working system/);
  assert.match(html, /18(?:<!--.*?-->)? field-tested plugins/);
  assert.match(html, /codex plugin marketplace add Israelmusondaayliffe/);
  assert.match(html, /knowledge-work-superpowers/);
  assert.match(html, /LoopKit/);
  assert.match(html, /Harness Engineering/);
  assert.match(html, /does not currently.*MCP servers/i);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape/);
});

test("server-renders plugin detail pages", async () => {
  const response = await render("/plugins/capability-operator");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /Capability Operator/);
  assert.match(html, /capability-router/);
  assert.match(
    html,
    /codex plugin add capability-operator@israel-codex-plugins/,
  );
});

test("server-renders the Harness Engineering release", async () => {
  const response = await render("/plugins/harness-engineering");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /Harness Engineering/);
  assert.match(html, /harness-interview/);
  assert.match(
    html,
    /codex plugin add harness-engineering@israel-codex-plugins/,
  );
});

test("server-renders the LoopKit release", async () => {
  const response = await render("/plugins/loopkit");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /LoopKit/);
  assert.match(html, /loop-runner/);
  assert.match(
    html,
    /codex plugin add loopkit@israel-codex-plugins/,
  );
});
