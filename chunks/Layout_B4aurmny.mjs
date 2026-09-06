import { b as createAstro, c as createComponent, m as maybeRenderHead, d as addAttribute, a as renderTemplate, e as renderHead, r as renderComponent, f as renderSlot } from './astro/server_DOuRIHWv.mjs';
import 'kleur/colors';
import 'html-escaper';
/* empty css                         */
import 'clsx';

const $$Astro$1 = createAstro("https://tiayanodrama.github.io");
const $$Nav = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$Nav;
  const links = [
    { href: "/", label: "HOME", cn: "\u9996\u9875" },
    { href: "/about", label: "ABOUT", cn: "\u5173\u4E8E\u6211" },
    { href: "/works", label: "WORKS", cn: "\u4F5C\u54C1" },
    { href: "/method", label: "METHOD", cn: "\u65B9\u6CD5\u8BBA" },
    { href: "/manual", label: "MANUAL", cn: "\u8BF4\u660E\u4E66" },
    { href: "/contact", label: "CONTACT", cn: "\u8054\u7CFB" }
  ];
  const path = Astro2.url.pathname;
  return renderTemplate`${maybeRenderHead()}<header class="nav" data-astro-cid-dmqpwcec> <a class="brand" href="/" data-astro-cid-dmqpwcec> <span class="brand-mark" data-astro-cid-dmqpwcec>TT</span> <span class="brand-sep" data-astro-cid-dmqpwcec>/</span> <span class="brand-name cn" data-astro-cid-dmqpwcec>ZHANG TIANTIAN</span> </a> <nav class="nav-links" data-astro-cid-dmqpwcec> ${links.map((l) => renderTemplate`<a${addAttribute(l.href, "href")}${addAttribute(["nav-link", { active: path === l.href || l.href !== "/" && path.startsWith(l.href) }], "class:list")} data-astro-cid-dmqpwcec> <span class="nl-en" data-astro-cid-dmqpwcec>${l.label}</span> <span class="nl-cn" data-astro-cid-dmqpwcec>${l.cn}</span> </a>`)} </nav> <div class="nav-status mono" data-astro-cid-dmqpwcec> <span class="led" data-astro-cid-dmqpwcec></span> <span class="led-text" data-astro-cid-dmqpwcec>ONLINE · 2026</span> </div> </header> `;
}, "C:/Users/Zhang tian tian/WorkBuddy/\u5317\u8FB0\u9752\u5E74/\u4E2A\u4EBA\u7AD9/src/components/Nav.astro", void 0);

const $$Footer = createComponent(($$result, $$props, $$slots) => {
  const year = (/* @__PURE__ */ new Date()).getFullYear();
  return renderTemplate`${maybeRenderHead()}<footer class="ft" data-astro-cid-sz7xmlte> <div class="ft-inner" data-astro-cid-sz7xmlte> <div class="ft-left" data-astro-cid-sz7xmlte> <span class="ft-brand mono" data-astro-cid-sz7xmlte>© ${year} ZHANG · TIANTIAN</span> <span class="ft-sub" data-astro-cid-sz7xmlte>写作 · AI 协作 · 研究 · 摄影 · 一切还在生长中</span> </div> <div class="ft-links mono" data-astro-cid-sz7xmlte> <a href="mailto:zhangtiantianxyt@163.com" data-astro-cid-sz7xmlte>EMAIL</a> <a href="https://github.com/tiayanodrama" target="_blank" rel="noopener" data-astro-cid-sz7xmlte>GITHUB</a> <a href="/about" data-astro-cid-sz7xmlte>ABOUT</a> <a href="/works" data-astro-cid-sz7xmlte>WORKS</a> <a href="/manual" data-astro-cid-sz7xmlte>MANUAL</a> </div> <div class="ft-version mono" data-astro-cid-sz7xmlte> <span class="ft-led" data-astro-cid-sz7xmlte></span>
v8.0 · ${year} </div> </div> </footer> `;
}, "C:/Users/Zhang tian tian/WorkBuddy/\u5317\u8FB0\u9752\u5E74/\u4E2A\u4EBA\u7AD9/src/components/Footer.astro", void 0);

const $$Astro = createAstro("https://tiayanodrama.github.io");
const $$Layout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Layout;
  const { title = "TT \xB7 \u5F20\u751C\u6E49", description = "\u4E00\u4E2A\u628A\u96F6\u6563\u4EA7\u51FA\u634F\u6210\u4F5C\u54C1\u7684\u4E2A\u4EBA\u7AD9\u3002\u5199\u4F5C\u3001AI \u534F\u4F5C\u3001\u7814\u7A76\u3001\u6444\u5F71\u3001\u8FD0\u52A8\u2014\u2014\u5173\u4E8E\u6211\u600E\u4E48\u60F3\u3001\u600E\u4E48\u505A\u3002" } = Astro2.props;
  const stars = Array.from({ length: 80 }).map((_, i) => {
    const colors = ["", "", "big", "pink", "cyan", "purple"];
    const pick = colors[Math.floor(Math.random() * colors.length)];
    return {
      x: Math.random() * 100,
      y: Math.random() * 100,
      d: 2 + Math.random() * 4,
      delay: Math.random() * 5,
      cls: pick
    };
  });
  const meteors = [
    { y: 12, x: -5, dur: 7, delay: 0.5, cls: "pink" },
    { y: 28, x: -8, dur: 9, delay: 3.2, cls: "cyan" },
    { y: 46, x: -10, dur: 6, delay: 6.5, cls: "purple" },
    { y: 66, x: -4, dur: 8, delay: 2, cls: "warm" },
    { y: 82, x: -12, dur: 11, delay: 8, cls: "pink" }
  ];
  return renderTemplate`<html lang="zh-CN"> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title><meta name="description"${addAttribute(description, "content")}><meta property="og:title"${addAttribute(title, "content")}><meta property="og:description"${addAttribute(description, "content")}><meta property="og:type" content="website"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Noto+Serif+SC:wght@400;500;700&display=swap" rel="stylesheet">${renderHead()}</head> <body> <!-- 星空层 --> <div class="starfield" aria-hidden="true"> ${stars.map((s) => renderTemplate`<span${addAttribute(`s-star ${s.cls}`, "class")}${addAttribute(`top:${s.y}%;left:${s.x}%;--d:${s.d}s;--delay:${s.delay}s`, "style")}></span>`)} </div> <!-- 流星层 --> <div class="meteor-field" aria-hidden="true"> ${meteors.map((m) => renderTemplate`<span${addAttribute(`meteor ${m.cls}`, "class")}${addAttribute(`--y:${m.y}%;--x:${m.x}%;--dur:${m.d}s;--delay:${m.delay}s`, "style")}></span>`)} </div> <!-- 全局装饰层：扫描线 + 角标 --> <div class="scanlines" aria-hidden="true"></div> <div class="corner-deco" aria-hidden="true"> <span class="cd tl"></span><span class="cd tr"></span> <span class="cd bl"></span><span class="cd br"></span> </div> ${renderComponent($$result, "Nav", $$Nav, {})} <main class="main"> ${renderSlot($$result, $$slots["default"])} </main> ${renderComponent($$result, "Footer", $$Footer, {})} </body></html>`;
}, "C:/Users/Zhang tian tian/WorkBuddy/\u5317\u8FB0\u9752\u5E74/\u4E2A\u4EBA\u7AD9/src/layouts/Layout.astro", void 0);

export { $$Layout as $ };
