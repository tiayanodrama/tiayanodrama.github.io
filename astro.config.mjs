import { defineConfig } from 'astro/config';

// 部署到 GitHub Pages（默认 *.github.io 用户站，base 留 '/'）
export default defineConfig({
  site: 'https://tiayanodrama.github.io',
  base: '/',
});
