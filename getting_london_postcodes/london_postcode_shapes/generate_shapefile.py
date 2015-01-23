'''
Created on 28 Oct 2014

@author: chris
'''
def main():
    source_shp_fname = '/home/chris/Projects/maps_base/drawing_a_map/postcode_shapefiles/Distribution/Districts.shp'
    sink_shp_fname = '/home/chris/Projects/maps_base/drawing_a_map/postcode_shapefiles/parsed/London.shp'
    postcodes_fname = '../scrape_london_postcodes/postcodes.p'
    
    import pickle
    with open(postcodes_fname,'r') as f:
        postcodes = pickle.load(f)    
    
    import fiona
    with fiona.open(source_shp_fname,'r') as source:
        
        # Copy the source schema and add two new properties.
        sink_schema = source.schema.copy()
        
        with fiona.open(sink_shp_fname, 'w',
                        crs=source.crs,
                        driver=source.driver,
                        schema=sink_schema,
                        ) as sink:
            
            for shp in source:
                if shp['properties']['name'] in postcodes or shp['properties']['name'][:2] == 'WC' or shp['properties']['name'][:2] == 'EC':
                    print shp['properties']
                    sink.write(shp)
        

if __name__ == '__main__':
    main()