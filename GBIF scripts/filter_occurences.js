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


const file = fs.readFileSync('Cnidaria_occurences.csv', 'utf8');
// read csv file
const data = file.split('\n').map(x => x.split('\t'));

const filtered_data = data.filter(x => matchSpecies(x.name));

console.log(filtered_data.length);
