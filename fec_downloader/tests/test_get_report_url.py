import unittest2

from fec_downloader.utils.get_report_url import get_report_url


# Tests for utils\get_report_url
class TestGetReportUrl(unittest2.TestCase):
    """
    Test reports:
    Electronic report with less than 1,000 rows: 1008299
    Electronic report with more than 1,000 rows: 877183
    Paper report with less than 1,000 rows: 1006117
    Paper report with more than 1,000 rows: 974135
    """
    def test_ascii28_electronic_less_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/dcdev/posted/1008299.fec'),
                         get_report_url('1008299', delimiter=chr(28)))

    def test_ascii28_electronic_greater_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/dcdev/posted/877183.fec'),
                         get_report_url('877183', delimiter=chr(28)))

    def test_ascii28_paper_less_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/paper/posted/1006117.fec'),
                         get_report_url('1006117', delimiter=chr(28)))

    def test_ascii28_paper_greater_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/paper/posted/974135.fec'),
                         get_report_url('974135', delimiter=chr(28)))

    def test_csv_electronic_less_than_1000_rows(self):
        """
        The xxx in the expected URL is a directory randomly generated
        by the FEC as part of the URL. This occurs only when trying
        to download an electronically filed report containing less
        than 1,000 lines in CSV format.
        """
        url = get_report_url('1008299', delimiter=',')[1]
        # Replace random folder name in url with xxx
        url_mod = url[:url.find('/showcsv/') + 9] + 'xxx' + url[len(url) - url[::-1].find('/') - 1:]
        self.assertEqual((True, 'http://docquery.fec.gov/showcsv/xxx/1008299.fec'), (True, url_mod))

    def test_csv_electronic_greater_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/comma/877183.fec'),
                         get_report_url('877183', delimiter=','))

    def test_csv_paper_less_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/paper/fecpprcsv/1006117.fec'),
                         get_report_url('1006117', delimiter=','))

    def test_csv_paper_greater_than_1000_rows(self):
        self.assertEqual((True, 'http://docquery.fec.gov/paper/fecpprcsv/974135.fec'),
                         get_report_url('974135', delimiter=','))

if __name__ == '__main__':
    unittest2.main()
