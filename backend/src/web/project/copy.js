import fs from 'fs/promises';
import path from 'path';

const sourceDirectory = path.resolve('../templates');
const destinationDirectory = path.resolve('../../../static');
const copyFiles = async (source, destination) => {
    if (!await fs.access(destination).then(() => true).catch(() => false)) {
      await fs.mkdir(destination, { recursive: true });
    }
    const entries = await fs.readdir(source, { withFileTypes: true });

    for (const entry of entries) {
      const sourcePath = path.join(source, entry.name);
      const destinationPath = path.join(destination, entry.name);
      if (entry.isDirectory()) {
        await copyFiles(sourcePath, destinationPath);
        await fs.rmdir(sourcePath);
      } else if (path.extname(entry.name) !== '.html') {
        await fs.copyFile(sourcePath, destinationPath);
        await fs.unlink(sourcePath);
      }
    }
};
try{
  copyFiles(sourceDirectory, destinationDirectory);
  console.log('Copy done.');
} catch (err) {
  console.error('Copy error:', err);
}