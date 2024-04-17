function getURL(scientificName) {
    scientificName = encodeURIComponent(scientificName);
    return `https://api.gbif.org/v1/species/match?name=${scientificName}`;
}

function getMatch(scientificName, callback) {
    const url = getURL(scientificName);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(scientificName, data);
            callback(data);
        });
}


// read metadata.json
const fs = require('fs');
const metadata = JSON.parse(fs.readFileSync('../Smithsonian Corals scripts/smithsonian_corals.json'));

for(const key in metadata) {
    getMatch(metadata[key].title, x => metadata[key].matchGBIF = x);
}

setTimeout(() => {
    // write metadata.json
    fs.writeFileSync('smithsonian_corals.json', JSON.stringify(metadata));
}, 5000)

