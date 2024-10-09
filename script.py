import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import cairosvg
import PyPDF2
from PIL import Image
# import argparse

# parser = argparse.ArgumentParser(description='Descargar imágenes SVG de una página de MuseScore.')
# parser.add_argument('url', type=str, help='URL de la página de MuseScore')
# args = parser.parse_args()

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')

output_dir = "sheets"
os.makedirs(output_dir, exist_ok=True)

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url_user = input("Ingresa la url de la página de MuseScore: ")
    print("Cargando página, esto puede demorar...")
    
    # driver.get(args.url)
    driver.get(url_user)
    driver.fullscreen_window()

    print("Página cargada correctamente")
    scroller = driver.find_element("id", "jmuse-scroller-component")
    divs = scroller.find_elements("xpath", ".//div[contains(@class, 'EEnGW')]")  

    svg_filenames = []
    png_filenames = []

    print("Descargando imágenes")
    for index, div in enumerate(divs):
        driver.execute_script("arguments[0].scrollIntoView();", div)

        img_tags = div.find_elements("tag name", "img")  
        for img in img_tags:
            img_url = img.get_attribute('src')  
            if img_url and '.svg' in img_url:  
                img_data = requests.get(img_url)
                if img_data.status_code == 200:
                    img_filename = os.path.basename(img_url.split('?')[0])
                    with open(img_filename, 'wb') as handler:
                        handler.write(img_data.content)
                    svg_filenames.append(img_filename)
            elif img_url and '.png' in img_url:
                img_data = requests.get(img_url)
                if img_data.status_code == 200:
                    img_filename = os.path.basename(img_url.split('?')[0])
                    with open(img_filename, 'wb') as handler:
                        handler.write(img_data.content)
                    png_filenames.append(img_filename)

    pdf_filename = pdf_filename = os.path.join(output_dir, f"{driver.title}.pdf")
    temp_pdf_filenames = []
    temp_png_filenames = []

    print("Convertiendo imagenes PDF")
    if svg_filenames:
        for svg_file in svg_filenames:
            temp_pdf_file = svg_file.replace('.svg', '.pdf')
            cairosvg.svg2pdf(url=svg_file, write_to=temp_pdf_file)
            temp_pdf_filenames.append(temp_pdf_file)

        print("Combinando imagenes PDF")
        merger = PyPDF2.PdfMerger()
        for pdf_file in temp_pdf_filenames:
            merger.append(pdf_file)
        merger.write(pdf_filename)
        merger.close()

        for svg_file in svg_filenames:
            os.remove(svg_file)
        for pdf_file in temp_pdf_filenames:
            os.remove(pdf_file)

    elif png_filenames:
        temp_pdf_png_filenames = []
        for png_file in png_filenames:
            temp_pdf_png_file = png_file.replace('.png', '.pdf')
            image = Image.open(png_file)
            image.save(temp_pdf_png_file, "PDF", resolution=100.0)
            temp_pdf_png_filenames.append(temp_pdf_png_file)

        print("Combinando imagenes PDF")
        merger = PyPDF2.PdfMerger()
        for pdf_file in temp_pdf_png_filenames:
            merger.append(pdf_file)
        merger.write(pdf_filename)
        merger.close()
        for png_file in png_filenames:
            os.remove(png_file)
        for pdf_file in temp_pdf_png_filenames:
            os.remove(pdf_file)


    else:
        print("No se encontraron archivos SVG para convertir.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()

print("Script finalizado.")
