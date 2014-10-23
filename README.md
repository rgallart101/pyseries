PySeries
========
This is an application to keep track of your tv shows. Once you feed the file series.txt it will tell you when your favourite tve shows have been updated.

Version
-------
Current version is 0.2.

Dependencies
------------
This new version has been updated to use Python 3. Specifically it has been tested with version 3.4.1.

Adding to the fact that it has been ported to Python 3 it is necessary to install the libraries cited in the tools/requirements3.txt file.

In order to do that it is advised to create a virtual environment so everything can be installed in a safe way.

To do that I recommend:

- For Mac OSX: the excellent article by Marina Mele (@marina_mele): [Install Python 3 on Mac OS X and use virtualenv and virtualenvwrapper](http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html).
- For Windows: [Install Python, Pip and Virtualenv on Windows](https://zignar.net/2012/06/17/install-python-on-windows/) updated on June 2014 to include Python 3.4
- For Linux: There are concise instructions at [Python2 and Python3 co-existing in harmony using Virtualenv](http://www.circuidipity.com/python2-and-python3.html) It is for Debian-based distros, but the main process should be easily extrapolated to any other distro.

Installing the dependencies
---------------------------
Assuming you have created the virtual environment, activate it and:

```
cd <the directory where you downloaded the app>
pip install -r tools/requirements3.txt

```

About the files
---------------
All the input and output files are created in the data folder. The program expects to find them all there.

series.txt (input file)
-----------------------
In this file you have to put the series you want to track. By now the
process is quite manual.

In the file each line is a register like this:

    number#site#name#URL

where:

    number: is a kind of serie identifier
    site: is where new chapter of the serie are announced (currently only 'divxatope' and 'todohdtv' are allowed)
    name: the main name of the serie (it's a free field)
    URL: the URL where you can find the serie

The character '#' works as a field separator. So it's recommended not to
use it in the name filed as it can direct to a malfunction of the program.
As an example:

    22#yourseries#Castle - S5#http://www.yourseries.com/show.php?t=234145

acts.txt (output file)
----------------------
This file is where the program will save the last state of the series.
On the next run, the program will match the contents found against those
of this file. If they differ, that will mean there will be an update of the
serie. Otherwise the serie won't be updated.

output.html (output file)
-------------------------
When the program ends this file will contain the links in order to get
the updated series.

Running the app
---------------
First activate your virtual environment if you have created any.

```
cd <the directory where you downloaded the app>/src
python pyseries
```

Future plans
------------
These are some functionalities I would like to create:

- Create an interface to handle the series.txt file. Be it a console interface or any other kind.
- Handle authentication for the different websites announcing links to the las tv shows episodes. 
- Make the program intelligent enough to get the links for the new episodes.
- Some kind of interface with JDownloader if possible
- ...