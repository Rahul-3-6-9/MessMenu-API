import json
import os
import re
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key='AIzaSyChoUuA5bNG2MdlEIbqaCs7BW1vYf-Kaao')


# Function to process a single file (PDF, Excel, or downloaded GSheet) using Gemini
def process_file(file_path, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')  

    uploaded_file = genai.upload_file(file_path)
    response = model.generate_content([prompt, uploaded_file])
    json_text = response.text.strip('```json\n').strip('```')
    return json.loads(json_text)


# Function to map filename menu type to JSON menu type
def map_menu_type(filename_menu_type):
    filename_menu_type = ' '.join(filename_menu_type.strip().split())
    menu_type_mapping = {
        'Veg': 'Unified_Veg',
        'Non Veg': 'Unified_Non_Veg',
        'North Veg': 'North_Veg',
        'North Non Veg': 'North_Non_Veg',
        'North Veg No Onion Garlic': 'North_Veg_No_Onion_Garlic',
        'South Veg': 'South_Veg',
        'South Non Veg': 'South_Non_Veg'
    }
    mapped_type = menu_type_mapping.get(filename_menu_type, None)
    if not mapped_type:
        print(f"Warning: Could not map menu type '{filename_menu_type}' to a valid JSON menu type")
    return mapped_type


# Function to process multiple files and aggregate results
def process_files(file_paths, prompt):

    menu_types = [
        'Unified_Veg', 'Unified_Non_Veg', 'North_Veg', 'North_Non_Veg',
        'North_Veg_No_Onion_Or_Garlic', 'South_Veg', 'South_Non_Veg'
    ]
    weeks = ['A', 'B', 'C', 'D']

    aggregated_json = {}
    for menu_type in menu_types:
        aggregated_json[menu_type] = {
            "common_items": {},
            "A": {"schedule": {}},
            "B": {"schedule": {}},
            "C": {"schedule": {}},
            "D": {"schedule": {}}
        }
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for week in weeks:
            for day in days:
                aggregated_json[menu_type][week]["schedule"][day] = {
                    "Breakfast": [],
                    "Lunch": [],
                    "Snacks": [],
                    "Dinner": []
                }


    for filename, file_path in file_paths:
        print(f"Processing file: {filename}")
        match = re.match(r'Unified Menu\s*-\s*Week\s*([A-D])\s*-\s*(.+?)\s*\.(pdf|xlsx|xls)', filename, re.IGNORECASE)
        if not match:
            print(f"Skipping file with invalid name format: {filename}")
            continue

        groups = match.groups()
        print(f"Regex groups captured: {groups}")
        week, filename_menu_type = groups[:2]
        menu_type = map_menu_type(filename_menu_type)
        if not menu_type or menu_type not in menu_types or week not in weeks:
            print(
                f"Invalid menu_type '{filename_menu_type}' (mapped to {menu_type}) or week '{week}' in file: {filename}")
            continue

        try:
            file_json = process_file(file_path, prompt)

            if menu_type in file_json:
                if "common_items" in file_json[menu_type]:
                    aggregated_json[menu_type]["common_items"] = file_json[menu_type]["common_items"]
                if week in file_json[menu_type] and "schedule" in file_json[menu_type][week]:
                    aggregated_json[menu_type][week]["schedule"] = file_json[menu_type][week]["schedule"]
            else:
                print(f"Warning: {menu_type} not found in {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

    return aggregated_json


# Script to process all files in a directory
def process_directory(directory, output_file="menu_output.json"):
    try:
        with open("prompt.txt", "r") as f:
            prompt = f.read()
    except FileNotFoundError:
        print("Error: prompt.txt not found")
        return

    file_paths = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.pdf', '.xlsx', '.xls')):
            file_path = os.path.join(directory, filename)
            file_paths.append((filename, file_path))

    if not file_paths:
        print(f"No valid files found in directory: {directory}")
        return

    result = process_files(file_paths, prompt)

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Aggregated JSON saved to {output_file}")
