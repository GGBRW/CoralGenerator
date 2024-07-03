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

const growthForms = {
    "Acropora aspera": "branching_open",
    "Acropora cervicornis": "branching_open",
    "Acropora digitifera": "digitate",
    "Acropora palmata": "branching_open",
    "Acropora prolifera": "branching_closed",
    "Acropora secale": "branching_closed",
    "Acropora tenuis": "corymbose",
    "Acropora valenciennesi": "branching_open",
    "Diploastrea heliopora": "massive",
    "Diploria labyrinthiformis": "massive",
    "Favia fragum": "massive",
    "Goniastrea favulus": "massive",
    "Goniopora columna": "columnar",
    "Heliopora coerulea": "massive",
    "Leptoseris cailleti": "laminar",
    "Leptoseris cucullata": "laminar",
    "Leptoseris gardineri": "laminar",
    "Meandrina meandrites": "submassive",
    "Montipora danae": "laminar",
    "Pleurocorallium niveum": "arborescent",
    "Pocillopora damicornis": "branching_closed",
    "Pocillopora meandrina": "branching_closed",
    "Pocillopora molokensis": "branching_closed",
    "Porites lobata": "massive",
    "Porites monticulosa": "encrusting",
    "Pseudodiploria strigosa": "massive",
    "Seriatopora hystrix": "branching_closed",
    "Tubipora musica": "massive"
}

const growthFormsOBIS = {
    "Acropora abrotanoides": "branching_open",
    "Acropora aculeus": "corymbose",
    "Acropora aspera": "branching_open",
    "Acropora austera": "branching_open",
    "Acropora cerealis": "corymbose",
    "Acropora cervicornis": "branching_open",
    "Acropora cytherea": "tables_or_plates",
    "Acropora digitifera": "digitate",
    "Acropora divaricata": "tables_or_plates",
    "Acropora elseyi": "hispidose",
    "Acropora florida": "branching_open",
    "Acropora gemmifera": "digitate",
    "Acropora humilis": "digitate",
    "Acropora hyacinthus": "tables_or_plates",
    "Acropora intermedia": "branching_open",
    "Acropora latistella": "corymbose",
    "Acropora loripes": "corymbose",
    "Acropora lutkeni": "branching_open",
    "Acropora microphthalma": "branching_open",
    "Acropora millepora": "corymbose",
    "Acropora muricata": "branching_open",
    "Acropora nasuta": "corymbose",
    "Acropora palmata": "branching_open",
    "Acropora pulchra": "branching_open",
    "Acropora robusta": "branching_open",
    "Acropora samoensis": "digitate",
    "Acropora secale": "branching_closed",
    "Acropora selago": "corymbose",
    "Acropora solitaryensis": "tables_or_plates",
    "Acropora tenuis": "corymbose",
    "Acropora valida": "corymbose",
    "Agaricia agaricites": "laminar",
    "Agaricia fragilis": "encrusting",
    "Agaricia humilis": "encrusting",
    "Agaricia lamarcki": "laminar",
    "Agaricia tenuifolia": "laminar",
    "Astrea curta": "massive",
    "Astreopora myriophthalma": "massive",
    "Coelastrea aspera": "massive",
    "Colpophyllia natans": "massive",
    "Cyphastrea microphthalma": "massive",
    "Cyphastrea serailia": "massive",
    "Desmophyllum dianthus": "Element not found",
    "Diploastrea heliopora": "massive",
    "Diploria labyrinthiformis": "massive",
    "Dipsastraea favus": "massive",
    "Dipsastraea matthaii": "massive",
    "Dipsastraea pallida": "massive",
    "Dipsastraea speciosa": "massive",
    "Echinophyllia aspera": "laminar",
    "Echinopora lamellosa": "laminar",
    "Enallopsammia rostrata": "Element not found",
    "Eusmilia fastigiata": "massive",
    "Favia fragum": "massive",
    "Favia gravida": "massive",
    "Favites abdita": "massive",
    "Favites pentagona": "submassive",
    "Fungia fungites": "massive",
    "Galaxea fascicularis": "massive",
    "Goniastrea edwardsi": "massive",
    "Goniastrea pectinata": "submassive",
    "Goniastrea retiformis": "massive",
    "Goniastrea stelligera": "massive",
    "Goniocorella dumosa": "Element not found",
    "Helioseris cucullata": "laminar",
    "Hydnophora exesa": "submassive",
    "Isopora palifera": "branching_open",
    "Leptastrea purpurea": "encrusting",
    "Leptopsammia pruvoti": "Element not found",
    "Leptoria phrygia": "massive",
    "Leptoseris mycetoseroides": "laminar",
    "Lobactis scutaria": "massive",
    "Lobophyllia hemprichii": "massive",
    "Madracis decactis": "digitate",
    "Madracis myriaster": "Element not found",
    "Madrepora oculata": "Element not found",
    "Meandrina meandrites": "submassive",
    "Merulina ampliata": "laminar",
    "Montastraea cavernosa": "massive",
    "Montipora aequituberculata": "laminar",
    "Montipora capitata": "encrusting_long_uprights",
    "Montipora foveolata": "massive",
    "Montipora verrucosa": "laminar",
    "Mycedium elephantotus": "laminar",
    "Oculina varicosa": "branching_closed",
    "Orbicella annularis": "massive",
    "Orbicella faveolata": "massive",
    "Orbicella franksi": "massive",
    "Oxypora lacera": "laminar",
    "Pachyseris speciosa": "laminar",
    "Paragoniastrea australensis": "submassive",
    "Pavona clavus": "columnar",
    "Pavona duerdeni": "massive",
    "Pavona gigantea": "massive",
    "Pavona maldivensis": "columnar",
    "Pavona varians": "encrusting",
    "Platygyra daedalea": "massive",
    "Platygyra lamellina": "massive",
    "Platygyra pini": "massive",
    "Platygyra sinensis": "massive",
    "Plesiastrea versipora": "massive",
    "Pocillopora meandrina": "branching_closed",
    "Pocillopora verrucosa": "branching_closed",
    "Porites astreoides": "massive",
    "Porites cylindrica": "encrusting_long_uprights",
    "Porites divaricata": "branching_closed",
    "Porites evermanni": "columnar",
    "Porites furcata": "branching_closed",
    "Porites lichen": "laminar",
    "Porites lobata": "massive",
    "Porites lutea": "massive",
    "Porites porites": "branching_closed",
    "Porites rus": "digitate",
    "Porites vaughani": "encrusting",
    "Psammocora haimiana": "submassive",
    "Pseudodiploria clivosa": "massive",
    "Pseudodiploria strigosa": "massive",
    "Seriatopora hystrix": "branching_closed",
    "Siderastrea radians": "massive",
    "Siderastrea siderea": "massive",
    "Solenosmilia variabilis": "Element not found",
    "Stephanocoenia intersepta": "massive",
    "Stylophora pistillata": "branching_closed",
    "Tubastraea coccinea": "Element not found",
    "Turbinaria mesenterina": "laminar",
    "Turbinaria reniformis": "laminar"
}

