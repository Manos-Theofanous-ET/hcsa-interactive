/**
 * Password gate for the whole site (Vercel Routing Middleware, works with Vite).
 *
 * Public without a password: /preview (the public page), the login endpoint,
 * the favicon, link-preview images, robots.txt and fonts.
 * Everything else needs the access cookie, which /api/login sets when the
 * password matches the SITE_PASSWORD environment variable on Vercel.
 *
 * A one-click link also works: any page with ?access=<password> sets the
 * cookie and reloads the page without the parameter.
 *
 * The password is never in the code: it is the SITE_PASSWORD environment
 * variable in the Vercel project settings (Production and Preview). Until it
 * is set, the gate stays open and the site behaves as before. To change the
 * password, edit the variable and redeploy.
 */
export const config = {
  matcher: ["/((?!_vercel).*)"],
};

const PUBLIC = [
  /^\/preview(\/.*)?$/,
  /^\/api\/login$/,
  /^\/favicon\.svg$/,
  /^\/og-[\w-]+\.jpg$/,
  /^\/og-image\.jpg$/,
  /^\/robots\.txt$/,
  /^\/fonts\//,
];

const COOKIE = "hcsa_access";
const MAX_AGE = 60 * 60 * 24 * 30; // 30 days

async function tokenFor(password: string): Promise<string> {
  const data = new TextEncoder().encode(`${password}:hcsa-access-v1`);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(hash), (b) => b.toString(16).padStart(2, "0")).join("");
}

function readCookie(req: Request, name: string): string | null {
  const raw = req.headers.get("cookie") || "";
  for (const part of raw.split(/;\s*/)) {
    const i = part.indexOf("=");
    if (i > 0 && part.slice(0, i) === name) return decodeURIComponent(part.slice(i + 1));
  }
  return null;
}

const next = () => new Response(null, { headers: { "x-middleware-next": "1" } });

export default async function middleware(req: Request): Promise<Response> {
  const url = new URL(req.url);
  if (PUBLIC.some((re) => re.test(url.pathname))) return next();

  const envPw = process.env.SITE_PASSWORD;
  if (!envPw) return next(); // gate stays open until SITE_PASSWORD is set in Vercel
  const good = await tokenFor(envPw);

  const access = url.searchParams.get("access");
  if (access !== null) {
    url.searchParams.delete("access");
    if ((await tokenFor(access)) === good) {
      return new Response(null, {
        status: 303,
        headers: {
          Location: url.pathname + (url.search || "") + url.hash,
          "Set-Cookie": `${COOKIE}=${good}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
        },
      });
    }
  }

  if (readCookie(req, COOKIE) === good) return next();

  const to = new URL("/preview/", url.origin);
  if (url.pathname !== "/") to.searchParams.set("next", url.pathname + url.search);
  return Response.redirect(to.toString(), 302);
}
