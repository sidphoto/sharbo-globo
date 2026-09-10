/**
 * SharBo Globo public reference: precise external trigger for GitHub Actions.
 *
 * Required Worker secrets/vars:
 *   GITHUB_TOKEN      fine-grained token with Actions: write for the target repo
 *   GITHUB_OWNER      repository owner
 *   GITHUB_REPO       repository name
 * Optional:
 *   GITHUB_WORKFLOW   defaults to daily-demo.yml
 *   GITHUB_REF        defaults to main
 *   TRIGGER_KEY       enables authenticated manual GET testing
 */

function setting(env, name, fallback = "") {
  const value = String(env[name] || fallback).trim();
  if (!value) throw new Error(`Missing Worker setting: ${name}`);
  return value;
}

async function dispatch(env) {
  const owner = setting(env, "GITHUB_OWNER");
  const repo = setting(env, "GITHUB_REPO");
  const workflow = String(env.GITHUB_WORKFLOW || "daily-demo.yml").trim();
  const ref = String(env.GITHUB_REF || "main").trim();
  const token = setting(env, "GITHUB_TOKEN");
  const endpoint = `https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflow}/dispatches`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "sharbo-globo-public-trigger",
    },
    body: JSON.stringify({ ref }),
  });

  if (!response.ok) {
    throw new Error(`GitHub dispatch failed: ${response.status} ${await response.text()}`);
  }
  return `dispatched ${owner}/${repo}:${workflow}@${ref}`;
}

function sameSecret(a, b) {
  let mismatch = a.length ^ b.length;
  const width = Math.max(a.length, b.length, 1);
  for (let i = 0; i < width; i += 1) {
    mismatch |= a.charCodeAt(i % (a.length || 1)) ^ b.charCodeAt(i % (b.length || 1));
  }
  return mismatch === 0;
}

export default {
  async scheduled(_event, env, ctx) {
    ctx.waitUntil(dispatch(env).then(console.log).catch((error) => console.error(String(error))));
  },

  async fetch(request, env) {
    if (!env.TRIGGER_KEY) return new Response("not found\n", { status: 404 });
    if (request.method !== "GET") return new Response("method not allowed\n", { status: 405 });
    const supplied = new URL(request.url).searchParams.get("key") || "";
    if (!sameSecret(supplied, String(env.TRIGGER_KEY))) {
      return new Response("not found\n", { status: 404 });
    }
    try {
      return new Response(`${await dispatch(env)}\n`);
    } catch (error) {
      return new Response(`${String(error)}\n`, { status: 502 });
    }
  },
};
