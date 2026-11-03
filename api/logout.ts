/**
 * GET /api/logout: clears the team access cookie and goes back to the front page.
 */
export function GET(): Response {
  return new Response(null, {
    status: 303,
    headers: { Location: "/", "Set-Cookie": "hcsa_access=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax" },
  });
}
