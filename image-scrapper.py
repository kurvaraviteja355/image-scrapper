from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = r"C:\Users\raviteja.kurva\.wdm\drivers\chromedriver\win32\103.0.5060.134\chromedriver.exe"



options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])

wd = webdriver.Chrome(PATH, chrome_options=options)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?q=tchibo+coffee+package+side+view&tbm=isch&hl=en&chips=q:tchibo+coffee+package+side+view,online_chips:tchibo+exclusive:7EgVylLsYo8%3D,online_chips:instant+coffee:nbHaRssmuK8%3D,online_chips:tchibo+gold+selection:6IajI_ztf9g%3D&rlz=1C1GCEU_deDE972DE973&sa=X&ved=2ahUKEwjSnKSW3535AhVC0bsIHWBLCs4Q4lYoA3oECAEQLg&biw=1519&bih=754"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "a") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 55)

for i, url in enumerate(urls):
	download_image("tchibo-images/", url, str('gfhfhffhfh_') + str(i)  + ".jpg")

wd.quit()