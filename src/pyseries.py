# -*- encoding: utf8 -*-
import os

from settings import conf
from utils import print_message

from plugins import divxatope, todohdtv

__author__ = 'ramonmariagallart'


class PluginFactory():
    @staticmethod
    def get(plugin):
        if plugin == "divxatope":
            return divxatope.get_digest
        elif plugin == "todohdtv":
            return todohdtv.get_digest


class Serie():
    def __init__(self):
        self.id = -1
        self.plugin = ''
        self.name = ''
        self.url = ''
        self.current_digest = None
        self.updated = False


class Update():
    def __init__(self):
        self.id = -1
        self.digest = ''


class PySeries():
    def __init__(self):
        self.series = []
        self.updates = []
        self.update_file_exists = False
        self.errors = []

    def _load_series(self):
        """
        Reads the series.txt file and creates a list of tuples
        :return:
        """
        if os.path.exists(os.path.join(conf.BASE_DIR, 'data', 'series.txt')):
            with open(os.path.join(conf.BASE_DIR, 'data', 'series.txt'), 'r') as f:
                num_line = 0
                for line in f:
                    num_line += 1
                    if not line or line.strip().startswith("#"):
                        continue
                    try:
                        splitted_line = line.split("#")
                        serie = Serie()
                        serie.id = splitted_line[0].strip()
                        serie.plugin = splitted_line[1].strip()
                        serie.name = splitted_line[2].strip()
                        serie.url = splitted_line[3].strip()
                        self.series.append(serie)
                    except Exception as e:
                        msg = "Error on series.txt file on line {}. {}".format(num_line, e)
                        print_message(conf.ERROR, msg)
        else:
            raise Exception("File series.txt does not exist in data folder")

    def _load_updates(self):
        """
        Loads the tv shows updates.
        :return:
        """
        if os.path.exists(os.path.join(conf.BASE_DIR, 'data', 'acts.txt')):
            self.update_file_exists = True
            with open(os.path.join(conf.BASE_DIR, 'data', 'acts.txt'), 'r') as f:
                num_line = 0
                for line in f:
                    num_line += 1
                    if not line or line.strip().startswith("#"):
                        continue
                    try:
                        splitted_line = line.split("#")
                        update = Update()
                        update.id = splitted_line[0].strip()
                        update.digest = splitted_line[1].strip()
                        self.updates.append(update)
                    except Exception as e:
                        msg = "Error on acts.txt file on line {}. {}".format(num_line, e)
                        print_message(conf.ERROR, msg)

    def _get_digest_for_tv_shows(self):
        for serie in self.series:
            my_digest_function = PluginFactory.get(serie.plugin)
            try:
                current_digest = my_digest_function(serie.url)
            except Exception as e:
                msg = "Error getting digest for '{}'. {}".format(serie.name, e)
                print_message(conf.ERROR, msg)
                continue
            serie.current_digest = current_digest

    def _search_update(self, tv_show_id):
        for update in self.updates:
            if update.id == tv_show_id:
                return update.digest
        return None

    def _check_for_updates(self):
        for serie in self.series:
            update = self._search_update(serie.id)
            if not update or update != serie.current_digest:
                serie.updated = True
                print_message(conf.INFO, "[{}] UPDATED!".format(serie.name))

    def _process_tv_shows(self):
        self._get_digest_for_tv_shows()
        self._check_for_updates()

    def _write_updates(self):
        try:
            with open(os.path.join(conf.BASE_DIR, 'data', 'acts.txt'), 'w+') as f:
                for serie in self.series:
                    f.write("{}#{}\r\n".format(serie.id, serie.current_digest))
        except Exception as e:
            msg = "Could not create update file: {}".format(e)
            print_message(conf.ERROR, msg)

    def _write_html_output(self):
        """
        Escriu en el fitxer output.html els enllaços a les sèries que han
        estat actualitzades.
        """
        series_actualitzades = []
        for serie in self.series:
            if serie.updated:
                update = '<li><a href="{}" target="_blank">{}</a></li>'.format(serie.url, serie.name)
                series_actualitzades.append(update)

        try:
            with open(os.path.join(conf.BASE_DIR, 'data', 'output.html'), "w+") as f:
                f.write("<!DOCTYPE html>\r\n")
                f.write("""
<html>
<head>
    <meta charset="utf-8"/>
    <title>Llista de s&egrave;ries</title>
</head>
                """)
                f.write("<body>\r\n")
                if series_actualitzades:
                    f.write("""
    <h1>Llista de s&egrave;ries per actualitzar</h1>
    <ul>
                        """)
                    for serie in series_actualitzades:
                        f.write("\r\n\t\t" + serie)

                    f.write("\r\n\t</ul>")
                else:
                    f.write("""\r\n\t<h1>Totes les s&egrave;ries estan
                        actualitzades</h1>\r\n\t""")
                    f.write("\r\n</body>\r\n</html>\r\n")
                f.write("\r\n</body>\r\n</html>\r\n")
        except Exception as e:
            msg = "Could not create output file: {}".format(e)
            print_message(conf.ERROR, msg)

    def _write_output(self):
        self._write_updates()
        self._write_html_output()

    def parse_series(self):
        self._load_series()
        self._load_updates()
        self._process_tv_shows()
        self._write_output()


if __name__ == '__main__':
    pyseries = PySeries()
    try:
        pyseries.parse_series()
    except Exception as exception:
        print_message(conf.ERROR, exception)

    print_message(conf.INFO, "Program terminated.")
