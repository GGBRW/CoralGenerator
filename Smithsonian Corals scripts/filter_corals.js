const fs = require('fs');

const metadata = JSON.parse(fs.readFileSync('smithsonian_corals_filtered.json'));

// check items where the GBIF canonicalName is different from the Smithsonian title
const mismatches = Object.values(metadata).filter(x => x.matchGBIF && x.matchGBIF.canonicalName !== x.title);
console.log(mismatches.map(x => [x.title, x.matchGBIF.canonicalName]))

// check items that are maybe not corals 
const notCorals = Object.values(metadata).filter(x => x.matchGBIF && x.matchGBIF.rank !== 'SPECIES');
console.log(notCorals.map(x => x.title));

// check items that do not belong to phyllum Cnidaria
const notCnidaria = Object.values(metadata).filter(x => x.matchGBIF && x.matchGBIF.phylum !== 'Cnidaria');
console.log(notCnidaria.map(x => x.title));

const metadata2 = [];
for (const key in metadata) {
    if(!key.includes('.zip')) {
        console.log(key, metadata[key].matchGBIF.canonicalName)

        const coral = {}
        coral.name = metadata[key].matchGBIF.canonicalName
        coral.GBIFData = metadata[key].matchGBIF;
        coral.SIData = metadata[key].metadata;
        coral.occurences = metadata[key].occurences;
        coral.filename = key;
        coral.filepath = 'smithsonian_corals/' + key;
        metadata2.push(coral);
        
    } else {
        console.log(key, metadata[key].matchGBIF.canonicalName)

        // get filename of .obj file inside folder 
        const folder = key.replace('.zip', '');
        const files = fs.readdirSync('smithsonian_corals/' + folder);
        const obj = files.find(x => x.endsWith('.obj'));
        
        const coral = {}
        coral.name = metadata[key].matchGBIF.canonicalName
        coral.GBIFData = metadata[key].matchGBIF;
        coral.SIData = metadata[key].metadata;
        coral.occurences = metadata[key].occurences;
        coral.filename = obj;
        coral.filepath = 'smithsonian_corals/' + folder + '/' + obj;
        metadata2.push(coral);


        // rename folder to canonicalName
        // fs.renameSync('smithsonian_corals/' + folder, 'smithsonian_corals/' + metadata[key].matchGBIF.canonicalName);
    }
}

// check if there are duplicate keys
const keys = Object.values(metadata).map(x => x.matchGBIF.canonicalName);
const duplicates = keys.filter((item, index) => keys.indexOf(item) != index);
console.log(duplicates);

// write metadata.json
fs.writeFileSync('smithsonian_corals_filtered2.json', JSON.stringify(metadata2));