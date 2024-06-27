import json 

filename = "Andaman-Sea-20230309235804_output.json"

f = open(filename)
data = json.load(f)

# add up all the values where the key includes "&"
single_zone_total = 0
more_than_two_zones_total = 0

for key in data:
    if "&" not in key:
        single_zone_total += data[key]

    if len(key.split("&")) > 2:
        more_than_two_zones_total += data[key]
        

print(f"Total percentage of rectangles in single zones: {single_zone_total:.2f}%")
print(f"Total percentage of rectangles in multiple zones: {100 - single_zone_total:.2f}%")
print(f"Total percentage of rectangles in more than two zones: {more_than_two_zones_total:.2f}%")