from bs4 import BeautifulSoup
import requests

from FEC_Toolbox.settings.local import FILE_TYPES, DEFAULT_FILE_TYPE


def get_delimited_report_url(report_id, file_type=DEFAULT_FILE_TYPE, url_patterns=None, a_tag_id=None):
    """
    Determine a valid URL that can be used to download the specified report (rpt_id) in the desired format (file_type).

    The easiest way to use this function is to set file_type to a key in settings.FILE_TYPES. If this is done, values
    for url_patterns and a_tag_id will be retrieved from this dictionary. If file_type is not a key in
    settings.FILE_TYPES, this parameter is ignored and either url_patterns or a_tag_id must be set.

    It is not possible to use URL patterns to retrieve an electronically filed report in CSV format when that report has
    fewer than 1,000 rows. This is because the FEC website generates a random folder in the URL for these reports. To
    get a valid URL, set the a_tag_id parameter.

    :param report_id: Report ID. Required. This is the ID assigned by the FEC for a specific report. It is used as the
    primary key for reports in the database.
    :type report_id: str

    :param file_type: File type. Key used to look up default values in settings.FILE_TYPES. The function does not
    otherwise use or care about this variable. If this parameter is not provided, url_patterns or a_tag_id must be
    passed to the function.
    :type file_type: str

    :param url_patterns: URL patterns. List of patterns used by the function to attempt to construct a valid URL to
    download the specified report. You need to set this value only if file_type and a_tag_id are not set; file_type is
    not a key in settings.FILE_TYPES; or you want to override the default settings (the electronic_url_pattern and
    paper_url_pattern attributes) specified in settings.FILE_TYPES.
    :type url_patterns: list

    :param a_tag_id: <a> tag ID. Value of the id attribute of the <a> tag that houses a valid URL for the report.
    Generally speaking, the <a> tag should be necessary only when you are trying to download an electronically filed
    report with fewer than 1,000 rows in CSV format. You need to set this value only if file_type and url_patterns are
    not set; file_type is not a key in settings.FILE_TYPES; or you want to override the default setting (the a_tag_id
    attribute) specified in settings.FILE_TYPES.
    :type a_tag_id: str

    :return: The URL that can be used to download the report, or None if no valid URL has been determined.
    :rtype str
    """
    # Fetch URL patterns if not provided
    if url_patterns is None:
        url_patterns = []

        # Try to fetch patterns based on file_type
        if file_type in FILE_TYPES.keys():
            if FILE_TYPES[file_type]['electronic_url_pattern'] is not None:
                url_patterns.append(FILE_TYPES[file_type]['electronic_url_pattern'])
            if FILE_TYPES[file_type]['paper_url_pattern'] is not None:
                url_patterns.append(FILE_TYPES[file_type]['paper_url_pattern'])

        # Otherwise, try to fetch patterns based on a_tag_id:
        elif a_tag_id is not None:
            for key in FILE_TYPES.keys():
                if FILE_TYPES[key]['a_tag_id'] == a_tag_id and FILE_TYPES[key]['delimiter'] is not None:
                    if FILE_TYPES[key]['electronic_url_pattern'] is not None:
                        url_patterns.append(FILE_TYPES[key]['electronic_url_pattern'])
                    if FILE_TYPES[key]['paper_url_pattern'] is not None:
                        url_patterns.append(FILE_TYPES[key]['paper_url_pattern'])

    # Iterate through patterns to construct a valid URL
    for url_pattern in url_patterns:
        url = url_pattern.replace('<report_id>', report_id)
        x = requests.head(url)
        if x.status_code == 200:
            return url

    # If the function has not found a valid URL and an <a> tag is available, attempt to scrape the URL.
    # Note: This does not work for report of less than 1,000 rows filed on paper.
    if a_tag_id is None:
        if file_type in FILE_TYPES.keys():
            a_tag_id = FILE_TYPES[file_type]['a_tag_id']

    if a_tag_id is not None:
        base_url = 'http://docquery.fec.gov'
        url = base_url + '/cgi-bin/forms/DL/' + report_id
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        a_tag = soup.find("a", id=a_tag_id)
        if a_tag is None:
            pass
        elif 'href' in a_tag.attrs.keys():
            return base_url + a_tag['href']

    # No valid URL found
    return None
