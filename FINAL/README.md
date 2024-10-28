## Usage
To run the `generate_coral_reef.py` script from the terminal using Blender, use the following command (adjust the path to the Blender application as necessary):

```
/Applications/Blender.app/Contents/MacOS/blender --background --python generate_coral_reef.py
```

This script generates a coral reef model by distributing coral colonies. It uses `generate_spatial_distribution.py` as a module to calculate and apply the spatial distribution of coral species.

If `calculate_spatial_distribution` (at line 26) is set to False, the script accepts a file path (`spatial_distribution_file` at line 27) to a JSON file that contains a static spatial distribution.



## Generating species abundance data

The `generate_species_abundance.py` script is responsible for generating the species abundance data for the coral reef model. To generate this data as a JSON file, run the following:

```
python generate_species_abundance.py [geomorphic_zones_folder_path] 
```

