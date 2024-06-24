const fs = require('fs');

const coralCatalog = JSON.parse(fs.readFileSync('coralCatalog.json'));

console.log(coralCatalog.map(x => x.name));

const notFoundInCoralTraits = [
    "Agaricia speciosa",
    "Astraea favistella",
    "Astraea pulchra",
    "Montastraea curta",
    "Crypthelia viridis",
    "Distichopora borealis",
    "Distichopora violacea",
    "Echinopora reflexa",
    "Gemmipora brassica",
    "Herpetolithus crassus",
    "Madrepora conigera",
    "Madrepora cuneata",
    "Madrepora cytherea",
    "Madrepora florida",
    "Acropora formosa",
    "Madrepora horrida",
    "Madrepora humilis",
    "Madrepora hyacinthus",
    "Madrepora robusta",
    "Madrepora spicifera",
    "Madrepora surculosa",
    "Madrepora valida",
    "Manopora caliculata",
    "Manopora capitata",
    "Manopora digitata",
    "Montipora lichen",
    "Manopora lichen",
    "Manopora nodosa",
    "Manopora scabricula",
    "Merulina rigida",
    "Merulina rigida",
    "Millepora alcicornis",
    "Astraea curta",
    "Pavonia decussata",
    "Pavonia praetorta",
    "Pocillopora damicornis caespitosa",
    "Pocillopora grandis",
    "Psammocora columna",
    "Scolymia australis",
    "Sideropora mordax",
    "Stylaster alaskanus",
    "Stylaster brochi",
    "Stylaster sanguineus",
    "Stylaster verrillii"
]

for(let name of notFoundInCoralTraits) {
    if(coralCatalog.find(x => x.name == name).occurrences > 500)
        console.log(name, coralCatalog.find(x => x.name == name).occurrences);
}

// total occurences
console.log(coralCatalog.reduce((acc, x) => acc + x.occurrences, 0));