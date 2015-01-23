The shapefiles for the UK postcodes come from this link:

http://www.opendoorlogistics.com/wp-content/uploads/2014/04/Reconstructed-UK-postcode-polygons-March-2014.zip

These have various copyright and license files included.

The post-processing by the company isn't quite right - 
the output shows some obvious clipping where Thames ought
to match the postcode lines.  If this is needed for high
accuracy map-typ processing, these things will need to be
recreated by hand.

This is doable using various mapping libraries and the 
coordinates of all the postcodes, using these as edges of
a postcode region.  It also sounds quite painful.