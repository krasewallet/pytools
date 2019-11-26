#coding:utf-8
from pyquery import PyQuery
from urllib.parse import urlparse
from pathlib import Path
import requests,ctypes,random,os,sys

def wallpaperDownload(folder):
	wallpaperSiteUrl = "https://wallhaven.cc/search?categories=111&purity=100&ratios=16x9%2C16x10&sorting=random&order=desc"
	content = requests.get(wallpaperSiteUrl,verify = False).content.decode()
	doc = PyQuery(content)
	preview = random.choice(doc("figure .preview"))
	href = PyQuery(preview).attr("href")
	content = requests.get(href,verify = False).content.decode()
	doc = PyQuery(content)
	img = PyQuery(doc("#wallpaper")).attr("src")
	p = Path(urlparse(img).path)
	save = f"{folder}\\{p.name}"
	print(img,p,save)
	response = requests.get(img,verify = False)
	if response.status_code == 200:
		with open(save,'wb') as f:
			f.write(response.content)
	else:
		save = wallpaperDownload()
	return save

def set_wallpaper(picpath):	
	SPI_SETDESKWALLPAPER = 20
	ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, picpath , 0)

if __name__ == '__main__':
	img = wallpaperDownload(sys.argv[1])
	if os.path.exists(img):
		set_wallpaper(img)
