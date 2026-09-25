import { chromium } from "@playwright/test";
const S = process.argv[2];
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = [];
p.on("console", (m) => m.type() === "error" && errs.push(m.text()));
p.on("pageerror", (e) => errs.push(String(e)));
p.on("requestfailed", (r) => errs.push("FAIL " + r.url()));
p.on("response", (r) => r.status() >= 400 && errs.push(r.status() + " " + r.url()));
await p.goto("http://localhost:4173/", { waitUntil: "networkidle" });
await p.waitForTimeout(4000);
await p.screenshot({ path: `${S}/01-hero.png` });
for (const id of ["panel", "contact"]) {
  await p.evaluate((id) => document.getElementById(id).scrollIntoView(), id);
  await p.waitForTimeout(2500);
  await p.screenshot({ path: `${S}/02-${id}.png` });
}
for (const id of ["about", "work", "sponsor", "team"]) {
  await p.evaluate((id) => document.getElementById(id).scrollIntoView(), id);
  await p.waitForTimeout(1200);
  await p.screenshot({ path: `${S}/03-${id}.png`, fullPage: false });
}
await p.evaluate(() => document.getElementById("work").scrollIntoView());
await p.getByRole("tab", { name: /Engineering sheets/ }).click();
await p.waitForTimeout(800);
await p.screenshot({ path: `${S}/04-sheets.png` });
await p.locator("#work-panel button").first().click();
await p.waitForTimeout(1200);
await p.keyboard.press("ArrowRight");
await p.waitForTimeout(1200);
await p.screenshot({ path: `${S}/05-viewer.png` });
await p.keyboard.press("Escape");
const info = await p.evaluate(() => ({
  open: document.querySelector("dialog").open,
  railOpacity: document.querySelector('nav[aria-label="Chapter navigation"]').style.opacity,
  film: document.getElementById("film").offsetHeight,
  doc: document.documentElement.scrollHeight,
}));
console.log(JSON.stringify(info));
// all gallery images load?
const bad = [];
const tabs = await p.getByRole("tab").all();
for (const t of tabs) {
  await t.click();
  await p.waitForTimeout(300);
  for (const img of await p.locator("#work-panel img").all()) {
    await img.scrollIntoViewIfNeeded();
    await p.waitForTimeout(150);
    const ok = await img.evaluate((i) => i.complete && i.naturalWidth > 0);
    if (!ok) bad.push(await img.getAttribute("src"));
  }
}
console.log("bad images", bad);
console.log("errors", [...new Set(errs)].slice(0,15));
const m = await b.newPage({ viewport: { width: 390, height: 844 } });
await m.goto("http://localhost:4173/", { waitUntil: "networkidle" });
await m.waitForTimeout(3000);
await m.screenshot({ path: `${S}/06-mobile-hero.png` });
await m.evaluate(() => document.getElementById("sponsor").scrollIntoView());
await m.waitForTimeout(800);
await m.screenshot({ path: `${S}/07-mobile-sponsor.png` });
const ov = await m.evaluate(() => document.documentElement.scrollWidth);
console.log("mobile scrollWidth", ov);
await b.close();
