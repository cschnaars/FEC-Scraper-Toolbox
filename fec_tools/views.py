from django.shortcuts import render
from FEC_Toolbox import settings


class Report:
    """
    Report base class.
    """
    def __init__(self, rpt_id, down_now=settings.DOWN_NOW, mem_load=settings.MEM_LOAD,
                 db_load=[['ascii28'], settings.FILE_TYPES], destroy=False):
        """
        Report base class initialization.

        :param rpt_id: Report ID. Required. This is the ID assigned by the FEC for a specific report. It is used as the
        primary key for reports in the django database.
        :type rpt_id: integer

        :param down_now: Download now. Use this parameter to control whether the application automatically will download
        the specified Report ID in one or more formats upon instantiation. Leave this parameter unspecified to use
        default value (DOWN_NOW) specified in settings.py.
        :type down_now: list

        :param mem_load: Store report data in memory. Use this parameter to control whether the django application will
        download and retain a report's data in memory upon instantiation of the base Report class. Leave this parameter
        unspecified to use default value (MEM_LOAD) specified in settings.py.
        :type mem_load: list

        :param db_load: Load data into database upon instantiation. Leave this parameter unspecified to use default
        value (DB_LOAD) specified in settings.py.
        :type db_load: list

        :param destroy: Garbage collect this object after instantiation. This is useful if you only want to download a
        report and/or load its data into the database but do not otherwise need to inspect the data. Default is False.
        :type destroy: bool

        :return:
        """
        self.rpt_id = rpt_id

    def fetch(self, filetype, url=None, keep_in_mem=False, save_to_disk=False, save_path=None, overwrite=False):
        """
        If save path and/or url set to None, retrieve values from FILE_TYPES dictionary. Alert user and exit if filetype
        does not exist in FILE_TYPES to lookup values that have not been provided. Before downloading, check to see if
        file already exists. Alert user and take no other action if overwrite is set to False. Otherwise, download the
        file.
        :param filetype:
        :param url:
        :param keep_in_mem:
        :param save_to_disk:
        :param save_path:
        :param overwrite:
        :return:
        """
        pass

    def fech(self, filetype, url=None, keep_in_mem=False, save_to_disk=False, save_path=None, overwrite=False):
        """
        Calls fetch.
        :param filetype:
        :param url:
        :param keep_in_mem:
        :param save_to_disk:
        :param save_path:
        :param overwrite:
        :return:
        """
        pass

    def load_to_mem(filetype=DEFAULT_DELIM, url=None, file_path=None, local=True, reload=False):
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