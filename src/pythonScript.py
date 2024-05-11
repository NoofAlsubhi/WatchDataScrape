from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.parse import urlparse
from bs4 import Tag

def extract_watch_urls(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")
    links = []
    for link in soup.find_all(attrs={"class": "products columns-3"})[0].find_all("a"):
        links.append(link.attrs["href"])
    return links



def extract_reference_number(soup):
    header_elements = soup.find_all('h1')
    reference_number = header_elements[1].text.strip() if len(header_elements) >= 2 else ''
    if reference_number == "":
        info_section = soup.find('section', id='info')
        if info_section:
            p_tag = info_section.find('p')
            if p_tag:
                reference_number = p_tag.text.strip()
    return reference_number



def extract_brand(watch_url):
    parsed_url = urlparse(watch_url)
    brand = parsed_url.netloc.split('.')[0]
    return brand



def extract_models(soup):
    parent_model = " "  # Default value for parent model
    specific_model = " "  # Default value for specific model

    breadcrumbs_nav = soup.find('nav', class_='woocommerce-breadcrumb')
    if breadcrumbs_nav:
        breadcrumbs_div = breadcrumbs_nav.find('div', class_='o-wrapper o-wrapper--to@lg')
        if breadcrumbs_div:
            breadcrumb_links = breadcrumbs_div.find_all('a')
            breadcrumb_spans = breadcrumbs_div.find_all('span')
            if len(breadcrumb_links) >= 2:
                parent_model = breadcrumb_links[-1].text.strip()
            if len(breadcrumb_spans) >= 2:
                specific_model = breadcrumb_spans[-1].next_sibling.strip()

    if parent_model == " ":
        info_section = soup.find('section', id='info')
        if info_section:
            h1_tag = info_section.find('h1')
            if h1_tag:
                parent_model = h1_tag.text.strip()

    if specific_model == " ":
        if info_section:
            p_tag = info_section.find('p')
            if p_tag:
                specific_model = p_tag.text.strip()

    return parent_model, specific_model





def extract_nickname(product_title_element, parent_model):
    nickname = product_title_element.text.strip() if product_title_element else ''
    if nickname == parent_model:
        return ''
    return nickname




def extract_marketing_name(soup):
    parent_model = extract_models(soup)[0]  # Extract the parent model from the soup
    if 'Special Edition' in parent_model:
        return "Special Edition"
    else:
        return ""



def extract_currency(soup):
    currency_tag = soup.find_all("span", {"class": "woocommerce-Price-currencySymbol"})
    currency = currency_tag[0].text.strip() if currency_tag else ""
    return currency




def extract_price(soup):
    price_tag = soup.find('bdi')
    price_text = price_tag.get_text(strip=True) if price_tag else ''
    price = re.sub(r'[^\d]', '', price_text)
    return price




def extract_image_url(soup):
    images = soup.find_all('img')
    image_url = ''
    for image in images:
        if image['src'].endswith('.jpg'):
            image_url = image['src']
            break
    return image_url


def extract_made_in(soup):
    return "Switzerland"



def extract_case_material(soup):
    case_material = ''

    # Find all div elements with class 'c-tech-details__wrapper'
    case_details = soup.find_all("div", class_="c-tech-details__wrapper")

    # Iterate over each div element
    for detail in case_details:
        # Find all list items within the div
        list_items = detail.find_all("li")
        # Iterate over each list item
        for li in list_items:
            # Check if the text contains 'case' or 'bracelet' (case-insensitive)
            if 'case' in li.text.lower() or 'bracelet' in li.text.lower():
                # Check if the text mentions "Case back"
                if 'case back' not in li.text.lower():
                    # Extract the text of the list item
                    case_material = li.get_text(strip=True)
                    # Break the loop if found
                    break
        # Break the loop if found
        if case_material != '':
            break

    return case_material






def extract_diameter(soup):
    diameter = ''
    case_materials = soup.find_all("div", {"class": 'c-tech-details__wrapper'})
    for element in case_materials:
        for item in element:
            if isinstance(item, Tag) and 'case' in item.text.lower():
                bullet_point = item.find_next("li", text=lambda text: "mm" in text.lower())
                if bullet_point:
                    # Use regular expression to extract digits followed by "mm" and remove "mm"
                    diameter_match = re.search(r'(\d+\.\d+|\d+)\s*mm', bullet_point.text)
                    if diameter_match:
                        # Extract digits only
                        digits = diameter_match.group(1)
                        # Add " mm" after the digits
                        diameter = digits + " mm"
                break
        if diameter:
            break
    return diameter





def extract_caseback(soup):
    case_back = ""  # Default value for case back

    # Find the "Case" or "Case & Bracelet" section
    case_section = soup.find(text=["Case", "Case & Bracelet"])

    if case_section:
        # Find all the <li> tags within the "Case" or "Case & Bracelet" section
        list_items = case_section.find_next('ul').find_all('li')

        for li in list_items:
            # Check if the bullet point contains "case back" or "case-back"
            if 'case back' in li.text.lower() or 'case-back' in li.text.lower():
                # Skip the bullet point if it contains the phrase "Perceived height (bezel to case-back)"
                if 'perceived height' not in li.text.lower():
                    case_back = li.text.strip()
                    break

    return case_back




def extract_case_thickness(soup):
    technical_details = soup.find('div', class_='c-tech-details__wrapper')
    case_thickness = ""

    if technical_details:
        case_section = technical_details.find(text=["Case & Bracelet", "Case"])
        if case_section:
            bullet_points = case_section.find_next('ul').find_all('li')
            for bullet_point in bullet_points:
                if 'height' in bullet_point.text.lower():
                    # Use regular expression to extract digits and remove "mm", then add " mm"
                    thickness_match = re.search(r'(\d+\.\d+|\d+)\s*mm', bullet_point.text)
                    if thickness_match:
                        # Extract digits only
                        digits = thickness_match.group(1)
                        # Add " mm" after the digits
                        case_thickness = digits + " mm"
                    break

    return case_thickness


def extract_crystal(soup):
    crystal = ''
    case_materials = soup.find_all("div", {"class": 'c-tech-details__wrapper'})
    for case_material in case_materials:
        if 'case' in case_material.text.lower():
            bullet_points = case_material.find_all('li')
            for bullet_point in bullet_points:
                if 'crystal' in bullet_point.text.lower():
                    crystal = bullet_point.text.strip()
                    break
            if crystal:
                break
    return crystal



def extract_water_resistance(soup):
    water_resistance = ''
    case_materials = soup.find_all("div", {"class": 'c-tech-details__wrapper'})

    for element in case_materials:
        case_text = element.get_text().lower()
        if "case" in case_text or "bracelet" in case_text:
            bullet_points = element.find_all("li")
            for bullet_point in bullet_points:
                bullet_text = bullet_point.get_text().lower()
                if "water-resistance" in bullet_text or "water resistance" in bullet_text:
                    # Extract the water resistance value
                    water_resistance_value = bullet_text.split(':')[1].strip()
                    # Check if the unit is in atmospheres (atm)
                    if 'atm' in water_resistance_value:
                        water_resistance = re.search(r'\d+\s*atm', water_resistance_value).group()
                    else:
                        # Extract the numerical value and convert from meters to atm
                        numeric_value = int(re.search(r'\d+', water_resistance_value).group())
                        # Convert meters to atm (1 atm = 10 m)
                        atm_value = numeric_value // 10
                        water_resistance = f"{atm_value} atm"
                    break
            if water_resistance == '':
                water_resistance = case_text.strip()
            break

    return water_resistance


def extract_dial_color_bracelet_material(soup):
    dial_color = ''
    bracelet_material = ''
    technical_details = soup.find('div', class_='c-tech-details__wrapper')
    for div in technical_details.find_all('div'):
        if 'Dial' in div.text:
            dial_color = div.find_next('ul').text.strip().replace('\n', '')
        elif 'Bracelet' in div.text:
            bracelet_material = div.find_next('ul').text.strip().replace('\n', '')
    return dial_color, bracelet_material




def extract_caliber(soup):
    caliber = None
    movement_section = soup.find(text='Movement')
    if movement_section:
        bullet_points = movement_section.find_next('ul').find_all('li')
        first_bullet_point = bullet_points[0]
        caliber = first_bullet_point.text.strip()
    return caliber if caliber else ''




def extract_power_reserve(soup):
    power_reserve = None
    movement_section = soup.find(text='Movement')
    if movement_section:
        bullet_points = movement_section.find_next('ul').find_all('li')
        for bullet_point in bullet_points:
            if bullet_point.text.strip().startswith('Power-reserve'):
                power_reserve_text = bullet_point.text.strip()
                hours_match = re.search(r'\b(\d+)\s*hours?\b', power_reserve_text)
                if hours_match:
                    power_reserve = hours_match.group(0)
                    break
    return power_reserve if power_reserve else ''



def extract_jewels(soup):
    jewels = None
    technical_details = soup.find('div', class_='c-tech-details__wrapper')
    for detail in technical_details:
        if isinstance(detail, Tag):  # Check if the object is a Tag
            detail_text = detail.get_text().lower()
            if "movement" in detail_text:
                bullet_points = detail.find_all("li")
                for bullet_point in bullet_points:
                    bullet_text = bullet_point.get_text().lower().strip()
                    if "jewels" in bullet_text:
                        jewels_match = re.search(r"\b(\d+)\b", bullet_text)
                        if jewels_match:
                            jewels = jewels_match.group(1)
                            break
        if jewels is None:
            jewels = ""
        return jewels


    


def extract_frequency(soup):
    frequency = ''
    case_materials = soup.find_all('div', {'class': 'c-tech-details__wrapper'})
    for case_material in case_materials:
        for item in case_material:
            if hasattr(item, 'text') and 'Frequency' in item.text:
                match = re.search(r'(\d+\.*\d*)\s*Hz', item.text)
                if match:
                    frequency = match.group(1).strip() + " Hz"
                    break
        if frequency:
            break
    return frequency





def extract_features(soup):
    # Find the technical details section
    technical_details = soup.find('div', class_='c-tech-details__wrapper')
    if technical_details:
        # Find the functions section
        functions_section = None
        for div in technical_details.find_all('div'):
            if 'Functions' in div.text:
                functions_section = div
                break

        # Extract features if functions section is found
        if functions_section:
            # Extract the functions text
            functions_text = functions_section.find_next('ul').text.strip().replace('\n', '')
            return functions_text
    return ""





def extract_description(soup):
    woocommerce_description_element = soup.find('div', class_='woocommerce-product-details__short-description')
    if woocommerce_description_element:
        return woocommerce_description_element.text.strip().replace('\n', '')
    else:
        generic_description_element = soup.find('div', class_='description')
        if generic_description_element:
            return generic_description_element.text.strip().replace('\n', '')
        else:
            return ""
        



def initialize_empty_fields(data, key, num_records):
    for _ in range(num_records):
        data[key].append("")