from flask import Flask, request, render_template, redirect, url_for
import json, plotly, csv
from datetime import datetime
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


app = Flask(__name__)


def peakTimeChart(oneplusCampaign, samsungCampaign): #pie chart

    morning1 = datetime.strptime('06:00:00', '%H:%M:%S').time()
    morning2 = datetime.strptime('11:59:59', '%H:%M:%S').time()

    afternoon1 = datetime.strptime('12:00:00', '%H:%M:%S').time()
    afternoon2 = datetime.strptime('16:59:59', '%H:%M:%S').time()

    evening1 = datetime.strptime('17:00:00', '%H:%M:%S').time()
    evening2 = datetime.strptime('19:59:59', '%H:%M:%S').time()

    night1 = datetime.strptime('20:00:00', '%H:%M:%S').time()
    night2 = datetime.strptime('23:59:59', '%H:%M:%S').time()

    midnight1 = datetime.strptime('00:00:00', '%H:%M:%S').time()
    midnight2 = datetime.strptime('05:59:59', '%H:%M:%S').time()

    OPtime = [0, 0, 0, 0, 0] #morning, afternooon, evening, night, midnight
    for x in range(0, len(oneplusCampaign[0])):
        tempDate = datetime.strptime(oneplusCampaign[4][x], '%Y-%m-%d %H:%M:%S').time()
        if (morning1 <= tempDate < morning2):
            OPtime[0] += 1
        elif (afternoon1 <= tempDate < afternoon2):
            OPtime[1] += 1
        elif (evening1 <= tempDate < evening2):
            OPtime[2] += 1
        elif (night1 <= tempDate < night2):
            OPtime[3] += 1
        elif (midnight1 <= tempDate < midnight2):
            OPtime[4] += 1
        else:
            print(tempDate)

    SMtime = [0, 0, 0, 0, 0]  # morning, afternooon, evening, night, midnight
    for x in range(0, len(samsungCampaign[0])):
        tempDate = datetime.strptime(oneplusCampaign[4][x], '%Y-%m-%d %H:%M:%S').time()
        if (morning1 <= tempDate < morning2):
            SMtime[0] += 1
        elif (afternoon1 <= tempDate < afternoon2):
            SMtime[1] += 1
        elif (evening1 <= tempDate < evening2):
            SMtime[2] += 1
        elif (night1 <= tempDate < night2):
            SMtime[3] += 1
        elif (midnight1 <= tempDate < midnight2):
            SMtime[4] += 1
        else:
            print(tempDate)

    print(OPtime)
    print(SMtime)

    datadict1 = {
        'values': OPtime,
        'labels': ["Morning(6:00am - 11:59am)", "Afternoon(12:00pm - 4:59pm)", "Evening(5:00pm - 7:59pm)",
                   "Night(8:00pm - 11:59pm)", "Midnight(12:00am - 5:59am)"],
        'domain': {'x': [0, .48]},
        'name': 'OnePlus',
        'hoverinfo': 'label+percent+name+value',
        'textinfo': 'none',
        'hole': .4,
        'type': 'pie'
    }

    datadict2 = {
        'values': SMtime,
        'labels': ["Morning(6:00am - 11:59am)", "Afternoon(12:00pm - 4:59pm)", "Evening(5:00pm - 7:59pm)",
                   "Night(8:00pm - 11:59pm)", "Midnight(12:00am - 5:59am)"],
        'domain': {'x': [.52, 1]},
        'name': 'SamsungMobile',
        'hoverinfo': 'label+percent+name+value',
        'textinfo': 'none',
        'hole': .4,
        'type': 'pie'
    }

    fig = {
        'data': [datadict1, datadict2],
        'sort': False,
        'layout': {
            'title': 'Time of Campaign Tweets Created by OnePlus and SamsungMobile',
            'font': dict(size=15),
            "annotations": [
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": "OnePlus",
                    "x": 0.17,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": "Samsung<br>Mobile",
                    "x": 0.84,
                    "y": 0.5
                }
            ],
            "legend": {'font': {'size': 12}}
        }
    }

    graphJSON7 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON7

