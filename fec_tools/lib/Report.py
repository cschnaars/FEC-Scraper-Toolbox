# from fec_tools.lib import paper_or_plastic
from FEC_Toolbox import settings
from fec_tools.lib.download_report import download_report
from fec_tools.lib.get_delim_report_url import get_delim_report_url


class Report:
    """
    Report base class.
    """
    def __init__(self, rpt_id, down_now=settings.DOWN_NOW):
        # down_now_urls=None
        # down_now_paths=None
        # mem_load=settings.MEM_LOAD
        # db_load_delim=settings.DB_LOAD_DELIM
        # db_load_url=None
        # destroy=False
        """
        Report base class initialization.

        :param rpt_id: Report ID. Required. This is the ID assigned by the FEC for a specific report. It is used as the
        primary key for reports in the django database.
        :type rpt_id: int

        :param down_now: Download now. Use this parameter to control whether the application automatically downloads
        the specified Report ID in one or more formats upon instantiation. Leave this parameter unspecified to use the
        default value (DOWN_NOW) specified in settings.py. If you do not want any files downloaded on instantiation,
        set this value (or settings.DOWN_NOW) to None. If any filetypes you specify here don't match a key in
        settings.FILE_TYPES, you must provide a url ('url') and save path ('path') in a dictionary for each filetype.
        Example: down_now = {'ascii28': {'url': 'http://docquery.fec.gov/dcdev/posted/1008299.fec',
        'path': 'C:\data\fec\reports\text\ascii28\1008299.txt'}}

        Each filetype is useful only to access settings in settings.FILE_TYPES. If you are not using these settings or
        want to override them, you can set the appropriate filetype(s) to any object you like (including None or '');
        your filetype setting will be ignored.
        :type down_now: dict

        # :param down_now_urls: Download now URLs. You can ignore this setting (set to None) unless a value in down_now
        # does not match a key in settings.DOWN_NOW or you want to override those settings. In those cases, set
        # down_now_urls to a list containing a valid URL for each filetype in down_now. For any filetype that is a key
        # in settings.FILE_TYPES, you can set the appropriate URL in down_now_urls to None, if you want to use the
        # default URL.
        # :type down_now_urls: list
        #
        # :param down_now_paths: Download now file paths. You can ignore this setting (set to None) unless a filetype in
        # down_now does not match a key in settings.DOWN_NOW or you want to override those settings. In those cases, set
        # down_now_paths to a list containing a valid save file path for each filetype in down_now. For any filetype
        # that is a key in settings.FILE_TYPES, you can set the appropriate path in down_now_paths to None, if you want
        # to use the default path. Note that unless overridden, the default save path for a given filetype is:
        # settings.FILE_TYPES[filetype]['save_path']<rpt_id>.settings.FILE_TYPES[filetype]['ext']
        # :type down_now_paths: list

        # :param mem_load: Store report data in memory. Use this parameter to control whether the django application
        # will download and retain a report's data in memory upon instantiation of the base Report class. Leave this
        # parameter unspecified to use default value (MEM_LOAD) specified in settings.py.
        # :type mem_load: tuple
        #
        # :param db_load_delim: Delimiter used in data file to be downloaded from the FEC and loaded into the database
        # upon instantiation. Set to None if the file should not be loaded upon instantiation. If this value matches a
        # key found in settings.FILE_TYPES, the class can determine db_load_url automatically.
        # :type db_load_delim: str
        #
        # :param db_load_url: The URL (or URL pattern) used to download -- and load into the database -- a delimited
        # text file in the format specified by db_load_delim. If db_load_delim matches a key found in
        # settings.FILE_TYPES, you can set db_load_url to None and the class will determine the URL automatically. This
        # setting is ignored if db_load_delim is set to None.
        # :type db_load_url: str
        #
        # :param destroy: Garbage collect this object after instantiation. This is useful if you only want to download a
        # report and/or load its data into the database but do not otherwise need to inspect the data. Default is False.
        # :type destroy: bool
        #
        # :return: Report
        """
        self.rpt_id = rpt_id

        # Download report in one or more formats
        if down_now is not None:
            self.download_reports(down_now)

    def download_reports(self, down_now):
        for filetype in down_now.keys():
            url = None

            # Fetch url if provided explicitly
            if 'url' in down_now[filetype].keys():
                url = down_now[filetype]['url']

            # Otherwise, call function to determine URL
            elif filetype in settings.FILE_TYPES.keys():
                url = get_delim_report_url(rpt_id=self.rpt_id, file_type=filetype)

            # Return error message if no valid URL
            if url is None:
                return 'Report ' + str(self.rpt_id) + ' was not downloaded because either an invalid URL was ' \
                    'provided or a valid URL could not be constructed from the default settings.'

            path = None

            # Fetch save path if provided explicitly
            if 'path' in down_now[filetype].keys():
                path = down_now[filetype]['path']

            # Otherwise, call function to determine URL
            elif filetype in settings.FILE_TYPES.keys():
                file_ext = settings.FILE_TYPES[filetype]['ext']
                path = settings.FILE_TYPES[filetype]['save_path'] + str(self.rpt_id) + '.' + file_ext

            # Return error message if invalid save path
            if path is None:
                return 'Report ' + str(self.rpt_id) + ' was not downloaded because either an invalid save path was ' \
                    'provided or a valid path could not be constructed from the default settings.'

            # If we reach this point, we have a url and a save path
            downloaded, msg = download_report(url, path)

            # Display message if there was a problem
            if downloaded is False:
                print(msg)

    def download(self, url=None, save_path=None):
        pass

    def fech(self):
        """
        It's "fetch", with a soft "ch" sound. There are no other acceptable pronunciations.
        """
        msg = "It's " + '"fetch", with a soft "ch" sound. There are no other acceptable pronunciations.'
        print(msg)

    def fetch(self, rpt_id, filetype, delim=None, url_pattern=None, keep_in_mem=False, save_to_disk=False,
              save_path=None, overwrite=False):
        """
        If save path and/or url set to None, retrieve values from FILE_TYPES dictionary. Alert user and exit if filetype
        does not exist in FILE_TYPES to lookup values that have not been provided. Before downloading, check to see if
        file already exists. Alert user and take no other action if overwrite is set to False. Otherwise, download the
        file.
        :param rpt_id:
        :param filetype:
        :param url_pattern:
        :param keep_in_mem:
        :param save_to_disk:
        :param save_path:
        :param overwrite:
        :return:
        """

        # Fetch default/missing values from FILE_TYPES
        # if filetype in settings.FILE_TYPES.keys():
        #     if delim is None:
        #         delim = settings.FILE_TYPES[filetype][delim]
        #     if url_pattern is None:
        #         url_pattern = settings.FILE_TYPES[filetype][url_pattern]
        #     if save_path is None:
        #         save_path = settings.FILE_TYPES[filetype][save_path]
        #
        # # Check to see whether report was filed electronically or on paper.
        # # This is necessary to form URL to fetch report for text-based reports.
        # # Skip this process if no delimiter
        # if delim is None:
        #     pass
        # elif 'text_url' not in self.__dict__:
        #     self.text_url = paper_or_plastic(rpt_id, url_pattern)
        # elif self.text_url is None:
        #     self.text_url = paper_or_plastic(rpt_id, url_pattern)

        # Display

    def load_to_mem(self, filetype=settings.DEFAULT_DELIM, url=None, file_path=None, local=True, reload=False):
        """
        DOCSTRING NEEDS REVSION:
        Load the raw data. If data is not None and reload is False, alert the user. If filetype is provided, it must be
        in FILE_TYPES, or user must provide url or file_path. If both url and file_path are available (either from the
        method call or by looking up those values in FILE_TYPES), the method will first try to get the data from an
        already downloaded file if local is True. Otherwise, it will try to download the data from the FEC first. User
        will get an alert if both methods fail.
        :param filetype:
        :param url:
        :param file_path:
        :param local:
        :param reload:
        :return:
        """
        pass

    def get_url(self, format):
        """
        Returns URL that be used to view the report online. Note that while this method only returns the URL, there also
        is a view_url method.

        :return:
        """
        pass

    def view_url(self, format):
        """
        Opens the report in a web browser in the specified format. This is most useful for viewing a report as a PDF
        that has not been downloaded or to view a report as a series of HTML pages.
        :return:
        """
        pass

    def remove_from_db(self):
        """
        Remove the report from the database.
        :return:
        """
        pass

    def delete_file(self, formats=None):
        """
        Remove the file from disk, if it exists. If formats is not specified, django will use FILE_TYPES to attempt to
        delete all known copies of the report.
        :param formats:
        :return:
        """
        pass

    def purge(self):
        """
        Delete the file, remove from database and garbage collect this object.
        :return:
        """
        pass

    def reload_all(self):
        """
        Delete the file (if it exists), remove it from the database (if loaded) and re-fetch the file from the FEC
        website.

        :return:
        """
        pass

    def parse(self):
        """
        This method prompts the user to run load_to_mem if data is None. The parse method then looks at the two header
        rows to determine the form type and header version, then passes these values to create the appropriate subclass,
        each of which must override the parent Report class' parse method.

        :return:
        """
        pass
