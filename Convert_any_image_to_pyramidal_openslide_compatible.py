import pyvips

from tifffile import TiffFile, imwrite

def convert_ome_to_tiff(input_path, output_path):
    """
    Convert an OME-TIFF file to a standard TIFF file.

    Parameters:
    input_path (str): The path to the input OME-TIFF file.
    output_path (str): The path to save the output TIFF file.
    """
    # Read the OME-TIFF file
    with TiffFile(input_path) as tif:
        # Extract the image data
        image_data = tif.asarray()

    # Save the image data as a standard TIFF file
    imwrite(output_path, image_data)

    print(f"Conversion from OME-TIFF to TIFF is complete. The output file is saved as '{output_path}'.")

def convert_to_pyramidal_tiff(input_image_path, output_image_path):
    """
    Convert a regular TIFF image to a pyramidal TIFF format, compatible with OpenSlide.
    
    :param input_image_path: Path to the input TIFF image.
    :param output_image_path: Path to the output pyramidal TIFF image.
    """
    # Load the TIFF image using pyvips
    image = pyvips.Image.new_from_file(input_image_path, access='sequential')

    # Save the image as a pyramidal TIFF with tiling and multiple resolutions
    image.tiffsave(output_image_path,
                   tile=True,             # Enable tiling
                   pyramid=True,   # Create multiple resolution levels
                   compression='jpeg',    # Compression method (JPEG is common for WSI)
                   tile_width=256,        # Tile width
                   tile_height=256,       # Tile height
                   bigtiff=True)          # Ensure the output is in BigTIFF format for large images

# Example usage:
input_tiff = "/home/images/image.tif"
output_pyramidal_tiff = "/home/images/pyramidal.tif"

convert_to_pyramidal_tiff(input_tiff, output_pyramidal_tiff)

## adding Meta data 
tifftools set -y -s ImageDescription  "Aperio Fake |AppMag = 40|MPP = 0.2527" /home/pyramidal.tif

