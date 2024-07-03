import json
import matplotlib.pyplot as plt
import numpy as np

# Sample JSON data
data = {
  'Deep Lagoon': {
    "encrusting_long_uprights": 0.9103078982597055,
    "branching_closed": 12.797858099062918,
    "laminar": 5.327978580990629,
    "unknown": 1.7670682730923692,
    "submassive": 2.436412315930388,
    "digitate": 5.836680053547524,
    "tables_or_plates": 9.424364123159304,
    "corymbose": 31.298527443105755,
    "branching_open": 14.484605087014726,
    "massive": 13.065595716198125,
    "hispidose": 1.3654618473895583,
    "encrusting": 1.285140562248996
  },
  'Reef Slope': {
    "massive": 20.09446114212108,
    "corymbose": 19.06397595534564,
    "branching_closed": 12.58050665521683,
    "digitate": 9.53198797767282,
    "tables_or_plates": 7.85744954916273,
    "branching_open": 10.347788750536711,
    "submassive": 3.9501932159725204,
    "encrusting": 3.3490768570201808,
    "laminar": 9.10261914984972,
    "unknown": 2.31859167024474,
    "encrusting_long_uprights": 0.9875483039931301,
    "hispidose": 0.7728638900815801,
    "columnar": 0.042936882782310004
  },
  'Back Reef Slope': {
    "laminar": 12.350163458045769,
    "digitate": 6.24772974936433,
    "corymbose": 15.001816200508536,
    "branching_closed": 11.58735924446059,
    "massive": 24.446058844896477,
    "unknown": 3.051216854340719,
    "tables_or_plates": 7.01053396294951,
    "branching_open": 8.209226298583364,
    "encrusting": 2.8332727933163824,
    "encrusting_long_uprights": 1.3076643661460225,
    "submassive": 6.610969851071559,
    "hispidose": 1.3439883763167455
  },
  'Outer Reef Flat': {
    "unknown": 3.1423583558165373,
    "branching_closed": 10.268211395016664,
    "branching_open": 11.268052690049199,
    "laminar": 10.680844310426917,
    "massive": 20.361847325821298,
    "corymbose": 20.076178384383432,
    "digitate": 6.681479130296779,
    "submassive": 4.5707030630058725,
    "tables_or_plates": 6.871925091255355,
    "encrusting_long_uprights": 1.602920171401365,
    "encrusting": 2.555149976194255,
    "columnar": 0.22218695445167433,
    "hispidose": 1.6981431518806538
  },
  'Terrestrial Reef Flat': {
    "branching_closed": 8.717221828490432,
    "unknown": 4.323175053153792,
    "digitate": 3.7562012756909993,
    "laminar": 15.024805102763997,
    "corymbose": 13.394755492558469,
    "massive": 26.0099220411056,
    "submassive": 8.008504606661942,
    "encrusting": 3.6853295535081503,
    "columnar": 0.4961020552799433,
    "branching_open": 8.788093550673281,
    "encrusting_long_uprights": 1.4174344436569808,
    "hispidose": 1.4174344436569808,
    "tables_or_plates": 4.961020552799433
  },
  'Inner Reef Flat': {
    "unknown": 3.7009063444108756,
    "digitate": 6.268882175226587,
    "branching_closed": 11.178247734138973,
    "encrusting_long_uprights": 1.1329305135951662,
    "laminar": 8.685800604229607,
    "hispidose": 1.2084592145015105,
    "tables_or_plates": 6.873111782477341,
    "submassive": 2.56797583081571,
    "massive": 15.030211480362537,
    "encrusting": 1.8882175226586102,
    "branching_open": 14.350453172205437,
    "corymbose": 26.963746223564954,
    "columnar": 0.1510574018126888
  },
  'Reef Crest': {
    "massive": 21.099744245524295,
    "branching_closed": 16.240409207161125,
    "laminar": 11.12531969309463,
    "digitate": 6.649616368286446,
    "branching_open": 10.485933503836318,
    "corymbose": 16.879795396419436,
    "encrusting": 2.4296675191815855,
    "unknown": 2.1739130434782608,
    "Element not found": 0.7672634271099744,
    "tables_or_plates": 7.161125319693094,
    "submassive": 3.9641943734015346,
    "hispidose": 0.3836317135549872,
    "encrusting_long_uprights": 0.3836317135549872,
    "columnar": 0.2557544757033248
  },
  'Shallow Lagoon': {
    "submassive": 5.299539170506913,
    "massive": 15.668202764976957,
    "encrusting": 4.147465437788019,
    "branching_closed": 12.211981566820276,
    "laminar": 8.755760368663594,
    "corymbose": 16.359447004608295,
    "branching_open": 9.90783410138249,
    "digitate": 14.746543778801843,
    "tables_or_plates": 6.682027649769585,
    "unknown": 4.838709677419355,
    'Element not found': 0.2304147465437788,
    "encrusting_long_uprights": 1.1520737327188941
  },
  'Sheltered Reef Slope': {
    "massive": 24.537905170104473,
    "laminar": 9.93838735601393,
    "corymbose": 17.572997589070454,
    "unknown": 2.009107956067506,
    "encrusting": 1.8215912135012053,
    "submassive": 5.732654701312617,
    "branching_closed": 12.161800160728637,
    "encrusting_long_uprights": 1.741226895258505,
    "tables_or_plates": 6.188052504687919,
    "branching_open": 10.44736137155103,
    "digitate": 6.3755692472542185,
    "hispidose": 1.3929815162068042,
    "columnar": 0.08036431824270024
  },
  "Plateau": {
    "corymbose": 14.478381594605317,
    "laminar": 15.866719555731853,
    "unknown": 4.244347481158271,
    "submassive": 7.616025386751289,
    "massive": 25.14875049583499,
    "columnar": 0.19833399444664812,
    "tables_or_plates": 4.799682665608886,
    "branching_open": 8.409361364537881,
    "encrusting": 2.499008330027767,
    "branching_closed": 9.282030940103134,
    "digitate": 4.125347084490281,
    "hispidose": 1.6263387544625147,
    "encrusting_long_uprights": 1.705672352241174
  }
}

# Process the data
zones = list(data.keys())
forms = list(set(form for zone in data.values() for form in zone.keys()))

# Sort forms for consistency
forms.sort()

# Initialize data matrix for the plot
values = {form: [] for form in forms}
for form in forms:
    for zone in zones:
        values[form].append(data[zone].get(form, 0))

# Plotting
fig, ax = plt.subplots(figsize=(14, 8))

bar_width = 0.04
index = np.arange(len(zones))

for i, form in enumerate(forms):
    bar_position = index + (i * bar_width)
    ax.bar(bar_position, values[form], bar_width, label=form)

# Adding labels and title
ax.set_xlabel('Geomorphic Zones')
ax.set_ylabel('Percentage')
ax.set_title('Coral Form Distribution by Geomorphic Zones')
ax.set_xticks(index + bar_width * (len(forms) / 2))
ax.set_xticklabels(zones)
ax.legend()

# Display the plot
plt.tight_layout()
plt.show()