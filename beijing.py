from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
import matplotlib.pyplot as plt
import json
from gradient import getColor
from matplotlib.cbook import is_scalar, dedent
from matplotlib.collections import LineCollection, PolyCollection
import os
import codecs
import numpy as np

mapdir = 'beijingMapinfo/'

class Beijing(Basemap):
    def __init__(self, llcrnrlon=None, llcrnrlat=None,
                 urcrnrlon=None, urcrnrlat=None,
                 llcrnrx=None, llcrnry=None,
                 urcrnrx=None, urcrnry=None,
                 width=None, height=None,
                 projection='cyl', resolution='c',
                 area_thresh=None, rsphere=6370997.0,
                 ellps=None, lat_ts=None,
                 lat_1=None, lat_2=None,
                 lat_0=None, lon_0=None,
                 lon_1=None, lon_2=None,
                 o_lon_p=None, o_lat_p=None,
                 k_0=None,
                 no_rot=False,
                 suppress_ticks=True,
                 satellite_height=35786000,
                 boundinglat=None,
                 fix_aspect=True,
                 anchor='C',
                 celestial=False,
                 round=False,
                 epsg=None,
                 ax=None):
        resolution = 'i'
        projection = 'tmerc'
        lat_0 = 39.76
        lon_0 = 115.45
        self.level = 1
        super(Beijing,self).__init__(llcrnrlon, llcrnrlat,
                                     urcrnrlon, urcrnrlat,
                                     llcrnrx, llcrnry,
                                     urcrnrx, urcrnry,
                                     width, height,
                                     projection, resolution,
                                     area_thresh, rsphere,
                                     ellps, lat_ts,
                                     lat_1, lat_2,
                                     lat_0, lon_0,
                                     lon_1, lon_2,
                                     o_lon_p, o_lat_p,
                                     k_0, no_rot,
                                     suppress_ticks,
                                     satellite_height,
                                     boundinglat,
                                     fix_aspect, anchor, celestial,
                                     round, epsg, ax)
        # self.readshapefile(mapdir+'county_region', 'county_region')


    def project(self,x,y):
        '''
        :param x: longitude
        :param y: latitude
        :return: a tuple with (x,y) with projected coordinate
        '''
        x = [x]
        y = [y]
        xa, ya = self(x, y)
        # print(xa, ya)
        xy = list(zip(xa, ya))
        return xy[0]
    def projectList(self,x,y):
        '''
        :param x: longitude list
        :param y: latitude list
        :return: a list and each element is a tuple with (x,y) with projected coordinate
        '''
        xa, ya = self(x, y)
        # print(xa, ya)
        return list(zip(xa, ya))
    def readmapinfo(self,shapefile,name, default_encoding='utf-8'):

        import shapefile as shp
        from shapefile import Reader
        shp.default_encoding = default_encoding
        if not os.path.exists('%s.shp'%shapefile):
            raise IOError('cannot locate %s.shp'%shapefile)
        if not os.path.exists('%s.shx'%shapefile):
            raise IOError('cannot locate %s.shx'%shapefile)
        if not os.path.exists('%s.dbf'%shapefile):
            raise IOError('cannot locate %s.dbf'%shapefile)
        # open shapefile, read vertices for each object, convert
        # to map projection coordinates (only works for 2D shape types).
        try:
            shf = Reader(shapefile)
        except:
            raise IOError('error reading shapefile %s.shp' % shapefile)
        fields = shf.fields
        coords = []; attributes = []
        msg=dedent("""
        shapefile must have lat/lon vertices  - it looks like this one has vertices
        in map projection coordinates. You can convert the shapefile to geographic
        coordinates using the shpproj utility from the shapelib tools
        (http://shapelib.maptools.org/shapelib-tools.html)""")
        shptype = shf.shapes()[0].shapeType
        bbox = shf.bbox.tolist()
        info = (shf.numRecords,shptype,bbox[0:2]+[0.,0.],bbox[2:]+[0.,0.])
        npoly = 0
        for shprec in shf.shapeRecords():
            shp = shprec.shape; rec = shprec.record
            npoly = npoly + 1
            if shptype != shp.shapeType:
                raise ValueError('readshapefile can only handle a single shape type per file')
            if shptype not in [1,3,5,8]:
                raise ValueError('readshapefile can only handle 2D shape types')
            verts = shp.points
            if shptype in [1,8]: # a Point or MultiPoint shape.
                lons, lats = list(zip(*verts))
                if max(lons) > 721. or min(lons) < -721. or max(lats) > 90.01 or min(lats) < -90.01:
                    raise ValueError(msg)
                # if latitude is slightly greater than 90, truncate to 90
                lats = [max(min(lat, 90.0), -90.0) for lat in lats]
                if len(verts) > 1: # MultiPoint
                    x,y = (lons, lats)
                    # x,y = self(lons, lats)
                    coords.append(list(zip(x,y)))
                else: # single Point
                    x,y = (lons[0], lats[0])
                    # x,y = self(lons[0], lats[0])
                    coords.append((x,y))
                attdict={}
                for r,key in zip(rec,fields[1:]):
                    attdict[key[0]]=r
                attributes.append(attdict)
            else: # a Polyline or Polygon shape.
                parts = shp.parts.tolist()
                ringnum = 0
                for indx1,indx2 in zip(parts,parts[1:]+[len(verts)]):
                    ringnum = ringnum + 1
                    lons, lats = list(zip(*verts[indx1:indx2]))
                    if max(lons) > 721. or min(lons) < -721. or max(lats) > 90.01 or min(lats) < -90.01:
                        raise ValueError(msg)
                    # if latitude is slightly greater than 90, truncate to 90
                    lats = [max(min(lat, 90.0), -90.0) for lat in lats]
                    x, y = (lons, lats)
                    # x, y = self(lons, lats)
                    coords.append(list(zip(x,y)))
                    attdict={}
                    for r,key in zip(rec,fields[1:]):
                        attdict[key[0]]=r
                    # add information about ring number to dictionary.
                    attdict['RINGNUM'] = ringnum
                    attdict['SHAPENUM'] = npoly
                    attributes.append(attdict)
        return coords
    def saveCoords(self,jsonfilename,coords):
        with open(jsonfilename, 'w') as fp:
            json.dump(coords,fp)
    def projectcoords(self,coords):
        lines = []
        for verts in coords:
            lons, lats = list(zip(*verts))
            lines.append(self.projectList(lons,lats))
        return lines
    def loadlines(self,name,curdir='beijingJson',zorder=None,
                      linewidth=0.5,color='k',antialiased=1,ax=None,
                      default_encoding='utf-8',linestyle='-',linesalpha = 1):
        # get current axes instance (if none specified).
        filename = curdir+'/'+name+'.json'
        coords = json.load(codecs.open(filename, 'r', 'utf-8'))
        coords = self.projectcoords(coords)

        ax = ax or self._check_ax()
        # make LineCollections for each polygon.
        lines = LineCollection(coords,antialiaseds=(1,))
        lines.set_color(color)
        lines.set_linewidth(linewidth)
        lines.set_linestyle(linestyle)
        lines.set_alpha(linesalpha)
        lines.set_label('_nolabel_')
        if zorder is not None:
           lines.set_zorder(zorder)
        ax.add_collection(lines)
        # set axes limits to fit map region.
        self.set_axes_limits(ax=ax)
        # clip boundaries to map limbs
        lines,c = self._cliplimb(ax,lines)
        self.__dict__[name]=coords
        return lines
        # self.__dict__[name+'_info']=attributes
        # return info
    def readshapefileext(self,shapefile,name,drawbounds=True,zorder=None,
                      linewidth=0.5,color='k',antialiased=1,ax=None,
                      default_encoding='utf-8',linestyle='-'):
        """
        Read in shape file, optionally draw boundaries on map.

        .. note::
          - Assumes shapes are 2D
          - only works for Point, MultiPoint, Polyline and Polygon shapes.
          - vertices/points must be in geographic (lat/lon) coordinates.

        Mandatory Arguments:

        .. tabularcolumns:: |l|L|

        ==============   ====================================================
        Argument         Description
        ==============   ====================================================
        shapefile        path to shapefile components.  Example:
                         shapefile='/home/jeff/esri/world_borders' assumes
                         that world_borders.shp, world_borders.shx and
                         world_borders.dbf live in /home/jeff/esri.
        name             name for Basemap attribute to hold the shapefile
                         vertices or points in map projection
                         coordinates. Class attribute name+'_info' is a list
                         of dictionaries, one for each shape, containing
                         attributes of each shape from dbf file, For
                         example, if name='counties', self.counties
                         will be a list of x,y vertices for each shape in
                         map projection  coordinates and self.counties_info
                         will be a list of dictionaries with shape
                         attributes.  Rings in individual Polygon
                         shapes are split out into separate polygons, and
                         additional keys 'RINGNUM' and 'SHAPENUM' are added
                         to the shape attribute dictionary.
        ==============   ====================================================

        The following optional keyword arguments are only relevant for Polyline
        and Polygon shape types, for Point and MultiPoint shapes they are
        ignored.

        .. tabularcolumns:: |l|L|

        ==============   ====================================================
        Keyword          Description
        ==============   ====================================================
        drawbounds       draw boundaries of shapes (default True).
        zorder           shape boundary zorder (if not specified,
                         default for mathplotlib.lines.LineCollection
                         is used).
        linewidth        shape boundary line width (default 0.5)
        color            shape boundary line color (default black)
        antialiased      antialiasing switch for shape boundaries
                         (default True).
        ax               axes instance (overrides default axes instance)
        ==============   ====================================================

        A tuple (num_shapes, type, min, max) containing shape file info
        is returned.
        num_shapes is the number of shapes, type is the type code (one of
        the SHPT* constants defined in the shapelib module, see
        http://shapelib.maptools.org/shp_api.html) and min and
        max are 4-element lists with the minimum and maximum values of the
        vertices. If ``drawbounds=True`` a
        matplotlib.patches.LineCollection object is appended to the tuple.
        """
        import shapefile as shp
        from shapefile import Reader
        shp.default_encoding = default_encoding
        if not os.path.exists('%s.shp'%shapefile):
            raise IOError('cannot locate %s.shp'%shapefile)
        if not os.path.exists('%s.shx'%shapefile):
            raise IOError('cannot locate %s.shx'%shapefile)
        if not os.path.exists('%s.dbf'%shapefile):
            raise IOError('cannot locate %s.dbf'%shapefile)
        # open shapefile, read vertices for each object, convert
        # to map projection coordinates (only works for 2D shape types).
        try:
            shf = Reader(shapefile)
        except:
            raise IOError('error reading shapefile %s.shp' % shapefile)
        fields = shf.fields
        coords = []; attributes = []
        msg=dedent("""
        shapefile must have lat/lon vertices  - it looks like this one has vertices
        in map projection coordinates. You can convert the shapefile to geographic
        coordinates using the shpproj utility from the shapelib tools
        (http://shapelib.maptools.org/shapelib-tools.html)""")
        shptype = shf.shapes()[0].shapeType
        bbox = shf.bbox.tolist()
        info = (shf.numRecords,shptype,bbox[0:2]+[0.,0.],bbox[2:]+[0.,0.])
        npoly = 0
        for shprec in shf.shapeRecords():
            shp = shprec.shape; rec = shprec.record
            npoly = npoly + 1
            if shptype != shp.shapeType:
                raise ValueError('readshapefile can only handle a single shape type per file')
            if shptype not in [1,3,5,8]:
                raise ValueError('readshapefile can only handle 2D shape types')
            verts = shp.points
            if shptype in [1,8]: # a Point or MultiPoint shape.
                lons, lats = list(zip(*verts))
                if max(lons) > 721. or min(lons) < -721. or max(lats) > 90.01 or min(lats) < -90.01:
                    raise ValueError(msg)
                # if latitude is slightly greater than 90, truncate to 90
                lats = [max(min(lat, 90.0), -90.0) for lat in lats]
                if len(verts) > 1: # MultiPoint
                    x,y = self(lons, lats)
                    coords.append(list(zip(x,y)))
                else: # single Point
                    x,y = self(lons[0], lats[0])
                    coords.append((x,y))
                attdict={}
                for r,key in zip(rec,fields[1:]):
                    attdict[key[0]]=r
                attributes.append(attdict)
            else: # a Polyline or Polygon shape.
                parts = shp.parts.tolist()
                ringnum = 0
                for indx1,indx2 in zip(parts,parts[1:]+[len(verts)]):
                    ringnum = ringnum + 1
                    lons, lats = list(zip(*verts[indx1:indx2]))
                    if max(lons) > 721. or min(lons) < -721. or max(lats) > 90.01 or min(lats) < -90.01:
                        raise ValueError(msg)
                    # if latitude is slightly greater than 90, truncate to 90
                    lats = [max(min(lat, 90.0), -90.0) for lat in lats]
                    x, y = self(lons, lats)
                    coords.append(list(zip(x,y)))
                    attdict={}
                    for r,key in zip(rec,fields[1:]):
                        attdict[key[0]]=r
                    # add information about ring number to dictionary.
                    attdict['RINGNUM'] = ringnum
                    attdict['SHAPENUM'] = npoly
                    attributes.append(attdict)
        # draw shape boundaries for polylines, polygons  using LineCollection.
        if shptype not in [1,8] and drawbounds:
            # get current axes instance (if none specified).
            ax = ax or self._check_ax()
            # make LineCollections for each polygon.
            lines = LineCollection(coords,antialiaseds=(1,))
            lines.set_color(color)
            lines.set_linewidth(linewidth)
            lines.set_linestyle(linestyle)
            lines.set_label('_nolabel_')
            if zorder is not None:
               lines.set_zorder(zorder)
            ax.add_collection(lines)
            # set axes limits to fit map region.
            self.set_axes_limits(ax=ax)
            # clip boundaries to map limbs
            lines,c = self._cliplimb(ax,lines)
            info = info + (lines,)
        self.__dict__[name]=coords
        self.__dict__[name+'_info']=attributes
        return info

    # def pointmarked(self,file='counties.csv'):
    #     import pandas as pd
    #     file = configdir+file
    #     csv=pd.read_csv(file)
    #     name = [name for name in csv['NAME']]
    #     x = csv['X'].tolist()
    #     y = csv['Y'].tolist()
    #     for i in range(len(name)):
    #         X,Y=self(float(x[i]),float(y[i]))
    #         plt.text(X,Y,name[i],horizontalalignment ='center')

if __name__ == "__main__":
    map= Beijing(llcrnrlon=115.3,llcrnrlat=39.4,urcrnrlon=117.6,urcrnrlat=41.1,
             resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = 115.45)

    # map.readshapefile('d:/beijingMapinfo/county_region', 'county_region')
    # map.fillPolygon(map.county_region[0],color='r',fill_color='aqua')

    x = [116.46198273, 115.57, 115.58, 116.313432, 116.445303, 116.289501, 116.289501]
    y = [39.91296005, 39.82, 39.83, 39.970475, 39.927248, 39.868793, 39.868793]
    xy = map.projectList(x, y)
    print(xy)

    print(map.project(116.46198273,39.91296005))

    verts = map.readmapinfo('beijingMapinfo/county_region', 'county_region')
    map.saveCoords('beijingJson/county_region.json',verts)

    plt.show()