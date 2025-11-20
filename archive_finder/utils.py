import json
from django.contrib.gis.geos.geometry import GEOSGeometry
from geojson_pydantic import Polygon


def is_valid_geometry_type(geojson):
    if geojson['type'] in ("MultiPolygon",  "Polygon", "Point"):
        return True
    return False

def geojson_to_geosgeom(geojson) -> GEOSGeometry:    
    if isinstance(geojson, str):
        return GEOSGeometry(geojson)
    if isinstance(geojson, dict):
        return GEOSGeometry(json.dumps(geojson))

# def geojson_to_pydanticpolygon(geojson) -> Polygon:    
#     if isinstance(geojson, str):
#         geojson_dict = json.loads(geojson)
#         return Polygon(type=geojson_dict["type"], coordinates=geojson_dict["coordinates"])
#     if isinstance(geojson, dict):
#         return Polygon(type=geojson_dict["type"], coordinates=geojson_dict["coordinates"])
