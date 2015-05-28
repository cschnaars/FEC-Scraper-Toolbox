from bs4 import BeautifulSoup
import requests

from FEC_Toolbox.settings import FILE_TYPES


def get_delim_report_url(rpt_id, filetype=None, url_patterns=None, delim=None, a_id=None):
    """
    Determine a valid URL that can be used to download the specified report (rpt_id) in the desired format (filetype).
    If filetype is not a key in settings.FILE_TYPES, url_patterns and delim must be specified.

    :param rpt_id: Report ID. Required. This is the ID assigned by the FEC for a specific report. It is used as the
    primary key for reports in the django database.
    :type rpt_id: int

    :param filetype: File type. Key used to look up default values in settings.FILE_TYPES. The function does not
    otherwise use or care about this variable. If this parameter is not provided, url_patterns, delim and i_id must be
    passed to the function.
    :type filetype: str

    :param url_patterns: URL patterns. List of patterns used by the function to attempt to construct a valid URL to
    download the specified report. You need to set this value only if filetype is not set or is not a key in
    settings.FILE_TYPES or you want to override the default settings (the elec_url_pattern and paper_url_pattern
    attributes) specified in settings.FILE_TYPES.
    :type url_patterns: list

    :param delim: Delimiter. Delimiter used to parse reports downloaded in a text format, such as CSV or ASCII-28. You
    need to set this value only if filetype is not set or is not a key in settings.FILE_TYPES or you want to override
    the default setting (the delim attribute) specified in settings.FILE_TYPES.
    :type delim: str

    :param a_id: <a> tag ID. Value of the id attribute of the <a> tag that houses a valid URL for the report. Generally
    speaking, the <a> tag should be necessary only when you are trying to download an electronically filed report in
    CSV format. You need to set this value only if filetype is not set or is not a key in settings.FILE_TYPES or you
    want to override the default setting (the a_id attribute) specified for that key in settings.FILE_TYPES.
    :type a_id: str

    :return: str
    """

    # Fetch URL patterns if not provided
    if url_patterns is None:
        url_patterns = []

        if filetype in FILE_TYPES.keys():
            if FILE_TYPES[filetype]['elec_url_pattern'] is not None:
                url_patterns.append(FILE_TYPES[filetype]['elec_url_pattern'])
            if FILE_TYPES[filetype]['paper_url_pattern'] is not None:
                url_patterns.append(FILE_TYPES[filetype]['paper_url_pattern'])

    # Iterate through patterns to construct a valid URL
    for url_pattern in url_patterns:
        url = url_pattern.replace('<rpt_id>', str(rpt_id))
        x = requests.head(url)
        if x.status_code == 200:
            return url

    # If the function has not found a valid URL and a delimiter and <a> tag are available, attempt to scrape the URL.
    if delim is None:
        if filetype in FILE_TYPES.keys():
            delim = FILE_TYPES[filetype]['delim']

    if a_id is None:
        if filetype in FILE_TYPES.keys():
            a_id = FILE_TYPES[filetype]['a_id']

    if delim is not None and a_id is not None:
        base_url = 'http://docquery.fec.gov'
        url = base_url + '/cgi-bin/forms/DL/' + str(rpt_id)
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        a_tag = soup.find("a", id=a_id)
        if a_tag is None:
            pass
        elif 'href' in a_tag.attrs.keys():
            return base_url + a_tag['href']

    # Try to extract URL from JSON if url_patterns is empty list
    # Will either need committee ID or will have to attempt to download a text report and extract the committee ID.
    if url_patterns == []:

        ########################
        #   INSERT CODE HERE   #
        ########################
        pass
