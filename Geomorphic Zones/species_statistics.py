import pandas as pd

import os
import glob
import json

gf = {
    "Acanthoprimnoa goesi": "Element not found",
    "Acropora cervicornis": "branching_open",
    "Acropora muricata": "branching_open",
    "Acropora palmata": "branching_open",
    "Acropora prolifera": "branching_closed",
    "Agaricia agaricites": "laminar",
    "Agaricia fragilis": "encrusting",
    "Agaricia grahamae": "laminar",
    "Agaricia humilis": "encrusting",
    "Agaricia lamarcki": "laminar",
    "Agaricia tenuifolia": "laminar",
    "Agaricia undata": "laminar",
    "Anomocora prolifera": "Element not found",
    "Antillogorgia acerosa": "Element not found",
    "Antillogorgia americana": "Element not found",
    "Antillogorgia bipinnata": "Element not found",
    "Antillogorgia blanquillensis": "Element not found",
    "Antillogorgia elisabethae": "Element not found",
    "Antillogorgia kallos": "Element not found",
    "Antillogorgia rigida": "Element not found",
    "Astrangia poculata": "submassive",
    "Balanophyllia floridana": "Element not found",
    "Bathypsammia tintinnabulum": "Element not found",
    "Bebryce cinerea": "Element not found",
    "Briareum asbestinum": "Element not found",
    "Carijoa riisei": "Element not found",
    "Chrysogorgia elegans": "Element not found",
    "Chrysogorgia multiflora": "Element not found",
    "Chrysogorgia thyrsiformis": "Element not found",
    "Cladocora arbuscula": "branching_closed",
    "Cladocora debilis": "Element not found",
    "Cladopsammia manuelensis": "Element not found",
    "Colangia immersa": "Element not found",
    "Colpophyllia amaranthus": "Element not found",
    "Colpophyllia breviserialis": "Element not found",
    "Colpophyllia natans": "massive",
    "Dasmosmilia lymani": "Element not found",
    "Dasmosmilia variegata": "Element not found",
    "Deltocyathoides stimpsonii": "Element not found",
    "Deltocyathus agassizi": "Element not found",
    "Deltocyathus andamanicus": "Element not found",
    "Deltocyathus calcar": "Element not found",
    "Dendrogyra cylindrus": "columnar",
    "Diploria labyrinthiformis": "massive",
    "Eguchipsammia cornucopia": "Element not found",
    "Ellisella elongata": "Element not found",
    "Enallopsammia profunda": "Element not found",
    "Enallopsammia rostrata": "Element not found",
    "Erythropodium caribaeorum": "Element not found",
    "Eunicea calyculata": "Element not found",
    "Eunicea clavigera": "Element not found",
    "Eunicea flexuosa": "Element not found",
    "Eunicea fusca": "Element not found",
    "Eunicea knighti": "Element not found",
    "Eunicea laciniata": "Element not found",
    "Eunicea mammosa": "Element not found",
    "Eunicea palmeri": "Element not found",
    "Eunicea pinta": "Element not found",
    "Eunicea succinea": "Element not found",
    "Eunicea tourneforti": "Element not found",
    "Eunicella verrucosa": "Element not found",
    "Eusmilia fastigiata": "massive",
    "Favia fragum": "massive",
    "Favia gravida": "massive",
    "Flabellum floridanum": "Element not found",
    "Gardineroseris planulata": "massive",
    "Gorgonia flabellum": "Element not found",
    "Gorgonia mariae": "Element not found",
    "Gorgonia ventalina": "Element not found",
    "Helioseris cucullata": "laminar",
    "Iciligorgia schrammi": "Element not found",
    "Isophyllia rigida": "massive",
    "Isophyllia sinuosa": "massive",
    "Keratoisis flexibilis": "Element not found",
    "Leptogorgia cardinalis": "Element not found",
    "Leptogorgia hebes": "Element not found",
    "Leptogorgia punicea": "Element not found",
    "Leptoseris gardineri": "laminar",
    "Leptoseris glabra": "laminar",
    "Madracis asperula": "branching_closed",
    "Madracis auretenra": "branching_closed",
    "Madracis carmabi": "branching_closed",
    "Madracis decactis": "digitate",
    "Madracis formosa": "columnar",
    "Madracis myriaster": "Element not found",
    "Madracis pharensis": "digitate",
    "Madrepora oculata": "Element not found",
    "Manicina areolata": "massive",
    "Meandrina meandrites": "submassive",
    "Montastraea cavernosa": "massive",
    "Muricea atlantica": "Element not found",
    "Muricea elongata": "Element not found",
    "Muricea laxa": "Element not found",
    "Muricea muricata": "Element not found",
    "Muricea pinnata": "Element not found",
    "Muriceopsis flavida": "Element not found",
    "Muriceopsis petila": "Element not found",
    "Mussa angulosa": "massive",
    "Mycetophyllia aliciae": "massive",
    "Mycetophyllia danaana": "encrusting",
    "Mycetophyllia ferox": "laminar",
    "Mycetophyllia lamarckiana": "encrusting",
    "Mycetophyllia reesi": "laminar",
    "Nicella deichmannae": "Element not found",
    "Nicella goreaui": "Element not found",
    "Oculina diffusa": "branching_closed",
    "Oculina robusta": "branching_open",
    "Oculina tenella": "Element not found",
    "Orbicella annularis": "massive",
    "Orbicella faveolata": "massive",
    "Orbicella franksi": "massive",
    "Paracyathus pulchellus": "Element not found",
    "Phacelocyathus flos": "Element not found",
    "Plexaura homomalla": "Element not found",
    "Plexaura kuekenthali": "Element not found",
    "Plexaurella dichotoma": "Element not found",
    "Plexaurella grisea": "Element not found",
    "Plexaurella nutans": "Element not found",
    "Pocillopora capitata": "branching_open",
    "Polymyces fragilis": "Element not found",
    "Porites astreoides": "massive",
    "Porites branneri": "digitate",
    "Porites colonensis": "laminar",
    "Porites divaricata": "branching_closed",
    "Porites furcata": "branching_closed",
    "Porites porites": "branching_closed",
    "Pseudodiploria clivosa": "massive",
    "Pseudodiploria strigosa": "massive",
    "Pseudoplexaura flagellosa": "Element not found",
    "Pseudoplexaura porosa": "Element not found",
    "Pseudoplexaura tenuis": "Element not found",
    "Pseudoplexaura wagenaari": "Element not found",
    "Pterogorgia anceps": "Element not found",
    "Pterogorgia citrina": "Element not found",
    "Pterogorgia guadalupensis": "Element not found",
    "Renilla reniformis": "Element not found",
    "Rhizosmilia maculata": "Element not found",
    "Scolymia cubensis": "massive",
    "Scolymia lacera": "massive",
    "Siderastrea radians": "massive",
    "Siderastrea siderea": "massive",
    "Solenastrea bournoni": "massive",
    "Solenastrea hyades": "submassive",
    "Stenocyathus vermiformis": "Element not found",
    "Stephanocoenia intersepta": "massive",
    "Swiftia exserta": "Element not found",
    "Telesto sanguinea": "Element not found",
    "Thalamophyllia riisei": "Element not found",
    "Tubastraea coccinea": "Element not found",
    "Tubastraea tagusensis": "Element not found",
    "Umbellula durissima": "Element not found"
}

