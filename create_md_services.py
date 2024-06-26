import json
import os
from PIL import Image
import re

def add_white_background(file_path, output_file_path):
    # def add_white_background(file_path, output_file_path):
    with Image.open(file_path) as im:
        width, height = im.size
        square_size = max(width, height)
        # Create a white background square image with the desired square size
        background = Image.new('RGB', (square_size, square_size), "WHITE")
        # Calculate position to paste the image on the background
        # Horizontally centered, and vertically, it should have equal space at top and bottom
        position = ((square_size - width) // 2, (square_size - height) // 2)

        # If the image has an alpha channel, keep the processing as is
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            # Paste the image on the background using the alpha channel as mask
            background.paste(im, position, im.split()[3])
        else:
            # Paste the image on the background without any mask
            background.paste(im, position)
        
        # Save the image with white background as a new file
        background.save(output_file_path)

def process_all_pngs(folder_path):
    # Loop over all files in the given folder
    for filename in os.listdir(folder_path):
        # Check if the file is a PNG
        if filename.lower().endswith('.png'):
            file_path = os.path.join(folder_path, filename)
            # Define the output file path (this could be the same as input or different)
            output_file_path = os.path.join(folder_path, filename)
            # Add a white background to the PNG
            add_white_background(file_path, output_file_path)

def transform_string(s):
    # First, replace underscores with spaces
    s_no_underscores = s.replace("_", " ")
    # Then, split on capital letters as before, keeping consecutive capitals together
    s_with_spaces = re.sub(r"(?<=[a-z])([A-Z])|(?<=[A-Z])([A-Z][a-z])", r" \1\2", s_no_underscores)
    # Finally, capitalize the first letter of each word
    return ' '.join(word.capitalize() for word in s_with_spaces.split())

# Usage
# Set your folder path here
# folder_path = '/folder/to/path'
folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
# Make sure the 'processed' folder exists or create it
os.makedirs(os.path.join(folder_path), exist_ok=True)
process_all_pngs(folder_path)


# Given JSON data
file_data_services = 'data_services_list.json'
with open(file_data_services, 'r') as f:
    data = json.load(f)

# Front matter template
file_front_matter_services = 'service_front_matter.md'
with open(file_front_matter_services, 'r', encoding='utf-8') as f:
    front_matter = f.read()

# Directory to save markdown files
output_directory = "_services"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate through all files in the directory
for filename in os.listdir(output_directory):
    # Check if the file has a .md extension
    if filename.endswith('.md'):
        # Construct the full file path
        file_path = os.path.join(output_directory, filename)
        try:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

# Iterate over the JSON data to create markdown files
for service in data:
    with open(os.path.join(output_directory, f'{service["service_id"]}.md'), 'w') as md_file:
        
        # Write front matter
        md_file.write(front_matter)
        try:
            md_file.write(f'title: {service["feature"]}\n')
        except:
            md_file.write(f'title: {service["service_name"]}\n')
        try: 
            md_file.write(f'description: {service["description"]}\n')
        except:
            md_file.write(f'description: {service["service_description"]}\n')
        md_file.write(f'image:\n')
        # md_file.write(f'   path: {service["path_image"]}\n')
        md_file.write(f'   thumbnail: {service["path_thumbnail"]}\n')
        try:
            md_file.write(f'   caption: {service["description"]}\n')
        except:
            md_file.write(f'description: {service["service_description"]}\n')
        try:
            md_file.write(f'tags: {service["keywords"]}\n')
        except:
            pass
        md_file.write("---\n\n")
        
        # Write normal-person details
        human_readable_list = [
            "party_name",
            "feature",
            "description",
            "contactPoint",
            "adherence",
            "conformsTo",
            "levelOfAssurance",
            "securityLevel",
            "accessRights",
            "serviceLevelAgreements",
            "costs"
        ]
        for key in human_readable_list:
            try:
                md_file.write(f'<b>{transform_string(key)+"</b>"}: {service[key]}'+'  \n')
            except:
                pass
       
        # Write technical-person details
        # for key, value in service.items():
        #     if key not in ["feature", "description","path_image","path_thumbnail","keywords"]+human_readable_list:
        #         md_file.write(f'<b>{key.capitalize().replace("_", " ")+"</b>"}: {value}'+'  \n')
        for key, value in service.items():
            if key not in ["feature", "description", "path_image", "path_thumbnail", "keywords"] + human_readable_list:
                # Check if the key contains 'endpoint' or 'Endpoint'
                if 'endpoint' in key.lower() or 'url' in key.lower():  # This will check for 'endpoint' in any case
                    md_file.write(f'<b>{transform_string(key)}</b>: [{value}]({value})' + '  \n')
                else:
                    md_file.write(f'<b>{transform_string(key)}</b>: {value}' + '  \n')

print("Markdown files created.")