def overallEngagementRate(ERcampaign1, ERnoncampaign1, ERcampaign2, ERnoncampaign2):  #bar chart
    trace1 = {}
    trace1['y'] = ['OnePlus', 'Samsung<br>Mobile']
    trace1['x'] = [ERcampaign1, ERcampaign2]
    trace1['orientation'] = 'h'
    trace1['name'] = 'Campaign'
    trace1['type'] = 'bar'

    trace2 = {}
    trace2['y'] = ['OnePlus', 'Samsung<br>Mobile']
    trace2['x'] = [ERnoncampaign1, ERnoncampaign2]
    trace2['orientation'] = 'h'
    trace2['name'] = 'Non-Campaign'
    trace2['type'] = 'bar'

    fig = {
        'data': [trace2, trace1],
        'layout': {'barmode': 'stack',
                   'xaxis': {'title': 'Engagement Rate (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'yaxis': {'title': 'Company', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'title': 'Engagement Rate over 6 months of OnePlus and SamsungMobile',
                   'font': dict(size=15)}
    }

    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON1


def tweetCount(tweetCampaign1, tweetNonCampaign1, tweetCampaign2, tweetNonCampaign2):  #pie chart

    datadict1 = {
        'values': [tweetCampaign1, tweetNonCampaign1],
        'labels': ['Campaign', 'Non-Campaign'],
        'domain': {'x': [0, .48]},
        'name': 'OnePlus',
        'hoverinfo': 'label+percent+name+value',
        'hole': .4,
        'type': 'pie',
        'marker': {'colors': ['#ff7f0e', '#1f77b4']},
        'sort': 'false'
    }

    datadict2 = {
        'values': [tweetCampaign2, tweetNonCampaign2],
        'labels': ['Campaign', 'Non-Campaign'],
        'domain': {'x': [.52, 1]},
        'name': 'SamsungMobile',
        'hoverinfo': 'label+percent+name+value',
        'hole': .4,
        'type': 'pie',
        'marker': {'colors': ['#ff7f0e', '#1f77b4']},
        'sort': 'false'
    }


    fig = {
        'data': [datadict1, datadict2],
        'sort': False,
        'layout': {
            'title': 'Proportion of Tweets by OnePlus and SamsungMobile',
            'font': dict(size=15),
            "annotations": [
                {
                    "font": {
                        "size": 13
                    },
                    "showarrow": False,
                    "text": "OnePlus",
                    "x": 0.18,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 13
                    },
                    "showarrow": False,
                    "text": "Samsung<br>Mobile",
                    "x": 0.835,
                    "y": 0.5
                }
            ]
        }
    }

    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON2


