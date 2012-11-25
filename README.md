PySeries
========
This is an application to keep track of your tv series.

What do you need
----------------
In order for PySeries to run the only must-have is BeautifulSoup4
which you can install using
    pip install beautifulsoup4
or
    easy\_install beautifulsoup4
For more information you can visit http://www.crummy.com/software/BeautifulSoup/

I've developed PySeries with python version 2.7.3. I have not tested it
on other versions but this, but I think it can work with 2.6.X. Anyway
if some of you check it and want to tell me your feedback will be welcomed.

series.txt (input file)
-----------------------
In this file you have to put the series you want to track. By now the
process is quite manual. In the file each line is a register of this form:
    number#site#name#URL
where:
    number: is a kind of serie identifier
    site: is where new chapter of the serie are announced
    name: the main name of the serie (it's a free field)
    URL: the URL where you can find the serie
The character '#' works as a field separator. So it's recommended not to
use it in the name filed as it can direct to a malfunction of the program.
As an example:
    22#yourseries#Castle - S5#http://www.yourseries.com/show.php?t=234145

cookies.data (input file)
-------------------------
Almost every website will ask you for registration. The most usual way to
know if you are registered is using cookies. In this file you will store
the cookies for every website you look for up to date series.
As in series.txt the process is quite manual by now. You have to get the
cookie from the browser (Firefox and Chrome have some good ways to get
cookies from sites) and put them in the file in the form:
    site#cookie
where:
    site: is the same as in series.txt
    cookie: is the site's cookie
As in series.txt the '#' character works as a field separator. Here is
an example:
    yourseries#the\_cookie\_got\_from\_my\_browser

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
