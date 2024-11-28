from PIL import Image
from fpdf import FPDF
import os
import sys

def png_to_pdf(input_file, output_file, page_height=842):
    # Open the input image
    img = Image.open(input_file)
    width, height = img.size
    
    # Create a PDF object with the same width as the image
    pdf = FPDF(orientation='P', unit='pt', format=(width, page_height))
    
    y_offset = 0  # Start at the top of the image
    temp_files = []  # To keep track of temporary files

    while y_offset < height:
        pdf.add_page()
        
        # Crop the image for the current page
        img_crop = img.crop((0, y_offset, width, min(y_offset + page_height, height)))
        
        # Save the cropped section temporarily
        temp_file = f"temp_page_{y_offset}.png"
        img_crop.save(temp_file)
        temp_files.append(temp_file)  # Add to the list of temp files
        
        # Add the cropped section to the PDF
        pdf.image(temp_file, 0, 0, width, min(page_height, height - y_offset))
        
        # Move the offset for the next page
        y_offset += page_height

    # Save the final PDF
    pdf.output(output_file)
    print(f"Multi-page PDF created successfully: {output_file}")
    
    # Delete all temporary files
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            print(f"Deleted temporary file: {temp_file}")
        except Exception as e:
            print(f"Could not delete {temp_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python imager.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    png_to_pdf(input_file, output_file)
