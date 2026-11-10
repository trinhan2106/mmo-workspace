'use strict';

const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');

function assertWithin(base, target) {
  const relative = path.relative(path.resolve(base), path.resolve(target));
  if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error('Target escapes the scoped repository directory');
  }
  let ancestor = path.resolve(target);
  while (!fs.existsSync(ancestor)) ancestor = path.dirname(ancestor);
  const realBase = fs.existsSync(base) ? fs.realpathSync(base) : path.resolve(base);
  const realAncestor = fs.realpathSync(ancestor);
  // Missing parents may be outside a not-yet-created base. Callers create the
  // scoped base first, so existing symlink/junction parents can be checked.
  const realRelative = path.relative(realBase, realAncestor);
  if (
    realRelative === '..' ||
    realRelative.startsWith(`..${path.sep}`) ||
    path.isAbsolute(realRelative)
  ) {
    throw new Error('Existing path resolves outside the scoped directory');
  }
  return path.resolve(target);
}

function catalog() {
  const value = JSON.parse(fs.readFileSync(path.join(ROOT, 'jailbreak/catalog.json'), 'utf8'));
  if (value.schema_version !== 1 || value.name !== 'byPass' || !Array.isArray(value.profiles)) {
    throw new Error('Invalid byPass catalog');
  }
  const ids = new Set();
  const profileBase = path.join(ROOT, 'jailbreak/byPass/profiles');
  for (const profile of value.profiles) {
    if (!/^[a-z][a-z0-9-]*$/.test(profile.id) || ids.has(profile.id) || !profile.purpose) {
      throw new Error('Invalid or duplicate profile ID');
    }
    const file = assertWithin(profileBase, path.join(ROOT, profile.path));
    if (!file.endsWith('.md') || !fs.statSync(file).isFile())
      throw new Error('Profile must be Markdown');
    ids.add(profile.id);
  }
  if (!ids.has(value.default_profile)) throw new Error('Default profile is missing');
  const source = value.source;
  if (source.repository !== '3641397194-wq/gpt6-Astra' || !/^[a-f0-9]{40}$/.test(source.commit)) {
    throw new Error('Unexpected upstream identity');
  }
  if (
    source.checkout !== 'jailbreak/gpt6-Astra' ||
    source.codex_home !== 'jailbreak/local/codex-home'
  ) {
    throw new Error('Unexpected source or installation target');
  }
  return value;
}

function scopedEnvironment() {
  const base = path.join(ROOT, 'jailbreak/local');
  fs.mkdirSync(base, { recursive: true });
  assertWithin(ROOT, base);
  const environment = { ...process.env };
  for (const key of Object.keys(environment)) {
    if (/(?:API_?KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|AUTHORIZATION|COOKIE)/i.test(key)) {
      delete environment[key];
    }
  }
  const directories = {
    USERPROFILE: 'user',
    HOME: 'user',
    APPDATA: 'appdata/roaming',
    LOCALAPPDATA: 'appdata/local',
    XDG_CONFIG_HOME: 'xdg/config',
    XDG_DATA_HOME: 'xdg/data',
    XDG_CACHE_HOME: 'xdg/cache',
    TEMP: 'temp',
    TMP: 'temp',
    TMPDIR: 'temp',
    CODEX_HOME: 'codex-home',
    CODEX_DIR: 'codex-home',
    CLAUDE_CONFIG_DIR: 'clients/.claude',
    CLAUDE_HOME: 'clients/.claude',
    GROK_HOME: 'clients/.grok',
    GROK_DIR: 'clients/.grok',
    DSH_HOME: 'clients/.dsh',
    GLM_HOME: 'clients/.glm',
    ZCODE_HOME: 'clients/.zcode',
    ZHIPU_HOME: 'clients/.glm',
    GEMINI_HOME: 'clients/.gemini',
    GEMINI_DIR: 'clients/.gemini',
    WORKBUDDY_HOME: 'clients/.workbuddy',
    CURSOR_HOME: 'clients/.cursor',
    MIMOCODE_HOME: 'clients/mimo',
    KIMI_CODE_HOME: 'clients/kimi',
  };
  for (const [key, relative] of Object.entries(directories)) {
    const directory = assertWithin(base, path.join(base, relative));
    fs.mkdirSync(directory, { recursive: true });
    environment[key] = directory;
  }
  environment.PYTHONUTF8 = '1';
  environment.PYTHONIOENCODING = 'utf-8';
  // Do not inherit optional test/portable overrides that redirect upstream data.
  delete environment.COLDCOFFEE_GATEWAY_TEST_HOME;
  delete environment.PORTABLE_EXECUTABLE_FILE;
  delete environment.PORTABLE_EXECUTABLE_DIR;
  delete environment.ELECTRON_RUN_AS_NODE;
  return environment;
}

module.exports = { ROOT, assertWithin, catalog, scopedEnvironment };
