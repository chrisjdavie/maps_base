'''
This draws a map of london.  The lattiude and longitude are equally
balanced so it can be imposed on a map.  This is more fortune than
planning, really.

lines commented out concerning font size are used to make it 
projector-friendly

Created on 21 Nov 2014

@author: chris
'''
import numpy as np 
import fiona
from matplotlib.patches import Polygon as Polygon_m    
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as pl
from matplotlib import font_manager

def main():
    
    postcodes_fname = '../getting_london_postcodes/scrape_london_postcodes/postcodes.p'
    
    import pickle
    with open(postcodes_fname,'r') as f:
        postcodes = pickle.load(f)       
    
    import random
    
    ''' In the centre of London there are a series of very small 
        postcode regions beginning with EC and WC.  I've merged them
        all into one, but that requires a bit of hacking to make it
        all be something close to sensible.
    '''
    
    lcn_count = {}
    lcn_count['EC'] = random.randint(0,100)
    lcn_count['WC'] = random.randint(0,100)
    
    
    for pc in postcodes:
        lcn_count[pc] = random.randint(0,100)
    
    
    draw_london_map(lcn_count,'test')
    
#     import matplotlib.pyplot as pl
    pl.axis('off')
    pl.show()    
    
    

def draw_london_map(locn_count,cbar_label,cmap='gist_heat_r'):
    
    ''' locn_count, dict, { postcode_str, counts_int } '''
    ''' everybody loves gist_heat_r '''
    
    '''testing - followed the values of single postcode through
       this, checked they appeared on the map where they should
       geographically.
       
       It handles absent postcodes, sets those values to zero and
       gives a warning ("No sales in <postcode>"). Can be set to
       different behaviour'''
    
    ax, p, pcc_new, xyy = setup_map(cmap)
    
    cts_map = []
    
    '''Takes the postcodes plotted on the map, and assigns the
       number associated with the colour to a list in the same 
       order, for the colour plotting'''
    
    for map_pc in pcc_new:
        try:
#         if map_pc == 'SW3':
            cts_map.append(locn_count[map_pc])
#             else:
#                 cts_map.append(1)
        except(KeyError):
            print "No sales in ", map_pc
            cts_map.append(0)
            
#         raw_input()
    cts_map = np.array(cts_map)
#     print locn_count['SW3']
#     raw_input()
    
#     import matplotlib 
#     matplotlib.rc('xtick', labelsize=18) 
#     matplotlib.rc('ytick', labelsize=18) 
    

#     matplotlib.rcParams.update({'font.size': 18})     
    
    '''fixing the limits and colourbar'''
    
    p.set_array(cts_map)
    p.set_clim(0,np.max(np.array(cts_map)))
    ax.add_collection(p)
    cb = pl.colorbar(p,label=cbar_label)#,fontsize=18)
    cb_ax = cb.ax
    text = cb_ax.yaxis.label
    font = font_manager.FontProperties(weight='bold')
    text.set_font_properties(font)
#     cbtext=cb.get_texts()
#     pl.setp(cbtext)
     

        
    put_Thames_on(ax)
#     
    return pcc_new, xyy, ax, cts_map
#         

def put_Thames_on(ax):
    ''' This came from a shapefile collection of the coastlines 
        and rivers of Europe, and quite a bit of painful work to 
        turn that into this'''
    
    shp_fname = '../getting_london_postcodes/Thames/Thames_ish2'
    
    with fiona.open(shp_fname + '.shp') as shps:
        for i, shp in enumerate(shps):
            print i
#             map_pc  = shp['properties']['name']
            xy = shp.items()[0][1]['coordinates'][0]

#     m.readshapefile(shp_fname,'waters')    
#     for shapedict, xy in zip(m.waters_info,m.waters):
            poly = Polygon_m(xy, facecolor='blue')#, alpha=1.0)
            ax.add_patch(poly)    
            

def setup_map(cmap='gist_heat_r'):
    
    '''shp_fname contains the 'shapefiles' of the london postcodes,
       basically polygons plus some geographical information.  The
       following stiches that into a map, but it's not graceful  
       
       The website I downloaded these from is dodgey, it's good enough
       for visual presenting, but if it's precise maths you need on
       postcode regions, something else will be needed'''
    
    shp_fname = '/home/chris/Projects/maps_base/drawing_a_map/postcode_shapefiles/parsed/London'
    
    '''Finding and using bounds of London'''
    
    with fiona.open(shp_fname + '.shp') as shps:
        bds = shps.bounds
    
    extra = 0.01
    ll = (bds[0], bds[1])
    ur = (bds[2], bds[3])
    
    from itertools import chain
    coords = list(chain(ll, ur))
    w, h = coords[2] - coords[0], coords[3] - coords[1]
    
    xlims = [ coords[0] - extra * w, coords[2] + extra * w ]
    ylims = [ coords[1] - extra + 0.01 * h, coords[3] + extra + 0.01 * h ]
    
    
    '''Here I'm trying to merge all the EC and WC areas'''
    from shapely.geometry import Polygon, LinearRing
     
    xyy_new  = [ None, None ]
    pcc_new  = [ 'EC', 'WC' ]
     
    EC_pgs = []
    WC_pgs = []
    
    ''' opens and stores the xy coords of the bounds of all postcodes
        in london, except WC and EC, which it stores separately '''
    
    with fiona.open(shp_fname + '.shp') as shps:
        
        for i, shp in enumerate(shps):
            print i
            map_pc  = shp['properties']['name']
            xy = shp.items()[0][1]['coordinates'][0]
            
            if len(np.shape(xy)) == 3 and len(xy) == 1:
                xy = xy[0]
            elif len(np.shape(xy[0])) == 2 and len(xy) == 2:
                '''This is not general and should be fixed if I extend this to outside London'''
                xy0 = xy[0]
                xy1 = xy[1]
                xy = xy0
                if len(xy1[0]) > len(xy0[1]):
                    xy = xy1 
                    
            if map_pc[:2] == 'EC':
                EC_pgs.append(Polygon(xy))
            elif map_pc[:2] == 'WC':
                WC_pgs.append(Polygon(xy))
            else:
                pcc_new.append(map_pc)
                xyy_new.append(xy)
    
    '''WC and EC are merged using this.  It is temperamental.'''
    
    from shapely.ops import cascaded_union
    WC_pg = cascaded_union(WC_pgs)
    EC_pg = cascaded_union(EC_pgs)
    
    xyy_new[0] = np.array(LinearRing(EC_pg.exterior.coords).xy).transpose()
     
    xyy_new[1] = np.array(LinearRing(WC_pg.exterior.coords).xy).transpose()
    
    pl.xlim(xlims)
    pl.ylim(ylims)
    
    ax = pl.gca()
    
    patches = []
    
    ''' makes the polygons into a plotable form by matplotlib
        alpha sets the transparancy, for putting over maps of london
        so people can see what this does.'''
    
    for i, (map_pc, xy) in enumerate(zip(pcc_new, xyy_new)):
        
        xy = np.array(xy)
        
        poly = Polygon_m(xy, True) 
        
        patches.append(poly)

    p = PatchCollection(patches,cmap=cmap)#,alpha=1.0)   
    return ax, p, pcc_new, xyy_new


if __name__ == '__main__':
    main()