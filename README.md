# About

The Nike+ GPS app is great when starting to run, but it's not something for the long term. One problem with switching to other programs or websites is that you will probably want to take your data with you. While there is no official way to do this, it is possible to coax the website into surrendering your data in a JSON format. This script converts that data into the [GPS Exchange Format (GPX)](http://www.topografix.com/gpx.asp), which most running websites and programs accept.

# Procedure for Converting the Data

You will have to do this manually for every run. Go to the runs tab on the Nike+ website and click on a run you want to export. In the URL bar, you will see something like this:

http://nikerunning.nike.com/nikeos/p/nikeplus/en_US/plus/#//runs/detail/__&lt;user-id&gt;__/__&lt;run-id&gt;__/all/allRuns/

Where the _user-id_ and _run-id_ are numerical. Use wget or curl to retrieve the following URL to a file (replacing the run-id part with your run-id):

http://nikerunning.nike.com/nikeplus/v2/services/app/get\_gps\_detail.jsp?\_plus=true&id=__&lt;run-id&gt;__&format=json

Name the file so that it ends in .json, because the script will produce a file with the same name and a .gpx extension (and it doesn't check whether the extension is correct or not). Run the script:

    ./nike2gpx filename.json

The resulting .gpx file can be imported to RunKeeper, etc.

# Caveats

This is a very simple (and ugly) script that produces a fairly basic GPX file. I make no claims to the general correctness of the output, but [RunKeeper](http://runkeeper.com/) accepts the files.

# License

Nike2GPX was written by Robert Kosara. I am placing it in the public domain.
