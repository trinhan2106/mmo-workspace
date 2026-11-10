'use strict';

const { catalog } = require('./bypass/paths.cjs');
const upstream = require('./bypass/upstream.cjs');

try {
  const [action = 'check', profile, brief] = process.argv.slice(2);
  const config = catalog();
  let result;
  if (action === 'check') {
    result = { ok: true, name: config.name, profiles: config.profiles.map((item) => item.id) };
  } else if (['preview', 'install', 'verify'].includes(action)) {
    result = upstream.seatAction(config, action);
    if (!result.ok) process.exitCode = 1;
  } else if (action === 'compose') {
    process.stdout.write(upstream.compose(config, profile, brief));
  } else if (action === 'launch') {
    result = upstream.launch(config);
  } else {
    throw new Error(
      'Usage: bypass.cjs check|preview|install|verify|compose <profile> <brief>|launch',
    );
  }
  if (result) console.log(JSON.stringify(result, null, 2));
} catch (error) {
  console.error(`byPass: ${error.message}`);
  process.exitCode = 1;
}
