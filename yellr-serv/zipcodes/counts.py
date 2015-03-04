import json
geojson = json.loads(open('zips.geojson','r').read())
total_count = len(geojson['features'])

geojson_5_percent = json.loads(open('zips_5_percent.geojson','r').read())
total_5_percent_count = len(geojson_5_percent['features'])

#geojson_10_percent = json.loads(open('zips_10_percent.geojson','r').read())
#total_10_percent_count = len(geojson_10_percent['features'])

#null_count_5_percent = 0
for i in range(0,len(geojson_5_percent['features'])): #feature in geojson_5_percent['features']:
    if geojson_5_percent['features'][i]['geometry'] == None or len(geojson_5_percent['features'][i]['geometry']['coordinates']) == 0:
#        null_count_5_percent += 1
        if geojson['features'][i]['properties']['GEOID10'] != geojson_5_percent['features'][i]['properties']['GEOID10']:
            raise Exception("Lists out of sync")
        geojson_5_percent['features'][i] = geojson['features'][i]  

#null_count_10_percent = 0
#for feature in geojson_10_percent['features']:
#    if feature['geometry'] == None or len(feature['geometry']['coordinates']) == 0:
#        null_count_10_percent += 1

#print total_count

#print total_5_percent_count

#print total_10_percent_count

#print null_count_5_percent

#print null_count_10_percent

null_count_5_percent = 0
for i in range(0,len(geojson_5_percent['features'])): #feature in geojson_5_percent['features']:
    if geojson_5_percent['features'][i]['geometry'] == None or len(geojson_5_percent['features'][i]['geometry']['coordinates']) == 0:
        null_count_5_percent += 1

print "{0} null/empty zipcodes.".format(null_count_5_percent)

with open('zips_5_percent_plus.geojson','w') as f:
    f.write(json.dumps(geojson_5_percent))
