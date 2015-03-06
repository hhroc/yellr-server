import json

with open("zipcodes.csv", "r") as f:
    csv = f.read()
rows = csv.split("\n")

def get_zipcode_data(target_zipcode):

    #with open("zipcodes.csv", "r") as f:
    #    csv = f.read()

    #rows = csv.split("\n")
    index = 0
    ret = None
    for row in rows:
        if index != 0 and row != '':
            values = row.replace('"','').split(',')
            if values[0] == target_zipcode:  # values[0] is zip
                ret = {
                    'zipcode': values[0],
                    'city': values[1],
                    'state_code': values[2],
                    'lat': float(values[3]),
                    'lng': float(values[4]),
                    'timezone': values[5],
                }
                break;
        index += 1
    #if ret == None:
    #    print "Invalid zipcode data."
    return ret

def build_geom_string(feature):

    #for feature in features:
    if True:
        zipcode_data = get_zipcode_data(feature['properties']['GEOID10'])
        coordinates = feature['geometry']['coordinates']
        geom_string = "POLYGON(("
        for i in range(0,len(coordinates[0])):
            coord = coordinates[0][i]
            lng = coord[0]
            lat = coord[1]
            geom_string += "{0} {1}".format(lng, lat)
            if i != len(coordinates[0])-1:
                geom_string += ","
        geom_string += "))"
    return zipcode_data, geom_string

def build_inserts():

    with open("zips_5_percent_plus.geojson", "r") as f:
        geojson = json.loads(f.read())

    print "Processing {0} zipcodes ...".format(len(geojson['features']))

    output_sql = ""
    output_sqlite = ""
    index = 0
    for feature in geojson['features']:
        if feature['geometry'] != None and len(feature['geometry']['coordinates']) != 0:
            zipcode_data, geom_string = build_geom_string(feature)
            if zipcode_data != None:
                #print "Working on {0}".format(feature['properties']['GEOID10'])
                sql_string = "INSERT INTO zipcodes(zipcode, city, state_code, lat, lng, timezone, geom) "
                sql_string += "VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6});".format(
                    '"{0}"'.format(zipcode_data['zipcode']),
                    '"{0}"'.format(zipcode_data['city']),
                    '"{0}"'.format(zipcode_data['state_code']),
                    zipcode_data['lat'],
                    zipcode_data['lng'],
                    zipcode_data['timezone'],
                    'GeomFromText("{0}")'.format(geom_string),
                )
                sqlite_string = "INSERT INTO zipcodes(zipcode, city, state_code, lat, lng, timezone) "
                sqlite_string += "VALUES({0}, {1}, {2}, {3}, {4}, {5});".format(
                    '"{0}"'.format(zipcode_data['zipcode']),
                    '"{0}"'.format(zipcode_data['city']),
                    '"{0}"'.format(zipcode_data['state_code']),
                    zipcode_data['lat'],
                    zipcode_data['lng'],
                    zipcode_data['timezone'],
                )
                #print sql_string
                #raise Exception('debug')
                output_sql += "{0}\n".format(sql_string)
                output_sqlite += "{0}\n".format(sqlite_string)
                index += 1
                #break
            else:
                print "No zipcode data for {0}".format(feature['properties']['GEOID10'])
        else:
            print "Invalid Zipcode data: {0}".format(feature['properties']['GEOID10'])
        if index % 100 == 0:
            print "{0} zipcodes processed.".format(index)
    return output_sql, output_sqlite

if __name__ == '__main__':

    output_sql, output_sqlite = build_inserts()

    with open("insert_zips.sql","w") as f:
        f.write(output_sql)

    with open("insert_zips_sqlite.sql","w") as f:
        f.write(output_sqlite)

    print "Done."

