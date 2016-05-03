import unittest

from ..lib.get_delimited_report_url import get_delimited_report_url


# Tests for lib\get_report_url
class TestGetReportUrl(unittest.TestCase):
    """
    Test reports:
    Electronic report with less than 1,000 rows: 1008299
    Electronic report with more than 1,000 rows: 877183
    Paper report with less than 1,000 rows: 1006117
    Paper report with more than 1,000 rows: 974135

    It is not possible to use URL patterns to retrieve an electronically filed report in CSV format when that report has
    fewer than 1,000 rows. This is because the FEC website generates a random folder in the URL for these reports. To
    get a valid URL, set the a_id parameter.
    """
    def test_ascii28_elec_lt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/1008299.fec',
                         get_delimited_report_url('1008299', file_type='ascii28'))

    def test_ascii28_elec_gt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/877183.fec',
                         get_delimited_report_url('877183', file_type='ascii28'))

    def test_ascii28_paper_lt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/1006117.fec',
                         get_delimited_report_url('1006117', file_type='ascii28'))

    def test_ascii28_paper_gt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/974135.fec',
                         get_delimited_report_url('974135', file_type='ascii28'))

    def test_csv_elec_lt_1000_file_type(self):
        """
        The xxx in the expected URL is a randomly generated folder in the actual URL.
        """
        url = get_delimited_report_url('1008299', file_type='csv')
        # Replace random folder name with xxx
        url_mod = url[:url.find('/showcsv/') + 9] + 'xxx' + url[len(url) - url[::-1].find('/') - 1:]
        self.assertEqual('http://docquery.fec.gov/showcsv/xxx/1008299.fec', url_mod)

    def test_csv_elec_gt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/comma/877183.fec',
                         get_delimited_report_url('877183', file_type='csv'))

    def test_csv_paper_lt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/1006117.fec',
                         get_delimited_report_url('1006117', file_type='csv'))

    def test_csv_paper_gt_1000_file_type(self):
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/974135.fec',
                         get_delimited_report_url('974135', file_type='csv'))

    def test_ascii28_elec_lt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/1008299.fec',
                         get_delimited_report_url('1008299', url_patterns=[
                             'http://docquery.fec.gov/dcdev/posted/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/posted/<rpt_id>.fec']))

    def test_ascii28_elec_gt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/877183.fec',
                         get_delimited_report_url('877183', url_patterns=[
                             'http://docquery.fec.gov/dcdev/posted/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/posted/<rpt_id>.fec']))

    def test_ascii28_paper_lt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/1006117.fec',
                         get_delimited_report_url('1006117', url_patterns=[
                             'http://docquery.fec.gov/dcdev/posted/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/posted/<rpt_id>.fec']))

    def test_ascii28_paper_gt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/974135.fec',
                         get_delimited_report_url('974135', url_patterns=[
                             'http://docquery.fec.gov/dcdev/posted/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/posted/<rpt_id>.fec']))

    def test_csv_elec_lt_1000_url_patterns(self):
        """
        It is not possible to use URL patterns to retrieve an electronically filed report in CSV format when that
        report has fewer than 1,000 rows. This is because the FEC website generates a random folder in the URL for
        these reports. To get a valid URL, set the a_id parameter.
        """
        pass

    def test_csv_elec_gt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/comma/877183.fec',
                         get_delimited_report_url('877183', url_patterns=[
                             'http://docquery.fec.gov/comma/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/fecpprcsv/<rpt_id>.fec']))

    def test_csv_paper_lt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/1006117.fec',
                         get_delimited_report_url('1006117', url_patterns=[
                             'http://docquery.fec.gov/comma/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/fecpprcsv/<rpt_id>.fec']))

    def test_csv_paper_gt_1000_url_patterns(self):
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/974135.fec',
                         get_delimited_report_url('974135', url_patterns=[
                             'http://docquery.fec.gov/comma/<rpt_id>.fec',
                             'http://docquery.fec.gov/paper/fecpprcsv/<rpt_id>.fec']))

    def test_ascii28_elec_lt_1000_a_id(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/1008299.fec',
                         get_delimited_report_url('1008299', a_tag_id='asciifile'))

    def test_ascii28_elec_gt_1000_a_id(self):
        self.assertEqual('http://docquery.fec.gov/dcdev/posted/877183.fec',
                         get_delimited_report_url('877183', a_tag_id='asciifile'))

    def test_ascii28_paper_lt_1000_a_id(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/1006117.fec',
                         get_delimited_report_url('1006117', a_tag_id='asciifile'))

    def test_ascii28_paper_gt_1000_a_id(self):
        self.assertEqual('http://docquery.fec.gov/paper/posted/974135.fec',
                         get_delimited_report_url('974135', a_tag_id='asciifile'))

    def test_csv_elec_lt_1000_a_id(self):
        """
        The xxx in the expected URL is a randomly generated folder in the actual URL.
        """
        url = get_delimited_report_url('1008299', a_tag_id='csvfile')
        # Replace random folder name with xxx
        url_mod = url[:url.find('/showcsv/') + 9] + 'xxx' + url[len(url) - url[::-1].find('/') - 1:]
        self.assertEqual('http://docquery.fec.gov/showcsv/xxx/1008299.fec', url_mod)

    def test_csv_elec_gt_1000_a_id(self):
        self.assertEqual('http://docquery.fec.gov/comma/877183.fec',
                         get_delimited_report_url('877183', a_tag_id='csvfile'))

    def test_csv_paper_lt_1000_a_id(self):
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/1006117.fec',
                         get_delimited_report_url('1006117', a_tag_id='csvfile'))

    def test_csv_paper_gt_1000_a_id(self):
        # Failed
        self.assertEqual('http://docquery.fec.gov/paper/fecpprcsv/974135.fec',
                         get_delimited_report_url('974135', a_tag_id='csvfile'))

if __name__ == '__main__':
    unittest.main()
