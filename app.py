from flask import Flask, render_template

from urllib.request import urlopen
import xmltodict
import datetime as dt

stop_509east = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13369&routeTag=509"
stop_511south = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13672&routeTag=511"
stop_511north = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=0100&routeTag=511"
stop_510north = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=10777&routeTag=510"
stop_121east = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=15504&routeTag=121"
stops = [stop_509east,stop_511north,stop_511south,stop_510north,stop_121east]
dirTags = {"511_1_511":"511 North  Bathurst @ Fort York",
           "511_0_511":"511 South Bathurst @ Fort York",
           "509_0_509":"509 East Queens Quay @ Dan Leckie",
           "121_0_121A":"121 East Fort York @ Bathurst",
           "121_0_121B":"121 East Fort York @ Bathurst",
           "510_1_510A": "510 North Spadina @ Fort York",
           "510_1_510B": "510 North Spadina @ Fort York"}

timeList= {"511_1_511":"","511_0_511":"","509_0_509":"","121_0_121A":"","510_1_510A":""}





app = Flask(__name__)

@app.route('/')
def index():
    route0=""
    route1=""
    route2=""
    route3=""
    route4=""
    route5=""
    for stopnum,item in enumerate(stops):
        file = urlopen(item)
        data = file.read()
        file.close()
        data_dict = xmltodict.parse(data)
        try:
            preds = data_dict['body']['predictions']['direction']['prediction']
        except:
            preds = data_dict['body']['predictions']['direction'][1]['prediction']

        arrtimes=[]
        
        for ind,vehicle in enumerate(preds):
            arr = dt.datetime.strptime(str(int(int(vehicle['@seconds']) / 60)) + ":" +
                                       str(int(int(vehicle['@seconds']) % 60)),"%M:%S")
            arrtimes.append(arr.strftime("%M:%S"))
        dirTag = vehicle['@dirTag']
        timeList[dirTag] = arrtimes
        try:
            route = ""
            times = ""
            route+= str(dirTags[dirTag])
            times+= str(timeList[dirTag])
        except:
            continue
        if stopnum == 0:
            route0 = route
            times0 = times
        if stopnum == 1:
            route1 = route
            times1 = times
        if stopnum == 2:
            route2 = route
            times2 = times
        if stopnum == 3:
            route3 = route
            times3 = times
        if stopnum == 4:
            route4 = route
            times4 = times
        
    return render_template('index.html',route0=route0,route1=route1,
                           route2=route2,route3=route3,route4=route4,times0=times0,
                           times1=times1,times2=times2,times3=times3,times4=times4)
    #return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