# get all csv files in 'results/' directory
files = glob.glob('results/*.json')
 
for file_path in files:
    print("----", file_path, "----")
    data = json.load(open(file_path))

    if 'species' in file_path and file_path.endswith('uncertain.json'):
        # for each zone, output the top 3 species
        for zone, species in data.items():
            sorted_species = sorted(species.items(), key=lambda x: x[1], reverse=True)

            print(zone, sorted_species[:3])

        # for each zone, calculate the percentage of occurences of the total occurences
        total = 0
        total_species = 0
        species_d = []
        for zone, species in data.items():
            total += sum(species.values())
            total_species += len(species)
            species_d.extend(list(species.keys()))

        print(f"Total occurences: {total}, {total_species} different species")
        # print(species_d)

        for zone, species in data.items():
            print(f"{zone}: {sum(species.values()) / total * 100:.2f}% of total occurences")
    # if 'species' in file_path and file_path.endswith('certain100.json'):
    #     # for each zone, output the top 3 species
    #     for zone, species in data.items():
    #         sorted_species = sorted(species.items(), key=lambda x: x[1], reverse=True)
    #         print(zone, sorted_species[:3])
    # if 'species' in file_path and file_path.endswith('certain10.json'):
    #     # for each zone, output the top 3 species
    #     for zone, species in data.items():
    #         sorted_species = sorted(species.items(), key=lambda x: x[1], reverse=True)
    #         print(zone, sorted_species[:3])

    if 'zones' in file_path:
        # count the total of zones with '&' occuring two times in the name
        # sort keys by value
        # data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
        # for zone in data:
        #     print(f"{zone}: {data[zone] / 100000 * 100:.2f}%")

        two_zones = 0
        more_zones = 0
        for zone in data:
            if zone.count('&') == 1:
                two_zones += data[zone]
            elif zone.count('&') > 1:
                more_zones += data[zone]
        
        print(f"Rectangles overlapping two zones: {two_zones / 100000 * 100:.2f}%")
        print(f"Rectangles overlapping three or more zones: {more_zones / 100000 * 100:.2f}%")
