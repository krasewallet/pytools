#coding:utf-8
from pyquery import PyQuery
from urllib.parse import urlparse
from pathlib import Path
import requests,win32api,win32con,win32gui,re,random,os,sys

def wallpaperDownload():
	wallpaperSiteUrl = "https://wallhaven.cc/random"
	wallpaperPicRepoBase = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{0}.jpg"
	picRgx = re.compile(r'data-wallpaper-id="(\d+)"')
	content = requests.get(wallpaperSiteUrl,verify = False).content.decode()
	doc = PyQuery(content)
	preview = random.choice(doc("figure .preview"))
	href = PyQuery(preview).attr("href")
	content = requests.get(href,verify = False).content.decode()
	doc = PyQuery(content)
	img = PyQuery(doc("#wallpaper")).attr("src")
	p = Path(urlparse(img).path)
	save = f"D:\\Users\\Administrator\\Pictures\\{p.name}"
	print(img,p,save)
	response = requests.get(img,verify = False)
	if response.status_code == 200:
		with open(save,'wb') as f:
			f.write(response.content)
	else:
		save = wallpaperDownload()
	return save

def set_wallpaper(picpath):	
	if sys.platform == 'win32':
		import win32api, win32con, win32gui
		k = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Control Panel\Desktop', 0, win32con.KEY_ALL_ACCESS)
		curpath = win32api.RegQueryValueEx(k, 'Wallpaper')[0]
		if curpath == picpath:
			pass
		else:
			win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, picpath, 1+2)
		win32api.RegCloseKey(k)
	else:
		curpath = commands.getstatusoutput('gsettings get org.gnome.desktop.background picture-uri')[1][1:-1]
		if curpath == picpath:
			pass
		else:
			commands.getstatusoutput('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri "%s"' % (picpath))

if __name__ == '__main__':
	img = wallpaperDownload()
	if os.path.exists(img):
		set_wallpaper(img)