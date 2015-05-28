import unittest

import fec_tools.lib.get_report_url


# Tests for lib\get_report_url
class TestGetReportUrl(unittest.TestCase):
    def test_ascii28_elec(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/1008299.fec',
                         fec_tools.lib.get_report_url.get_report_url(1008299, 'ascii28'))

    def test_ascii28_paper(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/1006117.fec',
                         fec_tools.lib.get_report_url.get_report_url(1006117, 'ascii28'))

    def test_csv_elec_gt_1000_rows(self):
        self.assertEqual('http://docquery.fec.gov/comma/877183.fec',
                         fec_tools.lib.get_report_url.get_report_url(877183, 'csv'))

    def test_csv_elec_lt_1000_rows(self):
        """
        The xxx in the expected URL is a randomly generated folder in the actual URL.
        """
        url = fec_tools.lib.get_report_url.get_report_url(1008299, 'csv')
        url_mod = url[:url.find('/showcsv/') + 9] + 'xxx' + url[url.find('/showcsv/') + 16:]
        self.assertEqual('http://docquery.fec.gov/showcsv/xxx/1008299.fec', url_mod)

    def test_csv_paper(self):
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/1006117.fec',
                         fec_tools.lib.get_report_url.get_report_url(1006117, 'csv'))


if __name__ == '__main__':
    unittest.main()
