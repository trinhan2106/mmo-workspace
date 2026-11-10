'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const { ROOT, assertWithin, catalog, scopedEnvironment } = require('../scripts/bypass/paths.cjs');

test('catalog resolves project-owned coding/writing profiles', () => {
  const config = catalog();
  assert.equal(config.default_profile, 'coding');
  const ids = new Set(config.profiles.map((item) => item.id));
  assert.ok(ids.has('coding'));
  assert.ok(ids.has('writing'));
});

test('target guard rejects parent traversal and outside absolute paths', () => {
  assert.throws(() => assertWithin(ROOT, path.join(ROOT, '../outside')), /escapes/);
  assert.equal(assertWithin(ROOT, path.join(ROOT, 'docs')), path.join(ROOT, 'docs'));
});

test('child homes/caches are scoped without modifying the parent environment', () => {
  const original = process.env.CODEX_HOME;
  const environment = scopedEnvironment();
  assert.equal(process.env.CODEX_HOME, original);
  for (const key of [
    'HOME',
    'USERPROFILE',
    'APPDATA',
    'LOCALAPPDATA',
    'CODEX_HOME',
    'TEMP',
    'DSH_HOME',
  ]) {
    assertWithin(path.join(ROOT, 'jailbreak/local'), environment[key]);
    assert.ok(fs.statSync(environment[key]).isDirectory());
  }
  assert.equal(environment.COLDCOFFEE_GATEWAY_TEST_HOME, undefined);
  for (const key of Object.keys(environment)) {
    assert.ok(!/(?:API_?KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|AUTHORIZATION|COOKIE)/i.test(key));
  }
});
