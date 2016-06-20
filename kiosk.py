#!/usr/bin/python
# encoding=utf-8

import lametric

import urllib, urllib2
import xml.etree.ElementTree as ET
import os.path
import ConfigParser

# Netatmo / LaMetric Proxy
# Author : Stanislav Likavcan, likavcan@gmail.com

# A simple client which turns LaMetric into Netamo display. This client calls Netatmo API and updates LaMetric display 
# Easiest way to keep the LaMetric display updated is via cron task:
# */10 * * * * /home/lametric/updateLaMetric.py
# Don't forget to create an app within both Netatmo and LaMetric and provide your credentials here:

scriptDir = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read("%s/config.ini"%(scriptDir))

# Netatmo authentication
app_id     = config.get('lametric','app_id')
access_token = config.get('lametric','access_token')

req = urllib2.Request("http://gir.local:32400/status/sessions")
response = urllib2.urlopen(req).read()
root = ET.fromstring(response)

is_playing = root.attrib['size'] != '0'

if is_playing:
	for video in root.findall("Video"):
		title = video.attrib["title"]
		year = video.attrib["year"]
		duration = float(video.attrib["duration"])
		current = float(video.attrib["viewOffset"])
		remaining_minutes = (duration-current)/60000

		print "Now Playing: %s (%s)"%(title,year)
		print "Currently at %.1f mins of %.1f"%(current/60000, duration/60000)

		# Post data to LaMetric
		lametric = lametric.Setup("https://10.0.1.100:4343")
		lametric.addTextFrame('a1944',"On Now")
		lametric.addTextFrame('',"%s (%s)"%(title,year))
		lametric.addGoalFrame('',0,current/60000, duration/60000," Mins")
		remaining_msg = "%i minute%s left"%(remaining_minutes, "s" if remaining_minutes > 1 else "")
		if remaining_minutes == 0:
			remaining_msg = "The End"
		lametric.addTextFrame('',remaining_msg)
		lametric.push(app_id, access_token)
		
		break