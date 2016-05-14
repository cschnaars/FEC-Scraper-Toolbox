import requests
from bs4 import BeautifulSoup


def get_report_url(report_id, delimiter=chr(28)):
    """
    Determine a valid URL that can be used to download the specified report in the desired format (file_type).

    The easiest way to use this function is to set delimiter to either chr(28) or ','. If this is done,
    values for url_patterns and a_tag_id will be calculated automatically.

    It is not possible to use URL patterns to retrieve an electronically filed report in CSV format (comma delimiter)
    when that report has fewer than 1,000 rows. This is because the FEC website generates a random folder in the URL for
    these reports. To get a valid URL, set the a_tag_id parameter.

    :param report_id: Report ID. Required. This is the ID assigned by the FEC for a specific report. It is used as the
    primary key for reports in the database.
    :type report_id: str

    :param delimiter: The delimiter used in the data. If you set this parameter to either a comma or chr(28),
    url_patterns and a_tag_id will be determined automatically and any values set explicitly for those parameters
    ignored. The delimiter parameter is needed only so the method can set the default url_patterns and a_tag_id. The
    delimiter is not used by this method to parse the data. If you want to override these defaults, set delimiter to
    None.
    :type delimiter: str

    :return: A two-item tuple containing a boolean value to indicate whether a valid URL was constructed and either the
    URL or a message for the user/log.
    :rtype tuple
    """

    # ASCII-28 delimiter
    if delimiter == chr(28):
        url_patterns = ['http://docquery.fec.gov/dcdev/posted/' + report_id + '.fec',
                        'http://docquery.fec.gov/paper/posted/' + report_id + '.fec']
        a_tag_id = 'asciifile'

    # CSV
    elif delimiter == ',':
        url_patterns = ['http://docquery.fec.gov/comma/' + report_id + '.fec',
                        'http://docquery.fec.gov/paper/fecpprcsv/' + report_id + '.fec']
        a_tag_id = 'csvfile'

    # Exit if invalid delimiter.
    else:
        return False, 'Report not downloaded. You must specify a valid delimiter.'

    # Iterate through patterns to check for a valid URL.
    for url in url_patterns:
        x = requests.head(url)
        if x.status_code == 200:
            return True, url

    # At this point, we don't have a valid url; try to retrieve from <a> tag.
    base_url = 'http://docquery.fec.gov/cgi-bin/forms/DL/'
    url = base_url + report_id
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    a_tag = soup.find("a", id=a_tag_id)
    if 'href' in a_tag.attrs.keys():
        base_csv_url = 'http://docquery.fec.gov/showcsv/'
        csv_url = base_csv_url + a_tag['href'] + '/' + report_id + '.fec'
        return True, csv_url

    # No valid URL found
    patterns_tried = ''
    if len(url_patterns) > 0:
        patterns_tried = ', '.join(map(str, url_patterns))
    msg = 'A valid url for this report could not be determined.'
    if patterns_tried != '':
        msg += ' Patterns tried: ' + patterns_tried
    else:
        msg += ' No url patterns found.'
    return False, msg
