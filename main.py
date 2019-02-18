import youtube_dl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import sys
import os
import time

channel = sys.argv[1]
scroll_wait = 2

if not os.path.exists("downloads/"):
    print("[Channel Downloader] Downloads folder doesn't exist, creating one.")
    os.makedirs("downloads/")

print("[Channel Downloader] Starting download on '%s'." % channel)

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)

url = ""

if("/channel/" in channel):
    # Get youtube channel name from videos tab
    browser.get(channel) # It's a link
    browser.find_element_by_xpath("//*[@id=\"tabsContent\"]/paper-tab[2]/div").click()
    time.sleep(2)
    url = browser.current_url
    channel = url.split("/")[-2]
elif("/user/" in channel):
    rurl = channel.split("/")
    url = ""
    for p in rurl[:-1]:
        url += p+"/"
    url += "videos"
    channel = url.split("/")[-2]
else:
    url = "https://youtube.com/user/%s/videos" % (channel)
print(url)
print("[Channel Downloader] Loading entire channel page...")

browser.get(url)
time.sleep(3)
source = browser.page_source
if(len(source) < 100000): # Channel doesn't exist
    url = "https://youtube.com/channel/%s/videos" % (channel)
    browser.get(url)
    time.sleep(3)
    source = browser.page_source
    if(len(source)< 100000):
        print("[Channel Downloader] URL: %s" % (url))
        sys.exit("[Channel Downloader] There was an error while loading the channel at the URL above, check if it exists. Exiting.")

if not os.path.exists("downloads/%s/" % (channel)):
    os.makedirs("downloads/%s/" % (channel))

# Get to the bottom of the page, so all videos will load into the source code
lsource = len(source)
while True:
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
    time.sleep(scroll_wait)
    nsource = len(browser.page_source)
    if(nsource == lsource):
        break
    lsource = nsource


print("[Channel Downloader] Fetching video URLs...")
# Parse the HTML to get the video URLs
source = browser.page_source
browser.close()
videos_raw = source.split("href=\"")
videos = []
for link_raw in videos_raw:
    link = link_raw.split("\"")[0]
    if("watch?v=" in link and link not in videos): # Check if it's a youtube video link and if it's not already on the list
        videos.append("https://youtube.com"+link)


# Start download using youtube_dl
downloaded = 0
size = len(videos)
print("[Channel Downloader] %d/%d videos downloaded." % (downloaded, size), end='\r')

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def prog_hook(d):
    if(d['status'] == 'finished'):
        global downloaded
        downloaded += 1
        print("[Channel Downloader] %d/%d videos downloaded." % (downloaded, size), end='\r')

ytd_options = {
        'outtmpl': 'downloads/{}/%(title)s.%(ext)s'.format(channel),
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        'logger': Logger(),
        'progress_hooks': [prog_hook],}

with youtube_dl.YoutubeDL(ytd_options) as dl:
    dl.download(videos)

print("[Channel Downloader] Finished download %d videos from '%s'!" % (size, channel))
