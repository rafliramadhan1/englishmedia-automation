import os
import requests
import urllib.parse
import subprocess
import time
import shutil


from bs4 import BeautifulSoup
from moviepy.editor import *


path = "C:/EnglishMedia/path"
path_out = "C:/EnglishMedia/path/out"


def download_videos(phrases):
	index = 100
	for item in phrases:

		url = requests.get(item, stream=True)

		soup = BeautifulSoup(url.content,'html.parser')

		item = item[31:].replace('%20', ' ').replace('%3F', '').replace('%27', '').replace('%21', '')

		if "&p=" in item:
			item = item[:item.index("&p=")].strip()
		else:
			item = item

		os.mkdir(f"output/{item}")

		movie_title = []


		for mt in soup.find_all("div", {"class": "title ab fw5 p025 px05 tal"}):
			movie_title.append(mt.text)

		download_url  = []
		for du in soup.find_all("a", href=True):
			download_url.append(du["href"])

		download_url_2 = list(dict.fromkeys(download_url[214:254]))

		video = {}

		for key in download_url_2:
			for value in movie_title:
				video[key] = value
				movie_title.remove(value)
				break

		for data1, data2 in video.items():
			final_download_url = "https://y.yarn.co" + data1[10:] + ".mp4"
			print (final_download_url)
			response = requests.get(final_download_url, stream=True)

			video_title = str(index) + "video.mp4"

			with open(video_title, 'wb') as f:
				for chunk in response.iter_content(chunk_size=1024*1024):
					if chunk:
						f.write(chunk)


			os.rename(video_title, f"output/{item}/{video_title}")

			print(f"Video title: {data2}")

			index+=1

			print (video.values())
			with open("video_data.txt", "w") as f:
				for title in video.values():
					f.write(title)
					f.write("\n")


		os.rename("video_data.txt", f"output/{item}/video_data.txt")
		url.close()

		print(f"<{'-'* 55}>")


def edit_video_data():

	for folder in os.listdir("output"):
		os.chdir(f"{path}/output/{folder}")
		data = []
		with open("video_data.txt") as fl:
			for text in fl.readlines():

				y = x.replace(":", " -").replace(".", "").replace(",", "").replace("&", "").strip()
				if "- S0" in y:
					n = y[:y.find("- S0")]
					data.append(n)
				else:
					data.append(y)

		with open("video_data.txt", "w") as fl:
			for x in data:
				fl.write(x)
				fl.write("\n")


def edit_videos():

	index = 0
	os.chdir(path)
	for folder in os.listdir("output"):

		src = f"{path}/myfont.ttf"
		dst = f"{path}/output/{folder}/myfont.ttf"
		shutil.copy(src, dst)


		os.chdir(f"{path}/output/{folder}")

		os.mkdir("finished")

		video_title = []
		video_title_1 = [x for x in os.listdir() if x.endswith(".mp4")]

		with open(f"video_data.txt", "r") as fl:
			for x in fl.readlines():
				video_title.append(x.replace("\n", ""))

		video_data = {}
		for key in video_title_1:
			for value in video_title:
				video_data[key] = value
				video_title.remove(value)
				break

		for data1, data2 in video_data.items():
			out_vid = f"out-vid{index}.mp4"
			out_vid1 = f"1-out-vid{index}.mp4"
			out_vid2 = f"2-out-vid{index}.mp4"
			out_vid3 = f"3-out-vid{index}.mp4"

			os.system(f"ffmpeg -y -i {data1} -vf scale=1280:720 -preset slow -crf 18 {out_vid1}")
			os.system(f'ffmpeg -y -i {out_vid1} -filter:a "volume=4.0" {out_vid2}')
			os.system(f'ffmpeg -y -i {out_vid2} -filter:v "drawtext=text={data2}\
				:x=(w-text_w)/2:y=9*(h-text_h)/10:fontsize=45:fontcolor=white:fontfile=myfont.ttf\
				:box=1:boxcolor=black@0.5:boxborderw=10" -c:a copy -c:v libx264 -preset slow -crf 18 {out_vid3}')

			os.system(f'ffmpeg -y -i {out_vid3} -vf "scale=1280:720, setsar=1" {out_vid}')
			os.rename(f"{out_vid}", f"finished/{out_vid}")
			os.remove(out_vid1); os.remove(out_vid2); os.remove(out_vid3)
			index+=1


def concatenate_videos():
	os.chdir(path)
	for folder in os.listdir("output"):
		os.chdir(f"{path}/output/{folder}/finished")

		result = concatenate_videoclips([VideoFileClip(x) for x in os.listdir() if x.endswith(".mp4")])
		result.write_videofile(f"{folder}.mp4")
		os.rename(f"{folder}.mp4", f"{path_out}/{folder}.mp4")