def applauseRate(likesCampaign1, likesCampaign2, campaign1Follower, campaign2Follower):  #bar chart
    num_of_tweet1 = len(likesCampaign1)
    num_of_tweet2 = len(likesCampaign2)
    applauseRate1 = ((sum(likesCampaign1)/num_of_tweet1)/campaign1Follower) * 100
    applauseRate2 = ((sum(likesCampaign2)/num_of_tweet2)/campaign2Follower) * 100

    trace1 = {}
    trace1['x'] = ['OnePlus', 'SamsungMobile']
    trace1['y'] = [applauseRate1, applauseRate2]
    trace1['type'] = 'bar'
    trace1['marker'] = {'color': '#ff7f0e'}

    fig = {
        'data': [trace1],
        'layout': {'title': 'Applause Rate over 6 months<br>of OnePlus and SamsungMobile',
                   'xaxis': {'title': 'Company', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'yaxis': {'title': 'Applause Rate (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'font': dict(size=15)}
    }

    graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON3


def conversationRate(replyCampaign1, replyCampaign2, campaign1Follower, campaign2Follower):  #bar chart
    num_of_tweet1 = len(replyCampaign1)
    num_of_tweet2 = len(replyCampaign2)
    converRate1 = ((sum(replyCampaign1)/num_of_tweet1)/campaign1Follower) * 100
    converRate2 = ((sum(replyCampaign2)/num_of_tweet2)/campaign2Follower) * 100

    trace1 = {}
    trace1['x'] = ['OnePlus', 'SamsungMobile']
    trace1['y'] = [converRate1, converRate2]
    trace1['type'] = 'bar'
    trace1['marker'] = {'color': '#ff7f0e'}

    fig = {
        'data': [trace1],
        'layout': {'title': 'Conversation Rate over 6 months<br>of OnePlus and SamsungMobile',
                   'xaxis': {'title': 'Company', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'yaxis': {'title': 'Coversation Rate (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'font': dict(size=15)}
    }

    graphJSON4 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON4


def amplificationRate(retCampaign1, retCampaign2, campaign1Follower, campaign2Follower):  #bar chart
    num_of_tweet1 = len(retCampaign1)
    num_of_tweet2 = len(retCampaign2)
    ampRate1 = ((sum(retCampaign1)/num_of_tweet1)/campaign1Follower) * 100
    ampRate2 = ((sum(retCampaign2)/num_of_tweet2)/campaign2Follower) * 100

    trace1 = {}
    trace1['x'] = ['OnePlus', 'SamsungMobile']
    trace1['y'] = [ampRate1, ampRate2]
    trace1['type'] = 'bar'
    trace1['marker'] = {'color': '#ff7f0e'}

    fig = {
        'data': [trace1],
        'layout': {'title': 'Amplification Rate over 6 months<br>of OnePlus and SamsungMobile',
                   'xaxis': {'title': 'Company', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'yaxis': {'title': 'Amplification Rate (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                   'font': dict(size=15),
                   }
    }

    graphJSON5 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON5


def engagementEachMonth(oneplusCampaign, oneplusNonCampaign, samsungCampaign, samsungNonCampaign,  #scatter / line chart
                                     oneplusFollower, samsungFollower):

    months = ['July', 'August', 'September', 'October', 'November', 'December']
    oneplusCampaign[4].sort()
    oneplusNonCampaign[4].sort()
    samsungCampaign[4].sort()
    samsungNonCampaign[4].sort()

    #Get OnePlus campaign Engagement Rate
    engagementOPC = []
    tempData = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for x in range(0, len(oneplusCampaign[0])):
        tempDate = datetime.strptime(oneplusCampaign[4][x], '%Y-%m-%d %H:%M:%S')
        tempIndex = months.index(tempDate.strftime("%B"))
        tempData[0][tempIndex] += oneplusCampaign[1][x] + oneplusCampaign[2][x] + oneplusCampaign[3][x]
        tempData[1][tempIndex] += 1

    for x in range(0, len(months)):
        if tempData[1][x] == 0:
            engagementOPC.append(0)
        else:
            rate = ((tempData[0][x]/tempData[1][x])/oneplusFollower) * 100
            engagementOPC.append(rate)

    # Get OnePlus non-campaign Engagement Rate
    engagementOPNC = []
    tempData = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for x in range(0, len(oneplusNonCampaign[0])):
        tempDate = datetime.strptime(oneplusNonCampaign[4][x], '%Y-%m-%d %H:%M:%S')
        tempIndex = months.index(tempDate.strftime("%B"))
        tempData[0][tempIndex] += oneplusNonCampaign[1][x] + oneplusNonCampaign[2][x] + oneplusNonCampaign[3][x]
        tempData[1][tempIndex] += 1

    for x in range(0, len(months)):
        if tempData[1][x] == 0:
            engagementOPNC.append(0)
        else:
            rate = ((tempData[0][x] / tempData[1][x]) / oneplusFollower) * 100
            engagementOPNC.append(rate)

    # Get Samsung campaign Engagement Rate
    engagementSMC = []
    tempData = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for x in range(0, len(samsungCampaign[0])):
        tempDate = datetime.strptime(samsungCampaign[4][x], '%Y-%m-%d %H:%M:%S')
        tempIndex = months.index(tempDate.strftime("%B"))
        tempData[0][tempIndex] += samsungCampaign[1][x] + samsungCampaign[2][x] + samsungCampaign[3][x]
        tempData[1][tempIndex] += 1

    for x in range(0, len(months)):
        if tempData[1][x] == 0:
            engagementSMC.append(0)
        else:
            rate = ((tempData[0][x] / tempData[1][x]) / samsungFollower) * 100
            engagementSMC.append(rate)

    # Get Samsung non-campaign Engagement Rate
    engagementSMNC = []
    tempData = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for x in range(0, len(samsungNonCampaign[0])):
        tempDate = datetime.strptime(samsungNonCampaign[4][x], '%Y-%m-%d %H:%M:%S')
        tempIndex = months.index(tempDate.strftime("%B"))
        tempData[0][tempIndex] += samsungNonCampaign[1][x] + samsungNonCampaign[2][x] + samsungNonCampaign[3][x]
        tempData[1][tempIndex] += 1

    for x in range(0, len(months)):
        if tempData[1][x] == 0:
            engagementSMNC.append(0)
        else:
            rate = ((tempData[0][x] / tempData[1][x]) / samsungFollower) * 100
            engagementSMNC.append(rate)

    trace1 = {
        'x': months,
        'y': engagementOPC,
        'name': 'OnePlus, Campaign',
        'line': {
            'color': 'rgb(205, 12, 24)',
            'width': 3
        },
        'type': 'scatter'
    }

    trace2 = {
        'x': months,
        'y': engagementOPNC,
        'name': 'OnePlus, Non-Campaign',
        'line': {
            'color': 'rgb(205, 12, 24)',
            'width': 3,
            'dash': 'dot',
        },
        'type': 'scatter'
    }

    trace3 = {
        'x': months,
        'y': engagementSMC,
        'name': 'SamsungMobile, Campaign',
        'line': {
            'color': 'rgb(0, 153, 0)',
            'width': 3
        },
        'type': 'scatter'
    }

    trace4 = {
        'x': months,
        'y': engagementSMNC,
        'name': 'SamsungMobile, Non-Campaign',
        'line': {
            'color': 'rgb(0, 153, 0)',
            'dash': 'dot',
            'width': 3
        },
        'type': 'scatter'
    }

    fig = {
        'data': [trace1, trace2, trace3, trace4],
        'layout': {
            'title': 'Engagement Rate Throughout 6 months',
            'xaxis': {'title': 'Month', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
            'yaxis': {'title': 'Engagement Rate (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
            'font': dict(size=15)
        }
    }

    graphJSON6 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON6


def filterCampaign(companyData, keyword):
    campaignData = [[], [], [], [], []]
    noncampaignData = [[], [], [], [], []]
    for x in range(0, len(companyData[0])):
        if (keyword in companyData[0][x].lower()):
            campaignData[0].append(companyData[0][x])
            campaignData[1].append(companyData[1][x])
            campaignData[2].append(companyData[2][x])
            campaignData[3].append(companyData[3][x])
            campaignData[4].append(companyData[4][x])
        else:
            noncampaignData[0].append(companyData[0][x])
            noncampaignData[1].append(companyData[1][x])
            noncampaignData[2].append(companyData[2][x])
            noncampaignData[3].append(companyData[3][x])
            noncampaignData[4].append(companyData[4][x])

    return campaignData, noncampaignData


def engagementRate(companyData, num_of_followers):
    numtweet = len(companyData[0])
    engagement = (((sum(companyData[1])+sum(companyData[2])+sum(companyData[3]))/numtweet)/num_of_followers) * 100
    engagementRate = round(engagement, 2)
    return engagementRate


@app.route('/dashboard')
def dashboard():
    file1 = "oneplus-with-reply.json"
    texts1 = []
    favorites1 = []
    replies1 = []
    retweets1 = []
    datetime1 = []
    oneplusData = []
    with open(file1) as f1:
        for line1 in f1:
            data1 = json.loads(line1)
            texts1.append(data1['text'])
            favorites1.append(data1['nbr_favorite'])
            replies1.append(data1['nbr_reply'])
            retweets1.append(data1['nbr_retweet'])
            datetime1.append(data1['datetime'])
    oneplusData.append(texts1)
    oneplusData.append(favorites1)
    oneplusData.append(replies1)
    oneplusData.append(retweets1)
    oneplusData.append(datetime1)

    file2 = "samsung-with-reply.json"
    texts2 = []
    favorites2 = []
    replies2 = []
    retweets2 = []
    datetime2 = []
    samsungData = []
    with open(file2) as f2:
        for line2 in f2:
            data2 = json.loads(line2)
            texts2.append(data2['text'])                ##0
            favorites2.append(data2['nbr_favorite'])    ##1
            replies2.append(data2['nbr_reply'])         ##2
            retweets2.append(data2['nbr_retweet'])      ##3
            datetime2.append(data2['datetime'])         ##4
    samsungData.append(texts2)
    samsungData.append(favorites2)
    samsungData.append(replies2)
    samsungData.append(retweets2)
    samsungData.append(datetime2)

    oneplusCampaign, oneplusNonCampaign = filterCampaign(oneplusData, '#oneplus6t')
    samsungCampaign, samsungNonCampaign = filterCampaign(samsungData, '#galaxynote9')

    profile1 = "user_profile_oneplus.json"
    profile2 = "user_profile_SamsungMobile.json"

    with open(profile1) as p1:
        oneplusProfile = json.loads(p1.read())
        oneplusFollower = oneplusProfile["followers_count"]

    with open(profile2) as p2:
        samsungProfile = json.loads(p2.read())
        samsungFollower = samsungProfile["followers_count"]

    ERcampaignOP = engagementRate(oneplusCampaign, oneplusFollower)
    ERnoncampaignOP = engagementRate(oneplusNonCampaign, oneplusFollower)
    ERcampaignSM = engagementRate(samsungCampaign, samsungFollower)
    ERnoncampaignSM = engagementRate(samsungNonCampaign, samsungFollower)

    print("oneplus campaign engagementRate:", str(ERcampaignOP), "%")
    print("samsung campaign engagementRate:", str(ERcampaignSM), "%")
    print("oneplus non-campaign engagementRate:", str(ERnoncampaignOP), "%")
    print("samsung non-campaign engagementRate:", str(ERnoncampaignSM), "%")

    graphJSON1 = overallEngagementRate(ERcampaignOP, ERnoncampaignOP, ERcampaignSM, ERnoncampaignSM)
    graphJSON2 = tweetCount(len(oneplusCampaign[0]), len(oneplusNonCampaign[0]), len(samsungCampaign[0]),
                            len(samsungNonCampaign[0]))
    graphJSON3 = applauseRate(oneplusCampaign[1], samsungCampaign[1], oneplusFollower, samsungFollower)
    graphJSON4 = conversationRate(oneplusCampaign[2], samsungCampaign[2], oneplusFollower, samsungFollower)
    graphJSON5 = amplificationRate(oneplusCampaign[3], samsungCampaign[3], oneplusFollower, samsungFollower)
    graphJSON6 = engagementEachMonth(oneplusCampaign, oneplusNonCampaign, samsungCampaign, samsungNonCampaign,
                                     oneplusFollower, samsungFollower)
    graphJSON7 = peakTimeChart(oneplusCampaign, samsungCampaign)
	
	#Kevin Part
	
    months = ['July', 'August', 'September', 'October', 'November', 'December']
    oppos = []
    opneut = []
    opneg = []
    sspos = []
    ssneut = []
    ssneg = []
    with open('SA_monthly_OP.csv') as op_sa_monthly:
        op_sa_monthly_read = csv.reader(op_sa_monthly, delimiter=',')
        for row in op_sa_monthly_read:
            if row[1] == 'July':
                oppos.append(round(float(row[2]), 8))
                opneut.append(round(float(row[3]), 8))
                opneg.append(round(float(row[4]), 8))
            if row[1] == 'August':
                oppos.append(round(float(row[2]), 8))
                opneut.append(round(float(row[3]), 8))
                opneg.append(round(float(row[4]), 8))
            if row[1] == 'September':
                oppos.append(round(float(row[2]), 8))
                opneut.append(round(float(row[3]), 8))
                opneg.append(round(float(row[4]), 8))
            if row[1] == 'October':
                oppos.append(round(float(row[2]), 8))
                opneut.append(round(float(row[3]), 8))
                opneg.append(round(float(row[4]), 8))
            if row[1] == 'November':
                oppos.append(round(float(row[2]), 8))
                opneut.append(round(float(row[3]), 8))
                opneg.append(round(float(row[4]), 8))
            if row[1] == 'December':
                oppos.append(round(float(row[2]), 8))
                opneut.append(round(float(row[3]), 8))
                opneg.append(round(float(row[4]), 8))

    with open('SA_monthly_SS.csv') as ss_sa_monthly:
        ss_sa_monthly_reader = csv.reader(ss_sa_monthly, delimiter=',')
        for row in ss_sa_monthly_reader:
            if row[1] == 'July':
                sspos.append(round(float(row[2]), 8))
                ssneut.append(round(float(row[3]), 8))
                ssneg.append(round(float(row[4]), 8))
            if row[1] == 'August':
                sspos.append(round(float(row[2]), 8))
                ssneut.append(round(float(row[3]), 8))
                ssneg.append(round(float(row[4]), 8))
            if row[1] == 'September':
                sspos.append(round(float(row[2]), 8))
                ssneut.append(round(float(row[3]), 8))
                ssneg.append(round(float(row[4]), 8))
            if row[1] == 'October':
                sspos.append(round(float(row[2]), 8))
                ssneut.append(round(float(row[3]), 8))
                ssneg.append(round(float(row[4]), 8))
            if row[1] == 'November':
                sspos.append(round(float(row[2]), 8))
                ssneut.append(round(float(row[3]), 8))
                ssneg.append(round(float(row[4]), 8))
            if row[1] == 'December':
                sspos.append(round(float(row[2]), 8))
                ssneut.append(round(float(row[3]), 8))
                ssneg.append(round(float(row[4]), 8))

    trace1 = {
        'x': months,
        'y': oppos,
        'name': 'OnePlus, Positive',
        'line': {
            'color': '#2ca02c',
            'width': 3
        },
        'type': 'scatter'
    }
    trace2 = {
        'x': months,
        'y': opneut,
        'name': 'OnePlus, Neutral',
        'line': {
            'color': '#00BFFF',
            'width': 3
        },
        'type': 'scatter'
    }
    trace3 = {
        'x': months,
        'y': opneg,
        'name': 'OnePlus, Negative',
        'line': {
            'color': '#d62728',
            'width': 3
        },
        'type': 'scatter'
    }
    trace4 = {
        'x': months,
        'y': sspos,
        'name': 'Samsung Mobile, Positive',
        'line': {
            'color': '#2ca02c',
            'width': 3,
            'dash': 'dot',
        },
        'type': 'scatter'
    }
    trace5 = {
        'x': months,
        'y': ssneut,
        'name': 'Samsung Mobile, Neutral',
        'line': {
            'color': '#00BFFF',
            'width': 3,
            'dash': 'dot',
        },
        'type': 'scatter'
    }
    trace6 = {
        'x': months,
        'y': ssneg,
        'name': 'Samsung Mobile, Negative',
        'line': {
            'color': '#d62728',
            'width': 3,
            'dash': 'dot',
        },
        'type': 'scatter'
    }

    fig6 = {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout': {
            'title': 'Sentiment Analysis Throughout 6 months',
            'xaxis': {'title': 'Month', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
            'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
            'font': dict(size=15),
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)'
            }
    }

    # Topic Aspect
    with open('op_topic_aspect.csv') as op_topic:
        op_topic_read = csv.reader(op_topic, delimiter=',')
        for row in op_topic_read:
            if row[1] == 'fingerprint':
                oppos1 = round(float(row[2]), 13)
                opneut1 = round(float(row[3]), 13)
                opneg1 = round(float(row[4]), 13)
            elif row[1] == 'price':
                oppos2 = round(float(row[2]), 13)
                opneut2 = round(float(row[3]), 13)
                opneg2 = round(float(row[4]), 13)
            elif row[1] == 'jack':
                oppos3 = round(float(row[2]), 13)
                opneut3 = round(float(row[3]), 13)
                opneg3 = round(float(row[4]), 13)

        trace7 = {}
        trace7['x'] = ['Positive', 'Neutral', 'Negative']
        trace7['y'] = [oppos1, opneut1, opneg1]
        trace7['type'] = 'bar'
        trace7['marker'] = {'color': ['#2ca02c', '#00BFFF', '#d62728']}

        fig7= {
            'data': [trace7],
            'layout': {'title': 'FingerPrint',
                       'xaxis': {'title': 'Sentiment', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

        trace8 = {}
        trace8['x'] = ['Positive', 'Neutral', 'Negative']
        trace8['y'] = [oppos2, opneut2, opneg2]
        trace8['type'] = 'bar'
        trace8['marker'] = {'color': ['#2ca02c', '#00BFFF', '#d62728']}

        fig8 = {
            'data': [trace8],
            'layout': {'title': 'Price',
                       'xaxis': {'title': 'Sentiment', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

        trace9 = {}
        trace9['x'] = ['Positive', 'Neutral', 'Negative']
        trace9['y'] = [oppos3, opneut3, opneg3]
        trace9['type'] = 'bar'
        trace9['marker'] = {'color': ['#2ca02c', '#00BFFF', '#d62728']}

        fig9 = {
            'data': [trace9],
            'layout': {'title': 'Audio Jack',
                       'xaxis': {'title': 'Sentiment', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

    with open('ss_topic_aspect.csv') as op_topic:
        op_topic_read = csv.reader(op_topic, delimiter=',')
        for row in op_topic_read:
            if row[1] == 'battery':
                sspos1 = round(float(row[2]), 13)
                ssneut1 = round(float(row[3]), 13)
                ssneg1 = round(float(row[4]), 13)
            elif row[1] == 'camera':
                sspos2 = round(float(row[2]), 13)
                ssneut2 = round(float(row[3]), 13)
                ssneg2 = round(float(row[4]), 13)
            elif row[1] == 'pen':
                sspos3 = round(float(row[2]), 13)
                ssneut3 = round(float(row[3]), 13)
                ssneg3 = round(float(row[4]), 13)

        trace10 = {}
        trace10['x'] = ['Positive', 'Neutral', 'Negative']
        trace10['y'] = [sspos1, ssneut1, ssneg1]
        trace10['type'] = 'bar'
        trace10['marker'] = {'color': ['#2ca02c', '#00BFFF', '#d62728']}

        fig10= {
            'data': [trace10],
            'layout': {'title': 'Battery',
                       'xaxis': {'title': 'Sentiment', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

        trace11 = {}
        trace11['x'] = ['Positive', 'Neutral', 'Negative']
        trace11['y'] = [sspos2, ssneut2, ssneg2]
        trace11['type'] = 'bar'
        trace11['marker'] = {'color': ['#2ca02c', '#00BFFF', '#d62728']}

        fig11 = {
            'data': [trace11],
            'layout': {'title': 'Camera',
                       'xaxis': {'title': 'Sentiment', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

        trace12 = {}
        trace12['x'] = ['Positive', 'Neutral', 'Negative']
        trace12['y'] = [sspos3, ssneut3, ssneg3]
        trace12['type'] = 'bar'
        trace12['marker'] = {'color': ['#2ca02c', '#00BFFF', '#d62728']}

        fig12 = {
            'data': [trace12],
            'layout': {'title': 'S-Pen',
                       'xaxis': {'title': 'Sentiment', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

    # Overall SA
    with open('SA.csv') as SA:
        SA_read = csv.reader(SA, delimiter=',')
        for row in SA_read:
            if row[0] == 'oneplus':
                opapos = round(float(row[1]), 13)
                opaneut = round(float(row[2]), 13)
                opaneg = round(float(row[3]), 13)
            elif row[0] == 'samsung':
                ssapos = round(float(row[1]), 13)
                ssaneut = round(float(row[2]), 13)
                ssaneg = round(float(row[3]), 13)

        trace13 = {}
        trace13['y'] = ['OnePlus', 'Samsung<br>Mobile']
        trace13['x'] = [opapos, ssapos]
        trace13['orientation'] = 'h'
        trace13['name'] = 'Positive'
        trace13['type'] = 'bar'
        trace13['marker'] = {'color': '#2ca02c'}

        trace14 = {}
        trace14['y'] = ['OnePlus', 'Samsung<br>Mobile']
        trace14['x'] = [opaneut, ssaneut]
        trace14['orientation'] = 'h'
        trace14['name'] = 'Neutral'
        trace14['type'] = 'bar'
        trace14['marker'] = {'color': '#00BFFF'}

        trace15 = {}
        trace15['y'] = ['OnePlus', 'Samsung<br>Mobile']
        trace15['x'] = [opaneg, ssaneg]
        trace15['orientation'] = 'h'
        trace15['name'] = 'Negative'
        trace15['type'] = 'bar'
        trace15['marker'] = {'color': '#d62728'}

        fig13 = {
            'data': [trace13, trace14, trace15],
            'layout': {'xaxis': {'title': 'Tweet Ratio (%)', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'yaxis': {'title': 'Company', 'titlefont': {'size': 15, 'color': '#7f7f7f'}},
                       'title': 'Sentiment Analysis over 6 months of OnePlus and SamsungMobile',
                       'font': dict(size=15),
                       'paper_bgcolor': 'rgba(0,0,0,0)',
                       'plot_bgcolor': 'rgba(0,0,0,0)'
                        }
        }

    # pass diagram to web application
    graph13 = json.dumps(fig13, cls=plotly.utils.PlotlyJSONEncoder)  # SA over 6 months
    graph6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)  # SA for 6 months
    graph7 = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)  # SA for Topic
    graph8 = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)  # SA for Topic
    graph9 = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)  # SA for Topic
    graph10 = json.dumps(fig10, cls=plotly.utils.PlotlyJSONEncoder)  # SA for Topic
    graph11 = json.dumps(fig11, cls=plotly.utils.PlotlyJSONEncoder)  # SA for Topic
    graph12 = json.dumps(fig12, cls=plotly.utils.PlotlyJSONEncoder)  # SA for Topic
	

    return render_template('dashboard.html', oneplusCampaign=oneplusCampaign, graphJSON1=graphJSON1, graphJSON2=graphJSON2,
                           graphJSON3=graphJSON3, graphJSON4=graphJSON4, graphJSON5=graphJSON5, graphJSON6=graphJSON6,
                           graphJSON7=graphJSON7, graph6=graph6, graph7=graph7, graph8=graph8, graph9=graph9, 
						   graph10=graph10, graph11=graph11, graph12=graph12, graph13=graph13)

if __name__=="__main__":
    app.run(debug=True)
