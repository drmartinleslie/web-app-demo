from flask import Flask, render_template, request
from pymongo import MongoClient
from collections import defaultdict

app = Flask(__name__)
mc = MongoClient()
db = mc.fish_db
app.debug = True


@app.route('/')
def index():
    return render_template('index.html', numEntries=db.fish_counts.count())


@app.route('/submit')
def submit():
        species = request.args.get("Species")
        count = request.args.get("Number")
        post = {"species": species, "count": count}
        db.fish_counts.insert_one(post)
        return "You saw {} {}".format(count, species)

@app.route('/analysis')
def analysis():
        data = db.fish_counts.find()
        fishCountDict = defaultdict(int)
        recordCountDict = defaultdict(int)
        for record in data:
            recordCountDict[record['species']] += 1
            fishCountDict[record['species']] += int(record['count'])
        averageDict = {}
        for species in recordCountDict:
            averageDict[species] = fishCountDict[species] / float(recordCountDict[species])
        print data
        return "Average {} black cod and {} sand dabs".format(averageDict['Black Cod'], averageDict['Sand Dab'])


if __name__ == "__main__":
    app.run(host='0.0.0.0')