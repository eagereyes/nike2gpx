#!/usr/bin/python

#
# Nike2GPX by Robert Kosara. This program is in the public domain.
#
# This is a very simple script to convert JSON data from the Nike Running Site into GPX,
# which can be imported into other programs and sites (like RunKeeper)
# 
# Download the JSON using this URL schema (replace the run-id with your run ID)
# http:#nikerunning.nike.com/nikeplus/v2/services/app/get_gps_detail.jsp?_plus=true&id=<run-id>&format=json
# 
# Save it to a file that ends in .json, and run this script: ./nike2gpx <filename>.json
# This will create a file <filename>.gpx in GPX format
#

from xml.etree.ElementTree import TreeBuilder, ElementTree
from datetime import datetime
import json
import sys

data = json.load(open(sys.argv[1], "r"))

route = data["plusService"]["route"]

builder = TreeBuilder()

gpxAttrs = {
			"version":				"1.1",
			"creator":				"Nike2GPX",
			"xmlns:xsi":			"http://www.w3.org/2001/XMLSchema-instance",
			"xmlns":				"http://www.topografix.com/GPX/1/1",
			"xsi:schemaLocation":	"http://www.topografix.com/GPX/1/1 http://www.topografix.com/gpx/1/1/gpx.xsd"
}
builder.start("gpx", gpxAttrs)

builder.start("metadata", {})

builder.start("name", {})
builder.data("Run " + sys.argv[1][:-5])
builder.end("name")

minLon = 10000
maxLon = -10000
minLat = 10000
maxLat = -10000
for waypoint in route["waypointList"]:
	if waypoint["lon"] > maxLon:
		maxLon = waypoint["lon"]
	if waypoint["lon"] < minLon:
		minLon = waypoint["lon"]

	if waypoint["lat"] > maxLat:
		maxLat = waypoint["lat"]
	if waypoint["lat"] < minLat:
		minLat = waypoint["lat"]

bounds = {"minlat":str(minLat), "maxlat":str(maxLat), "minlon":str(minLon), "maxlon":str(maxLon)}
builder.start("bounds", bounds)
builder.end("bounds")

builder.end("metadata")

builder.start("trk", {})

builder.start("name", {})
builder.data(sys.argv[1][:-5])
builder.end("name")

builder.start("type", {})
builder.data("Run")
builder.end("type")

builder.start("trkseg", {})

for waypoint in route["waypointList"]:

	coords = {"lat":str(waypoint["lat"]), "lon":str(waypoint["lon"])}
	builder.start("trkpt", coords)
	
	builder.start("ele", {})
	builder.data(str(waypoint["alt"]))
	builder.end("ele")
	
	builder.start("time", {})
	time = datetime.utcfromtimestamp(waypoint["time"]/1000)
	builder.data(time.strftime("%Y-%m-%dT%H:%M:%SZ"))
	builder.end("time")
	
	builder.end("trkpt")

builder.end("trkseg")

builder.end("trk")

builder.end("gpx")

root = builder.close()

tree = ElementTree(root)

tree.write(open(sys.argv[1][:-5]+".gpx", "wb"), "utf-8")
