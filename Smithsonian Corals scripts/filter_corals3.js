const fs = require('fs');
const path = require('path');

let catalog = JSON.parse(fs.readFileSync('CORALCATALOG.json'));

catalog = catalog.filter(x => !x.notes)

console.log(catalog.length);