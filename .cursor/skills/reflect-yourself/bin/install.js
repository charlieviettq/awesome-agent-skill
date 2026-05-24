#!/usr/bin/env node

/**
 * reflect-yourself installer for npm/npx
 * Installs the skill to ~/.cursor/skills/ for global availability
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const DEST_DIR = path.join(os.homedir(), '.cursor', 'skills', 'reflect-yourself');
const COMMANDS_DIR = path.join(os.homedir(), '.cursor', 'commands');
const QUEUE_FILE = path.join(os.homedir(), '.cursor', 'reflect-queue.json');

// Get the package root (parent of bin/)
const PKG_ROOT = path.join(__dirname, '..');
const PKG_JSON = require(path.join(PKG_ROOT, 'package.json'));
const VERSION = PKG_JSON.version;

console.log('');
console.log(`reflect-yourself installer v${VERSION}`);
console.log('='.repeat(`reflect-yourself installer v${VERSION}`.length));
console.log('');

// Create destination directories
const dirs = [
    DEST_DIR,
    COMMANDS_DIR,
    path.join(DEST_DIR, 'commands'),
    path.join(DEST_DIR, 'rules'),
    path.join(DEST_DIR, 'references')
];

dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Files to copy
const files = [
    { src: 'SKILL.md', dest: 'SKILL.md' },
    { src: 'commands/reflect-yourself.md', dest: 'commands/reflect-yourself.md' },
    { src: 'commands/reflect-yourself-skills.md', dest: 'commands/reflect-yourself-skills.md' },
    { src: 'commands/reflect-yourself-queue.md', dest: 'commands/reflect-yourself-queue.md' },
    { src: 'commands/reflect-yourself-skip.md', dest: 'commands/reflect-yourself-skip.md' },
    { src: 'rules/session-reflect.mdc', dest: 'rules/session-reflect.mdc' },
    { src: 'references/ONBOARDING.md', dest: 'references/ONBOARDING.md' }
];

console.log('Installing files...');

files.forEach(file => {
    const srcPath = path.join(PKG_ROOT, file.src);
    const destPath = path.join(DEST_DIR, file.dest);
    
    if (fs.existsSync(srcPath)) {
        // Inject version into files with frontmatter descriptions (skip references)
        if ((file.src === 'SKILL.md' || file.src.startsWith('commands/')) && !file.src.startsWith('references/')) {
            let content = fs.readFileSync(srcPath, 'utf8');
            // Ensure description ends with (vX.Y.Z). — add or replace existing version
            content = content.replace(
                /^(description: .+?)(\s*\(v\d+\.\d+\.\d+\))?(\.)?\s*$/m,
                (_, desc, _v, dot) => `${desc} (v${VERSION})${dot || '.'}`
            );
            fs.writeFileSync(destPath, content);
            if (file.src.startsWith('commands/')) {
                const flatPath = path.join(COMMANDS_DIR, path.basename(file.src));
                fs.writeFileSync(flatPath, content);
                console.log(`  ✓ ${file.dest} → also ${flatPath}`);
            } else {
                console.log(`  ✓ ${file.dest}`);
            }
        } else {
            fs.copyFileSync(srcPath, destPath);
            console.log(`  ✓ ${file.dest}`);
        }
    } else {
        console.error(`  ✗ ${file.src} not found`);
    }
});

// Create empty queue file if it doesn't exist
if (!fs.existsSync(QUEUE_FILE)) {
    fs.writeFileSync(QUEUE_FILE, JSON.stringify({ version: 1, learnings: [] }, null, 2));
    console.log(`  ✓ Created queue file`);
}

console.log('');
console.log(`Installed to ${DEST_DIR}`);
console.log(`Commands overwritten in ${COMMANDS_DIR} (v${VERSION}).`);
console.log(`  → Main command: ${path.join(COMMANDS_DIR, 'reflect-yourself.md')}`);
console.log('');
console.log('All listed files were overwritten. If Cursor still shows old command content, restart Cursor or open the command file above to confirm.');
console.log('');
console.log('The skill is now available in ALL your Cursor projects.');
console.log('');
console.log('Commands:');
console.log('  /reflect-yourself        - Capture learnings from session');
console.log('  /reflect-yourself-skills - Discover skill patterns');
console.log('  /reflect-yourself-queue  - View pending learnings');
console.log('  /reflect-yourself-skip   - Clear the queue');
console.log('');
console.log('Run /reflect-yourself at the end of your sessions!');
console.log('');
console.log('To update later, run: npx reflect-yourself@latest');
console.log('');

// Non-blocking check for newer version on registry
const https = require('https');
https.get('https://registry.npmjs.org/reflect-yourself/latest', { timeout: 3000 }, (res) => {
    let data = '';
    res.on('data', (ch) => { data += ch; });
    res.on('end', () => {
        try {
            const latest = JSON.parse(data).version;
            if (latest && latest !== VERSION) {
                const [a, b, c] = VERSION.split('.').map(Number);
                const [x, y, z] = latest.split('.').map(Number);
                if (x > a || (x === a && y > b) || (x === a && y === b && z > c)) {
                    console.log(`A newer version (${latest}) is available. Run: npx reflect-yourself@latest`);
                    console.log('');
                }
            }
        } catch (_) { /* ignore */ }
    });
}).on('error', () => { /* ignore */ });
