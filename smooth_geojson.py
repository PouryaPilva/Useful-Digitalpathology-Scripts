import geojson
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry import shape
from shapely.ops import transform
import pyproj

def smooth_polygon(polygon, smoothing_factor=3):
    """Smooth the polygon using a moving average filter on its points."""
    if isinstance(polygon, Polygon):
        coords = np.array(polygon.exterior.coords)
        smoothed_coords = moving_average(coords, smoothing_factor)
        return Polygon(smoothed_coords)
    elif isinstance(polygon, MultiPolygon):
        return MultiPolygon([smooth_polygon(p, smoothing_factor) for p in polygon])
    else:
        return polygon

def moving_average(coords, window_size):
    """Applies a simple moving average to smooth coordinates."""
    smoothed = []
    for i in range(len(coords)):
        start = max(0, i - window_size)
        end = min(len(coords), i + window_size + 1)
        smoothed.append(np.mean(coords[start:end], axis=0))
    return smoothed

def read_geojson(input_file):
    """Reads a GeoJSON file and returns its features."""
    with open(input_file, 'r') as f:
        data = geojson.load(f)
    return data['features']

def save_geojson(data, output_file):
    """Saves the GeoJSON data to a new file."""
    with open(output_file, 'w') as f:
        geojson.dump(data, f)

def smooth_contours(input_geojson, output_geojson, smoothing_factor=3):
    """Reads contours from GeoJSON, smooths them, and saves to another GeoJSON."""
    # Read the GeoJSON file
    features = read_geojson(input_geojson)
    
    # Smooth each contour in the features list
    for feature in features:
        geom = shape(feature['geometry'])  # Convert the geometry to a Shapely object
        smoothed_geom = smooth_polygon(geom, smoothing_factor)
        
        # Update the feature with the smoothed geometry
        feature['geometry'] = geojson.loads(geojson.dumps(smoothed_geom.__geo_interface__))

    # Save the smoothed contours to a new GeoJSON file
    save_geojson({"type": "FeatureCollection", "features": features}, output_geojson)
    print(f"Smoothed contours saved to {output_geojson}")

# Example usage
input_geojson = '/home/pourya/Desktop/01_017_PAS.geojson'
output_geojson = '/home/pourya/Desktop/01_017_PAS2.geojson'
smoothing_factor = 10  # Adjust this for more or less smoothing

smooth_contours(input_geojson, output_geojson, smoothing_factor)
