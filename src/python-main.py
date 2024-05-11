from pythonScript import *
from datetime import datetime
import os


# Main Function
def main():
    data = {
        'reference_number': [],
        'watch_URL': [],
        'type': [],
        'brand': [],
        'year_introduced': [],
        'parent_model': [],
        'specific_model': [],
        'nickname': [],
        'marketing_name': [],
        'style': [],
        'currency': [],
        'price': [],
        'image_URL': [],
        'made_in': [],
        'case_shape': [],
        'case_material': [],
        'case_finish': [],
        'caseback': [],
        'diameter': [],
        'between_lugs': [],
        'lug_to_lug': [],
        'case_thickness': [],
        'bezel_material': [],
        'bezel_color': [],
        'crystal': [],
        'water_resistance': [],
        'weight': [],
        'dial_color': [],
        'numerals': [],
        'bracelet_material': [],
        'bracelet_color': [],
        'clasp_type': [],
        'movement': [],
        'caliber': [],
        'power_reserve': [],
        'frequency': [],
        'jewels': [],
        'features': [],
        'description': [],
        'short_description': []
    }



    # Define the URL for all watches
    url = "https://czapek.com/all-timepieces/"

    # Extract watch URLs
    links = extract_watch_urls(url)

    # Loop through each watch URL
    for watch_url in links:
        # Send a GET request to the watch URL
        result = requests.get(watch_url)
        soup = BeautifulSoup(result.content, "html.parser")

        # Extract and append data to the dictionary
        data['watch_URL'].append(watch_url)
        data['reference_number'].append(extract_reference_number(soup))
        data['brand'].append(extract_brand(watch_url))
        data['marketing_name'].append(extract_marketing_name(soup))
        data['currency'].append(extract_currency(soup))
        data['price'].append(extract_price(soup))
        data['image_URL'].append(extract_image_url(soup))
        data['made_in'].append(extract_made_in(soup))
        data['case_material'].append(extract_case_material(soup))
        data['diameter'].append(extract_diameter(soup))
        data['case_thickness'].append(extract_case_thickness(soup))
        data['caseback'].append(extract_caseback(soup))
        data['crystal'].append(extract_crystal(soup))
        data['water_resistance'].append(extract_water_resistance(soup))
        dial_color, bracelet_material = extract_dial_color_bracelet_material(soup)
        data['dial_color'].append(dial_color)
        data['numerals'].append(dial_color)  # Assigning dial_color to numerals
        data['bracelet_material'].append(bracelet_material)
        data['clasp_type'].append(bracelet_material)  # Assigning bracelet_material to clasp_type
        data['bracelet_color'].append(bracelet_material)
        data['caliber'].append(extract_caliber(soup))
        data['power_reserve'].append(extract_power_reserve(soup))
        data['frequency'].append(extract_frequency(soup))
        data['jewels'].append(extract_jewels(soup))
        data['description'].append(extract_description(soup))
        data['features'].append(extract_features(soup))

        models = extract_models(soup)
        data['parent_model'].append(models[0])
        data['specific_model'].append(models[1])

      # Extract product title element (assuming it exists)
        product_title_element = soup.find('h1')

       # Extract and append nickname and marketing name
        if product_title_element:
            data['nickname'].append(extract_nickname(product_title_element, models[0]))
        else:
            data['nickname'].append('')
        
        
        
        
    initialize_empty_fields(data, 'type', 55)
    initialize_empty_fields(data, 'year_introduced', 55)
    initialize_empty_fields(data, 'style', 55)
    initialize_empty_fields(data, 'case_shape', 55)
    initialize_empty_fields(data, 'case_finish', 55)
    initialize_empty_fields(data, 'between_lugs', 55)
    initialize_empty_fields(data, 'lug_to_lug', 55)
    initialize_empty_fields(data, 'bezel_material', 55)
    initialize_empty_fields(data, 'bezel_color', 55)
    initialize_empty_fields(data, 'weight', 55)
    initialize_empty_fields(data, 'movement', 55)
    initialize_empty_fields(data, 'short_description', 55)
  
 
    # Create DataFrame
    df = pd.DataFrame(data)

    #Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Specify the data directory
    data_directory = "/home/ubuntu/Czapek/data"

    # Modify the CSV file name with timestamp
    csv_filename = f"czapek_{timestamp}.csv"

    # Create the absolute path for the CSV file
    csv_filepath = os.path.join(data_directory, csv_filename)

    # Write DataFrame to CSV
    df.to_csv(csv_filepath, index=False)



if __name__ == "__main__":
    main()
