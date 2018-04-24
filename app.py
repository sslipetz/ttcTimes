from flask import Flask, render_template

from urllib.request import urlopen
import xmltodict
import datetime as dt

stop_509east = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13369&routeTag=509"
stop_511south = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13672&routeTag=511"
stop_511north = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=0100&routeTag=511"
stop_510north = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=10777&routeTag=510"
stop_121east = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=15504&routeTag=121"
stop_509west = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13362&routeTag=509"
stops = [stop_509east,stop_509west,stop_511north,stop_511south,stop_510north,stop_121east]
dirTags = {"511_1_511":"511 N- Bathurst @ Fort York",
           "511_0_511":"511 S- Bathurst @ Fort York",
           "509_0_509":"509 E- Queens Qy. @ Dan Leckie",
           "509_1_509":"509 W- Queens Qy. @ Bathurst",
           "121_0_121":"121 E- Fort York @ Bathurst",
           "510_1_510":"510 N- Spadina @ Fort York"}
timeList= {"511_1_511":"","511_0_511":"","509_0_509":"","509_1_509":"","121_0_121":"","510_1_510":""}
keyList = ["511_1_511","509_0_509","510_1_510","511_0_511","509_1_509","121_0_121"]

app = Flask(__name__)

@app.route('/')
def index():
    for stopnum,item in enumerate(stops):
        arrtimes = []
        file = urlopen(item)
        data = file.read()
        file.close()
        data_dict = xmltodict.parse(data)
        try:
            preds = data_dict['body']['predictions']['direction']['prediction']
        except:
            preds = data_dict['body']['predictions']['direction'][1]['prediction']

        for ind,vehicle in enumerate(preds):
            arr = dt.datetime.strptime(str(int(int(vehicle['@seconds']) / 60)) + ":" +
                                       str(int(int(vehicle['@seconds']) % 60)),"%M:%S")
            arrtimes.append(arr.strftime("%M:%S"))

        dirTag = vehicle['@dirTag'].rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        timeList[dirTag] = arrtimes
        while len(timeList[dirTag])<3:
            timeList[dirTag].append("")
        print(timeList)

    return render_template('index.html',
        route0=dirTags[keyList[0]],times00=timeList[keyList[0]][0], times01=timeList[keyList[0]][1], times02=timeList[keyList[0]][2],
        route1=dirTags[keyList[1]],times10=timeList[keyList[1]][0], times11=timeList[keyList[1]][1], times12=timeList[keyList[1]][2],
        route2=dirTags[keyList[2]],times20=timeList[keyList[2]][0], times21=timeList[keyList[2]][1], times22=timeList[keyList[2]][2],
        route3=dirTags[keyList[3]],times30=timeList[keyList[3]][0], times31=timeList[keyList[3]][1], times32=timeList[keyList[3]][2],
        route4=dirTags[keyList[4]],times40=timeList[keyList[4]][0], times41=timeList[keyList[4]][1], times42=timeList[keyList[4]][2],
        route5=dirTags[keyList[5]],times50=timeList[keyList[5]][0], times51=timeList[keyList[5]][1], times52=timeList[keyList[5]][2],)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
