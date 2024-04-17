const fs = require('fs');

const metadata = JSON.parse(fs.readFileSync('smithsonian_corals_filtered.json'));

console.log(
    Object.values(metadata).filter(x => x.title != x.matchGBIF.canonicalName).map(x => [x.title, x.matchGBIF.canonicalName])

)