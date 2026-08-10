#!/usr/bin/env node

const resolver = require('../../../workspace/scripts/resolve-squad-workspace-readiness.cjs');

if (require.main === module) {
  resolver.main();
}

module.exports = resolver;
