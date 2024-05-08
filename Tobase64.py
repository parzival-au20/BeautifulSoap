import requests
import base64

def url_to_base64(image_url):
    # Resmi URL'den indirin
    response = requests.get(image_url, verify=False)
    
    # İndirilen veriyi base64'e dönüştürün
    base64_image = base64.b64encode(response.content).decode('utf-8')
    
    return base64_image

# Base64'e dönüştürmek istediğiniz resmin URL'si
image_url = "https://assets.verticalmag.com/wp-content/uploads/2023/02/THC-Dakar2023-0228.jpg"

# Fonksiyonu kullanarak resmi base64'e dönüştürün
base64_image = url_to_base64(image_url)

print(base64_image)
