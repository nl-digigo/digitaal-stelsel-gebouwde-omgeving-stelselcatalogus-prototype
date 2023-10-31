import json
import os

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
            "data_service_provider_name",
            "service_name",
            "service_description",
            "contact_point",
            "adherence",
            "version",
            "conforms_to",
            "level_of_assurance",
            "security_level",
            "acces_rules",
            "obligations_and_advice",
            "service_level_agreements",
            "costs"
        ]
        for key in human_readable_list:
            try:
                md_file.write(f'<b>{key.capitalize().replace("_", " ")+"</b>"}: {service[key]}'+'  \n')
            except:
                pass
       
        # Write technical-person details
        for key, value in service.items():
            if key not in ["feature", "description","path_image","path_thumbnail","keywords"]+human_readable_list:
                md_file.write(f'<b>{key.capitalize().replace("_", " ")+"</b>"}: {value}'+'  \n')
        

print("Markdown files created.")