'''
Created on 29 Oct 2014

@author: chris
'''
def main():
    source_shp_fname = '/home/chris/Projects/maps_base/drawing_a_map/postcode_shapefiles/Distribution/Districts.shp'
    
    import fiona
    with fiona.open(source_shp_fname,'r') as source:
        for shp in source:
            if shp['properties']['name'][:2] == 'WC' or shp['properties']['name'][:2] == 'EC':
                print shp['properties']['name']
                

if __name__ == '__main__':
    main()