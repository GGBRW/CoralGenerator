function getURL(scientificName) {
    scientificName = encodeURIComponent(scientificName);
    return `https://api.gbif.org/v1/occurrence/search?scientificName=${scientificName}`;
}

function getOccurrences(scientificName, callback) {
    const url = getURL(scientificName);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(scientificName, data.count);
            callback(data.count);
        });
}


// read metadata.json
const fs = require('fs');
const metadata = JSON.parse(fs.readFileSync('../Smithsonian Corals scripts/coral_catalog.json'));

for(let coral of metadata) {
    getOccurrences(coral.GBIFData.canonicalName, x => {
        const GBIFData = coral.GBIFData;
        delete coral.GBIFData;
        const SIData = coral.SIData;
        delete coral.SIData;
        coral.occurrences = x;
        coral.GBIFData = GBIFData;
        coral.SIData = SIData;
    });

}

setTimeout(() => {
    // write metadata.json
    fs.writeFileSync('smithsonian_corals.json', JSON.stringify(metadata));
}, 5000)

