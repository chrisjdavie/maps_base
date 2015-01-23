'''
Created on 29 Oct 2014

@author: chris
'''
def main():
    shp_fname = '/home/chris/Projects/maps_base/drawing_a_map/postcode_shapefiles/parsed/London.shp'
    
    import fiona
    with fiona.open(shp_fname,'r') as f_chk:
        for shp in f_chk:
            print shp['properties']['name']

if __name__ == '__main__':
    main()