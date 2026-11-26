const { copyFile, mkdir } = require('node:fs/promises');
const { join, resolve } = require('node:path');

// Copy the prepared image into the collection directory supplied by make.fun.
(async () => {
  const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR || '/output');
  await mkdir(outputDir, { recursive: true });
  await copyFile(join(__dirname, 'entry.png'), join(outputDir, 'entry.png'));
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
