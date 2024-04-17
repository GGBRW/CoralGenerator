const fs = require('fs');
const path = require('path');  // Include the path module for path operations

// read coral_catalog.json
const catalog = JSON.parse(fs.readFileSync('CORALCATALOG.json'));

console.log(catalog.filter(x => !x.notes).map(x => x.filepath.replace('smithsonian_corals/', '')))

const filtered = catalog.map(x => x.filepath.replace('smithsonian_corals/', '').split('/').slice(0,-1).join('/'));

// list all folder names in filtered_corals 
const folderNames = [...fs.readdirSync('filtered_corals')];

console.log(folderNames.length + " folders in filtered_corals");
console.log(folderNames.filter(x => !filtered.includes(x)));