// read coral_catalog.json
const fs = require('fs');
const path = require('path');

let catalog = JSON.parse(fs.readFileSync('CORALCATALOG.json'));

catalog = catalog.filter(x => !x.notes)

// detect duplicates and report how many times eeach duplicate occurs
let duplicates = {};
for (let coral of catalog) {
    if (duplicates[coral.name]) {
        duplicates[coral.name]++;
    } else {
        duplicates[coral.name] = 1;
    }
}
for (let name in duplicates) {
    if (duplicates[name] > 1) {
        console.log(name, duplicates[name]);
    }
}

console.log(Object.keys(duplicates).length);

// leave 1 of each duplicate
let uniqueCatalog = [];
for (let coral of catalog) {
    if (duplicates[coral.name] > 1) {
        duplicates[coral.name]--;
    } else {
        uniqueCatalog.push(coral);
    }
}

catalog = uniqueCatalog;

// total occurrences
let totalOccurrences = 0;
for (let coral of catalog) {
    totalOccurrences += coral.occurrences;
}
console.log(totalOccurrences);

for (let coral of catalog) {
    coral.popularity = coral.occurrences / totalOccurrences;
}


// sort by popularity
catalog.sort((a, b) => b.popularity - a.popularity);
console.log(catalog.slice(0, 10).map(x => [x.name, x.popularity]));


// Ensure the destination directory exists
const destFolder = 'filtered_corals';
if (!fs.existsSync(destFolder)) {
    fs.mkdirSync(destFolder, { recursive: true });
}
for (let coral of catalog) {
    const filepath = coral.filepath.split('/').slice(0,-1).join('/');
    const folder = filepath.replace('smithsonian_corals/', '');

    // copy folder to filtered_corals
    const dest = path.join(destFolder, folder);

    
}