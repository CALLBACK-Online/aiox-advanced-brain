#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const required = [
  "config.yaml",
  "data/token-registry.yaml",
  "workflows/generate-presentation.yaml",
  "templates/handoff-template.md",
];

const missing = required.filter((item) => !fs.existsSync(path.join(root, item)));
if (missing.length > 0) {
  console.error(`Missing slides-creator contract files: ${missing.join(", ")}`);
  process.exit(1);
}

console.log("slides-creator contract smoke passed");
