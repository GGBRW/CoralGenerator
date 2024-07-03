species = [
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

# function matchSpecies(str) {
#     return species.find(speciesName => {
#         return speciesName.toLowerCase().split(" ").every(name => str.toLowerCase().includes(name));
#     });
# }


file_path = 'Cnidaria_occurences.csv'

import pandas as pd

data = pd.read_csv(file_path, sep='\t')

#filter records, class should be Anthozoa or Hydrozoa
class_match = data['class'].apply(lambda x: x in ['Anthozoa', 'Hydrozoa'] if pd.notnull(x) else False)
filtered_data = data[class_match]


# print(filtered_data)
# print(len(filtered_data))

# species_count = filtered_data['species'].value_counts()
# species_count = species_count[species_count > 1000]

# # filter data by species that have 250 counts or more
# species_match = filtered_data['species'].apply(lambda x: x in species_count.index if pd.notnull(x) else False)
# species_filtered_data = filtered_data[species_match]

# species_match = data['species'].apply(lambda x: any([speciesName.lower() in x.lower() for speciesName in species]) if pd.notnull(x) else False)

# filtered_data = data[species_match]

# filter on where coordinateUncertaintyInMeters is less than 1000 and not null

# species_filtered_data = species_filtered_data[species_filtered_data['coordinateUncertaintyInMeters'] < 10]

# species should be not NaN
species_filtered_data = filtered_data[filtered_data['species'].notnull()]


species_filtered_data = species_filtered_data[['decimalLatitude', 'decimalLongitude', 'eventDate', 'class', 'order', 'family', 'genus', 'species']]
species_filtered_data.to_csv('GBIF_occurences_uncertain.csv', sep='\t', index=False)

print(species_filtered_data)