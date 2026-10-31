/**
 * POST /api/login with form field "password" (and optional "next").
 * Sets the access cookie the middleware checks, then sends the visitor on.
 */
import { createHash } from "node:crypto";

const COOKIE = "hcsa_access";
const MAX_AGE = 60 * 60 * 24 * 30;
const tokenFor = (pw: string) => createHash("sha256").update(`${pw}:hcsa-access-v1`).digest("hex");

export async function POST(req: Request): Promise<Response> {
  const form = await req.formData();
  const given = String(form.get("password") || "");
  let next = String(form.get("next") || "/");
  if (!next.startsWith("/") || next.startsWith("//")) next = "/";
  const envPw = process.env.SITE_PASSWORD?.trim();
  const good = envPw ? tokenFor(envPw) : "";
  if (!good || !given || tokenFor(given.trim()) !== good) {
    return new Response(null, { status: 303, headers: { Location: `/preview/?e=1&next=${encodeURIComponent(next)}#access` } });
  }
  const token = good;
  return new Response(null, {
    status: 303,
    headers: {
      Location: next,
      "Set-Cookie": `${COOKIE}=${token}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
    },
  });
}

export function GET(): Response {
  return new Response(null, { status: 303, headers: { Location: "/preview/#access" } });
}
