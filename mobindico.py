import urllib2, simplejson
from flask import Flask, render_template, request, json, jsonify
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/agenda')
def agenda():
    return render_template('agendaConference.html')

@app.route('/conference')
def conference():
    return render_template('conference.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/contribution')
def contribution():
    return render_template('contribution.html')

@app.route('/contributionAgenda')
def contributionAgenda():
    return render_template('contribution-agenda.html')

@app.route('/agendaTemplate')
def agendaTemplate():
    return render_template('agenda-template.html')

@app.route('/break')
def breakTemplate():
    return render_template('break.html')

@app.route('/slotsList')
def slotsList():
    return render_template('slots-list.html')

@app.route('/daysPage')
def daysPage():
    return render_template('days-page.html')

@app.route('/daysList')
def daysList():
    return render_template('days-list.html')

@app.route('/confList')
def confList():
    return render_template('conferenceList.html')

@app.route('/selectedDay')
def selectedDay():
    return render_template('selected-day.html')
@app.route('/agendaContribution')
def agendaContribution():
    return render_template('agendaContribution.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/getConferenceTT', methods=['GET'])
def timetable():
    confID = request.args.get('confID')
    confTitle = request.args.get('confTitle')
    confDate = request.args.get('confDate')
    req = urllib2.Request('http://pcuds43.cern.ch/indico/export/timetable/'+confID+'.json?ak=acde03d4-6145-4a16-9155-f785cdf75cc1')
    opener = urllib2.build_opener()
    f = opener.open(req)
    test = simplejson.load(f)
    if mongo.db.conferences.find({'id':confID}).count() == 0:
        mongo.db.conferences.save({'id':confID, 'title':confTitle, 'date':confDate})
        mongo.db.conferences.update({'id':confID},{'$set': {'days' : test['results'][confID]}})
        return json.dumps(mongo.db.conferences.find({'id':confID},{'_id':0})[0])
    else:
        print('already in DB')
        return json.dumps(mongo.db.conferences.find({'id':confID},{'_id':0})[0])

@app.route('/getConferenceInfo', methods=['GET'])
def ConfInfo():
    confID = request.args.get('confID')
    req = urllib2.Request('http://pcuds43.cern.ch/indico/export/event/'+confID+'.json?ak=acde03d4-6145-4a16-9155-f785cdf75cc1')
    opener = urllib2.build_opener()
    f = opener.open(req)
    return json.dumps(simplejson.load(f))

@app.route('/getConfInDB', methods=['GET'])
def getConfInDB():
    if mongo.db.conferences.find().count()>0:
        return json.dumps(list(mongo.db.conferences.find({},{'_id':0,'id':1,'title':1, 'date':1})))
    else:
        return json.dumps('')


@app.route('/save', methods=['POST'])
def save():
    mongo.db.users.update({'name' : 'claude'},{'$set' : {'agenda' : json.loads(request.form['agenda'])}})
    return ''


@app.route('/load', methods=['GET'])
def load():
    return json.dumps(mongo.db.users.find({'name':'claude'},{'_id':0, 'agenda':1})[0])

if __name__ == '__main__':
    app.run(debug=True, host="pcuds43.cern.ch")