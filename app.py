from flask import Flask, render_template
from urllib.request import urlopen
import xmltodict
stop_509east = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13369&routeTag=509"
stop_511south = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13672&routeTag=511"
stop_511north = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=0100&routeTag=511"
stop_510north = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=10777&routeTag=510"
stop_121east = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=15504&routeTag=121"
stop_509west = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=13362&routeTag=509"
stops = [stop_509east,stop_509west,stop_511north,stop_511south,stop_510north,stop_121east]
routes = {"511_1_511":"511 North","511_0_511":"511 South",
           "509_0_509":"509 East","509_1_509":"509 West",
           "121_0_121":"121 East","510_1_510":"510 North"}
close_stop = {"511_1_511":"Bathurst @ Fort York","511_0_511":"Bathurst @ Fort York",
           "509_0_509":"Queens Quay @ Dan Leckie","509_1_509":"Queens Quay @ Bathurst",
           "121_0_121":"Fort York @ Bathurst","510_1_510":"Spadina @ Fort York"}
timeList= {"511_1_511":["N/A","N/A","N/A"],"511_0_511":["N/A","N/A","N/A"],"509_0_509":["N/A","N/A","N/A"],
           "509_1_509":["N/A","N/A","N/A"],"121_0_121":["N/A","N/A","N/A"],"510_1_510":["N/A","N/A","N/A"]}
keyList = ["511_1_511","509_0_509","510_1_510","511_0_511","509_1_509","121_0_121"]

app = Flask(__name__)

@app.route('/')
def index():
    error = False
    for stopnum,item in enumerate(stops):
        arrtimes = []
        try:
            file = urlopen(item)
            data = file.read()
            file.close()
            data_dict = xmltodict.parse(data)
        except:
            error = True
            print("Network error")

        if not error:
            try:
                preds = data_dict['body']['predictions']['direction']['prediction']
            except:
                try:
                    preds = data_dict['body']['predictions']['direction'][1]['prediction']
                except:
                    error = True
                    print("XML parsing error")
                    continue

        if not error:
            try:
                for ind,vehicle in enumerate(preds):
                    mins = str(min(int(int(vehicle['@seconds']) / 60),59))
                    arr = "{0} min".format(mins)
                    arrtimes.append(arr)

                dirTag = preds[0]['@dirTag'].rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                timeList[dirTag] = arrtimes
                while len(timeList[dirTag]) <3:
                    timeList[dirTag].append("N/A")
                #print(timeList)
            except:
                print("Error updating time lists")
    return render_template('index.html',
        route0=routes[keyList[0]],stop0=close_stop[keyList[0]],times00=timeList[keyList[0]][0], times01=timeList[keyList[0]][1], times02=timeList[keyList[0]][2],
        route1=routes[keyList[1]],stop1=close_stop[keyList[1]],times10=timeList[keyList[1]][0], times11=timeList[keyList[1]][1], times12=timeList[keyList[1]][2],
        route2=routes[keyList[2]],stop2=close_stop[keyList[2]],times20=timeList[keyList[2]][0], times21=timeList[keyList[2]][1], times22=timeList[keyList[2]][2],
        route3=routes[keyList[3]],stop3=close_stop[keyList[3]],times30=timeList[keyList[3]][0], times31=timeList[keyList[3]][1], times32=timeList[keyList[3]][2],
        route4=routes[keyList[4]],stop4=close_stop[keyList[4]],times40=timeList[keyList[4]][0], times41=timeList[keyList[4]][1], times42=timeList[keyList[4]][2],
        route5=routes[keyList[5]],stop5=close_stop[keyList[5]],times50=timeList[keyList[5]][0], times51=timeList[keyList[5]][1], times52=timeList[keyList[5]][2],)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
