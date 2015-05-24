import requests

def paper_or_plastic(rpt_id, url_patterns):
    """
    This script attempts to determine a valid report URL. URL patterns for reports originally filed on paper (Senate)
    differ from patterns for electronically filed reports.

    :param rpt_id:
    :param url_patterns:
    :return:
    """

    for pattern in url_patterns:
        x = requests.head(pattern)
        if x.status_code == 200:
            return pattern

    # No valid pattern found
    return None

