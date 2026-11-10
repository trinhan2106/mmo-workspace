'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');
const { ROOT, assertWithin, scopedEnvironment } = require('./paths.cjs');

function sourceRoot(config) {
  const root = assertWithin(ROOT, path.join(ROOT, config.source.checkout));
  const result = spawnSync('git', ['-C', root, 'rev-parse', 'HEAD'], {
    encoding: 'utf8',
    windowsHide: true,
  });
  if (result.error)
    throw new Error(
      `Git preflight could not run (${result.error.code}); check execution permissions`,
    );
  if (result.status !== 0 || result.stdout.trim() !== config.source.commit) {
    throw new Error('Pinned upstream checkout missing or changed; run setup-bypass.ps1');
  }
  const dirty = spawnSync('git', ['-C', root, 'diff', '--name-only', 'HEAD'], {
    encoding: 'utf8',
    windowsHide: true,
  });
  if (dirty.status !== 0 || dirty.stdout.trim())
    throw new Error('Upstream tracked files changed; preserve and reconcile them');
  return root;
}

function seatAction(config, action) {
  if (action === 'install') {
    const state = JSON.parse(fs.readFileSync(path.join(ROOT, 'project/tasks.json'), 'utf8'));
    if (state.tasks.some((task) => task.id === 'T018' && task.status === 'blocked')) {
      throw new Error(
        'T018 blocks full bundle deployment after Defender detection; no automatic retry',
      );
    }
  }
  const root = sourceRoot(config);
  const runtime = require(path.join(root, 'desktop/src/lib/seat-runtime.js'));
  const home = path.join(ROOT, config.source.codex_home);
  fs.mkdirSync(home, { recursive: true });
  assertWithin(ROOT, home);
  const safetyNote = path.join(ROOT, 'jailbreak/local/INSTALL-BLOCKED.json');
  if (action === 'install' && fs.existsSync(safetyNote)) {
    throw new Error(
      'Full bundle installation is blocked by the recorded Defender event; see T018. No automatic retry.',
    );
  }
  const plan = runtime.plan('codex', home);
  for (const write of plan.writes) {
    assertWithin(home, write.file);
    if (write.home) assertWithin(home, write.home);
  }
  if (action === 'preview') {
    return {
      ok: true,
      action,
      home,
      sourceCommit: config.source.commit,
      plannedFiles: plan.writes.length,
    };
  }
  const options = { planFn: () => plan };
  const result =
    action === 'install'
      ? runtime.deploy('codex', home, options)
      : runtime.verify('codex', home, options);
  return {
    ok: result.ok,
    action,
    home,
    sourceCommit: config.source.commit,
    changed: result.changed,
    verifiedFiles: result.checks?.length,
    plannedFiles: plan.writes.length,
  };
}

function compose(config, profileId, briefFile) {
  const root = sourceRoot(config);
  const profile = config.profiles.find((item) => item.id === profileId);
  if (!profile || !briefFile)
    throw new Error('compose requires a catalog profile ID and brief file');
  const brief = fs.readFileSync(assertWithin(ROOT, path.resolve(ROOT, briefFile)), 'utf8');
  const text = fs.readFileSync(path.join(ROOT, profile.path), 'utf8');
  const standards =
    profileId === 'coding'
      ? fs.readFileSync(path.join(ROOT, 'docs/CODE-STANDARDS.md'), 'utf8')
      : '';
  const input = `${text}\n${standards}\n\nTask brief:\n${brief}`;
  const executable = process.platform === 'win32' ? 'py' : 'python3';
  const prefix = process.platform === 'win32' ? ['-3.12'] : [];
  const result = spawnSync(
    executable,
    [
      ...prefix,
      path.join(root, 'coldbrew.py'),
      '--activate',
      '冷咖啡',
      '--profile',
      'MAX',
      '--json',
    ],
    {
      input,
      encoding: 'utf8',
      cwd: root,
      env: scopedEnvironment(),
      windowsHide: true,
      timeout: 30000,
      maxBuffer: 8 * 1024 * 1024,
    },
  );
  if (result.status !== 0)
    throw new Error('Original ColdCoffee composition failed; no provider request was made');
  const output = JSON.parse(result.stdout);
  if (!output.ok || typeof output.prompt !== 'string')
    throw new Error('Invalid composition output');
  return output.prompt;
}

function launch(config) {
  if (fs.existsSync(path.join(ROOT, 'jailbreak/local/INSTALL-BLOCKED.json'))) {
    throw new Error(
      'Installation is partial after Defender detection; complete T018 in a prepared environment before launching',
    );
  }
  const root = sourceRoot(config);
  const binary = require(path.join(root, 'desktop/node_modules/electron'));
  const local = path.join(ROOT, 'jailbreak/local');
  const child = spawn(
    binary,
    [
      path.join(root, 'desktop'),
      `--user-data-dir=${path.join(local, 'electron-user-data')}`,
      `--disk-cache-dir=${path.join(local, 'electron-cache')}`,
      `--toolbox-workspace=${path.join(local, 'toolbox')}`,
    ],
    {
      cwd: root,
      env: scopedEnvironment(),
      detached: true,
      stdio: 'ignore',
      windowsHide: true,
    },
  );
  child.on('error', (error) => {
    console.error(`ColdCoffee launch failed: ${error.message}`);
    process.exitCode = 1;
  });
  child.unref();
  return {
    startedPid: child.pid,
    dataDirectory: local,
    note: 'Process start is not UI acceptance',
  };
}

module.exports = { sourceRoot, seatAction, compose, launch };
