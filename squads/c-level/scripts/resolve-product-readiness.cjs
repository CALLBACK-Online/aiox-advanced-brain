#!/usr/bin/env node

const resolver = require('../../../workspace/scripts/resolve-product-readiness.cjs');

if (require.main === module) {
  resolver.main();
}

module.exports = resolver;
