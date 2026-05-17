// Render a Brand Foundations one-pager to PNG + PDF.
//   node scripts/render-sheet.js <brand-foundations.html>
// Resolves Playwright from this skill, else a sibling image-studio skill.
const path = require('path'), fs = require('fs');

function loadChromium() {
  const tries = [
    'playwright',
    path.join(__dirname, '..', 'node_modules', 'playwright'),
    path.join(__dirname, '..', '..', 'image-studio', 'node_modules', 'playwright'),
  ];
  for (const t of tries) { try { return require(t).chromium; } catch (e) {} }
  console.error('Playwright not found. `npm i playwright` in this skill, or '
    + 'install the image-studio skill alongside it.');
  process.exit(1);
}

(async () => {
  const input = process.argv[2];
  if (!input || !fs.existsSync(input)) { console.error('usage: render-sheet.js <html>'); process.exit(1); }
  const base = input.replace(/\.html$/, '');
  const chromium = loadChromium();
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1240, height: 1754 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: base + '.png', fullPage: true });
  await p.pdf({ path: base + '.pdf', width: '1240px', printBackground: true,
                margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await b.close();
  console.log('PNG:', base + '.png');
  console.log('PDF:', base + '.pdf');
})();