const fs = require('fs');

function matchSpecies(str) {
    return species.find(speciesName => {
        return speciesName.toLowerCase().split(" ").every(name => str.toLowerCase().includes(name));
    });
}


const file = fs.readFileSync('Northern-Caribbean--Florida---Bahamas-20230310014129_species_count_GBIF_uncertain.json', 'utf8');
const data = JSON.parse(file);

// for(let i in data) {
//     const zone = data[i];

//     const species = Object.keys(zone);
//     for(let j in species) {
//         const match = matchSpecies(species[j]);
//         if(!match) {
//             delete zone[species[j]];
//         } 
//     }
// }

const zone_gf = {}

for(let zone in data) {
    zone_gf[zone] = {};
    for(let species in data[zone]) {
        const growthForm = growthForms[species] || growthFormsOBIS[species] || "unknown";
        if(!zone_gf[zone][growthForm]) {
            zone_gf[zone][growthForm] = 0;
        }
        zone_gf[zone][growthForm] += data[zone][species];
    }
}

let tototal = 0;
for(let zone in zone_gf) {
    const total = Object.values(zone_gf[zone]).reduce((acc, curr) => acc + curr, 0);
    tototal += total;
}
for(let zone in zone_gf) {
    const total = Object.values(zone_gf[zone]).reduce((acc, curr) => acc + curr, 0);
    console.log("Zone: " + zone + ": " + Math.round(total / tototal * 100) + "%");
}

// turn it into percentages for each zone
for(let zone in zone_gf) {
    const total = Object.values(zone_gf[zone]).reduce((acc, curr) => acc + curr, 0);
    for(let gf in zone_gf[zone]) {
        zone_gf[zone][gf] = zone_gf[zone][gf] / total * 100;
    }
}

console.log(zone_gf);
