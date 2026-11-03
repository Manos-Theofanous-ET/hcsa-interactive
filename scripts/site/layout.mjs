// After `vite build`: one site, two sides.
//  - the public front page (public/preview/index.html) becomes dist/index.html, served at /
//  - the older scroll-driven app (Vite's index.html) moves to dist/story/index.html, behind the password
// Its JS and CSS live in /assets/ with absolute paths, so moving the HTML is enough.
import fs from "node:fs";
const dist = new URL("../../dist/", import.meta.url);
fs.mkdirSync(new URL("story/", dist), { recursive: true });
fs.renameSync(new URL("index.html", dist), new URL("story/index.html", dist));
fs.copyFileSync(new URL("preview/index.html", dist), new URL("index.html", dist));
console.log("layout: / = public front page, /story/ = earlier scroll site");
