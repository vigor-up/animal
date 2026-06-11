const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const distDir = path.resolve(__dirname);
const screenshotDir = path.join(distDir, 'screenshots');
if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir);

const pages = [
  { file: 'index.html', slug: 'index' },
  { file: 'junzaiwang.html', slug: 'junzaiwang' },
  { file: 'kelionwang.html', slug: 'kelionwang' },
  { file: 'duoluanzhuang.html', slug: 'duoluanzhuang' },
  { file: 'zhangbiaowang.html', slug: 'zhangbiaowang' },
  { file: 'zujinwang.html', slug: 'zujinwang' },
  { file: 'baomiaowang.html', slug: 'baomiaowang' },
];

const viewports = [
  { name: 'desktop', width: 1280, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  let count = 0;

  for (const vp of viewports) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await ctx.newPage();

    for (const pg of pages) {
      const url = 'file:///' + path.join(distDir, pg.file).replace(/\\/g, '/');
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      // wait for fonts (brief)
      await page.waitForTimeout(800);
      const outFile = path.join(screenshotDir, `${pg.slug}_${vp.name}.png`);
      await page.screenshot({ path: outFile, fullPage: false });
      console.log(`[OK] ${pg.slug}_${vp.name}.png`);
      count++;
    }

    await ctx.close();
  }

  await browser.close();
  console.log(`\nDone: ${count} screenshots in ${screenshotDir}`);
})();
