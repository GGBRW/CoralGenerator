const species = [
    'Acropora cervicornis',
    'Acropora cervicornis',
    'Acropora digitifera',
    'Acropora palmata',
    'Acropora prolifera',
    'Acropora secale',
    'Acropora valenciennesi',
    'Agaricia speciosa',
    'Astraea favistella',
    'Astraea pulchra',
    'Montastraea curta',
    'Pleurocorallium niveum',
    'Crypthelia viridis',
    'Diploastrea heliopora',
    'Diploria labyrinthiformis',
    'Distichopora borealis',
    'Distichopora violacea',
    'Echinopora reflexa',
    'Favia fragum',
    'Gemmipora brassica',
    'Goniastrea favulus',
    'Goniastrea favulus',
    'Goniopora columna',
    'Heliopora coerulea',
    'Heliopora coerulea',
    'Herpetolithus crassus',
    'Leptoseris cailleti',
    'Leptoseris cucullata',
    'Leptoseris gardineri',
    'Acropora aspera',
    'Madrepora conigera',
    'Madrepora cuneata',
    'Madrepora cytherea',
    'Madrepora florida',
    'Acropora formosa',
    'Madrepora horrida',
    'Madrepora humilis',
    'Madrepora hyacinthus',
    'Madrepora robusta',
    'Madrepora spicifera',
    'Madrepora surculosa',
    'Acropora tenuis',
    'Madrepora valida',
    'Manopora caliculata',
    'Manopora capitata',
    'Manopora digitata',
    'Montipora lichen',
    'Manopora lichen',
    'Manopora nodosa',
    'Manopora scabricula',
    'Meandrina meandrites',
    'Merulina rigida',
    'Merulina rigida',
    'Millepora alcicornis',
    'Montipora danae',
    'Astraea curta',
    'Pavonia decussata',
    'Pavonia praetorta',
    'Pocillopora damicornis',
    'Pocillopora damicornis caespitosa',
    'Pocillopora damicornis',
    'Pocillopora damicornis',
    'Pocillopora damicornis',
    'Pocillopora grandis',
    'Pocillopora meandrina',
    'Pocillopora molokensis',
    'Pocillopora molokensis',
    'Porites lobata',
    'Porites monticulosa',
    'Psammocora columna',
    'Pseudodiploria strigosa',
    'Scolymia australis',
    'Sideropora mordax',
    'Stylaster alaskanus',
    'Stylaster brochi',
    'Stylaster sanguineus',
    'Stylaster verrillii',
    'Tubipora musica',
    'Seriatopora hystrix'
  ]

const fs = require('fs');

function matchSpecies(str) {
    return species.find(speciesName => {
        return speciesName.toLowerCase().split(" ").every(name => str.toLowerCase().includes(name));
    });
}

const data = JSON.parse(fs.readFileSync('allPatches.json', 'utf8'));

const coOccurrences = {};

for(let source in data) {
    const images = {};
    for(let species in data[source]) {
        const occurences = data[source][species];
        for(let occ of occurences) {
            const image = occ.split(':')[1].trim();
            if(!images[image]) images[image] = [];
            images[image].push(species);
        }
    }

    for(let image in images) {
        for(let i = 0; i < images[image].length; ++i) {
            for(let j = i; j < images[image].length; ++j) {
                const species1 = matchSpecies(images[image][i]);
                const species2 = matchSpecies(images[image][j]);
                if(species1 === species2) continue; 
                const key = species1 < species2 ? species1 + '; ' + species2 : species2 + '; ' + species1;

                if(!coOccurrences[key]) coOccurrences[key] = { count: 0, image, source };
                coOccurrences[key].count++;
            }
        }
    }
}

console.log("found " + Object.keys(coOccurrences).length + " co-occurrences.");
// write to file

fs.writeFileSync('coOccurrences.json', JSON.stringify(coOccurrences, null, 2));
