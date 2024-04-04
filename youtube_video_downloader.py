from pytube import YouTube
import re
import shutil


# functions
def dict_appender(text: str, dict: dict, arg: str, att: str):
    """This function de:
    * uses regex to extract two substrings
    * gather the 2 substrings in a tuple
    * append it to a dict
    """
    itag = re.search(r'itag="([^"]+)', text).group(1)
    res = re.search(rf'{att}="([^"]+)', text).group(1)
    dict[arg].append((itag, res))


url = input("URL: ")
video = YouTube(url)
video_streams = video.streams

# Title of the video
name = video.title

# Thumbnail_url
tn = video.thumbnail_url

# order types of downloads: by type (audio/video), then in video by progressive (w\audio, or not)
# save itag and res/abr

types = {"v": [], "vwa": [], "a": []}
for ind, i in enumerate(video_streams):
    i = str(i)
    if 'type="video"' in i:
        if 'progressive="True"' in i:
            dict_appender(i, types, "v", "res")
        else:
            dict_appender(i, types, "vwa", "res")
    else:
        dict_appender(i, types, "a", "abr")


print("video:")
ind = 1
l = []
unique = [[], [], []]
for i in types["v"]:
    if i[1] not in unique[0]:
        unique[0].append(i[1])
        l.append(i[0])
        print(f"\t{ind}. {i[1]}")
        ind += 1

print("video without audio:")
for i in types["vwa"]:
    if i[1] not in unique[1]:
        unique[1].append(i[1])
        l.append(i[0])
        print(f"\t{ind}. {i[1]}")
        ind += 1
print("audio only:")
for i in types["a"]:
    if i[1] not in unique[2]:
        unique[2].append(i[1])
        l.append(i[0])
        print(f"\t{ind}. {i[1]}")
        ind += 1
print(l)
code = int(input("choose: "))

video_streams.get_by_itag(l[code - 1]).download("temp")

print("Downloaded successfully!")
shutil.rmtree("temp")
