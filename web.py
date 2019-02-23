from flask import Flask, request
import json
import requests
import onesignal as onesignal_sdk

app = Flask(__name__)

@app.route('/',methods=['POST'])
def foo():
   youtubeData = json.loads(request.data)
   if(youtubeData['title'].lower().find('trailer')==-1):
       return "OK"
   omdbData = getOmdbData(youtubeData['title'])
   print(omdbData)
   if(omdbData['Response']=='False'):
       return "OK"
   sendNotification(youtubeData,omdbData)
   return "OK"

def getOmdbData(title):
    i = 1000
    title = title.replace('Trailer','*')
    title = title.replace('trailer','*')
    title = title.replace('|','*')
    title = title.replace('(','*')
    title = title.replace('#','*')
    title = title.replace('Movie','*')
    title = title.replace('movie','*')
    title = title.replace(':','*')
    i = title.find('*')
    title = title[:i].strip()
    title = title.replace(' ','+').lower()
    url = 'https://www.omdbapi.com/?t=' + title + '&apikey=c8ff786a'
    response = requests.get(url)
    response.raise_for_status() # optional but good practice in case thefails!
    return response.json()

def sendNotification(youtubeData,omdbData):
    onesignal_client = onesignal_sdk.Client()
    onesignal_client.user_auth_key = "XXXX"
    onesignal_client.app = {"app_auth_key": "YYYY", "app_id": "ZZZZ"}
    new_notification = onesignal_sdk.Notification(contents={"en": "{}".format(youtubeData['title'])})

    new_notification.set_parameter("headings", {"en": "{}".format(youtubeData['channelTitle'])})
    new_notification.set_parameter("data", { "type" : "2", "movieId" : "{}".format(omdbData['imdbID']), "videoId" : "{}".format(youtubeData['id']), "webpageUrl" : "https://www.bbc.com/news/world-europe-47126440" })
    new_notification.set_parameter("big_picture", "{}".format(youtubeData['highThumbnail']))
    new_notification.set_parameter("large_icon", "https://yt3.ggpht.com/a-/AAuE7mA31JFXfi7gZyjlR_RAJAa5ctCJlemkqgDF=s288-mo-c-c0xffffffff-rj-k-no")
    # new_notification.set_included_segments(["All"])
    new_notification.set_target_devices(["DDDD"])
    onesignal_response = onesignal_client.send_notification(new_notification)
    print(onesignal_response.status_code)
    print(onesignal_response.json())

if __name__ == '__main__':
   app.run()
