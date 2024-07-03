import pandas as pd

OBIS_data = pd.read_csv('OBIS_occurences.csv', sep=',')
OBIS_data = OBIS_data[OBIS_data['class'].apply(lambda x: x in ['Anthozoa', 'Hydrozoa'] if pd.notnull(x) else False)]
OBIS_data.dropna(subset=['species'], inplace=True)

GBIF_data = pd.read_csv('GBIF_occurences.csv', sep='\t')
GBIF_data = GBIF_data[GBIF_data['class'].apply(lambda x: x in ['Anthozoa', 'Hydrozoa'] if pd.notnull(x) else False)]
GBIF_data.dropna(subset=['species'], inplace=True)

print("OBIS data: ", len(OBIS_data), "GBIF data: ", len(GBIF_data))

print("OBIS data: ", OBIS_data['species'].isnull().sum(), "GBIF data: ", GBIF_data['species'].isnull().sum(), " missing species value")
print("OBIS data: ", OBIS_data['scientificname'].isnull().sum(), "GBIF data: ", GBIF_data['scientificName'].isnull().sum(), " missing species value")

OBIS_data.rename(columns={'decimallatitude': 'decimalLatitude', 'decimallongitude': 'decimalLongitude', 'coordinateuncertaintyinmeters': 'coordinateUncertaintyInMeters'}, inplace=True)

OBIS_data = OBIS_data[['species', 'phylum', 'class', 'order', 'family', 'genus', 'decimalLatitude', 'decimalLongitude', 'coordinateUncertaintyInMeters', 'eventdate']]
GBIF_data = GBIF_data[['species', 'phylum', 'class', 'order', 'family', 'genus', 'decimalLatitude', 'decimalLongitude', 'coordinateUncertaintyInMeters', 'eventDate']]

# see how many duplicated are in GBIF on 'species'
print(len(GBIF_data[GBIF_data.duplicated(subset=['decimalLatitude', 'decimalLongitude', 'species', 'eventDate'])]))
print(len(OBIS_data[OBIS_data.duplicated(subset=['decimalLatitude', 'decimalLongitude', 'species', 'eventdate'])]))

data = pd.concat([OBIS_data, GBIF_data])

# # Identify and remove duplicates based on 'decimalLatitude' and 'decimalLongitude'
# data_cleaned = data.drop_duplicates(subset=['decimalLatitude', 'decimalLongitude', 'species'])

# print(data_cleaned)
data.to_csv('combined_occurences.csv', sep='\t', index=False)