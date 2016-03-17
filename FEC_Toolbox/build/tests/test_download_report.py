import os
import unittest

from ..lib.download_report import download_report
from ..lib.get_delim_report_url import get_delim_report_url
from ...settings.local import FILE_TYPES, REPORTS_DIR, TEST_DIR


# Tests for lib\download_report
class TestDownloadReport(unittest.TestCase):
    """
    Test reports:
    Electronic report with less than 1,000 rows: 1008299
    xxx Electronic report with more than 1,000 rows: 877183
    Paper report with less than 1,000 rows: 1006117
    xxx Paper report with more than 1,000 rows: 974135
    """

    def test_down_pdf_with_defaults(self):
        # Still need to write code to download PDFs
        pass

    def test_down_csv_with_defaults(self):
        self.assertEqual((True, 'File downloaded.'), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext']))

    def test_down_asc28_with_defaults(self):
        self.assertEqual((True, 'File downloaded.'), download_report(
            url=get_delim_report_url(1008299, file_type='ascii28'),
            save_path=FILE_TYPES['ascii28']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['ascii28']['ext']))

    def test_down_csv_with_zero_tries(self):
        msg = 'File not downloaded. The tries parameter must be an integer >= 1.'
        self.assertEqual((False, msg), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'], tries='0'))

    def test_down_csv_with_string_tries(self):
        msg = 'File not downloaded. The tries parameter is invalid. Set to an integer >= 1.'
        self.assertEqual((False, msg), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'], tries='x'))

    def test_down_csv_with_overwrite_true(self):
        self.assertEqual((True, 'File downloaded.'), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'],
            overwrite=True))

    def test_down_csv_with_overwrite_false(self):
        msg = 'File not downloaded. File already exists, and overwriting the file is not allowed. To override this ' \
            'behavior, delete the file or set the overwrite parameter to True.'
        self.assertEqual((False, msg), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'],
            overwrite=False))

    def test_down_csv_with_chunk_size(self):
        self.assertEqual((True, 'File downloaded.'), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'],
            chunk_size=512 * 1024))

    def test_down_csv_with_ck_file_len_true(self):
        self.assertEqual((True, 'File downloaded.'), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'],
            ck_file_len=True))

    def test_down_csv_with_ck_file_len_false(self):
        self.assertEqual((True, 'File downloaded.'), download_report(
            url=get_delim_report_url(1008299, file_type='csv'),
            save_path=FILE_TYPES['csv']['save_path'].replace(REPORTS_DIR, TEST_DIR) + '1008299.' +
            FILE_TYPES['csv']['ext'],
            ck_file_len=False))

if __name__ == '__main__':
    # Make sure test directories exist
    if not os.path.isdir(TEST_DIR):
        os.mkdir(TEST_DIR)
    for file_type in FILE_TYPES:
        test_dir = FILE_TYPES[file_type]['save_path'].replace(REPORTS_DIR, TEST_DIR)
        sub_dirs = test_dir.replace(TEST_DIR, '')
        for i in range(len(sub_dirs)):
            if sub_dirs[i] != '/':
                continue
            if not os.path.isdir(TEST_DIR + sub_dirs[:i]):
                os.mkdir(TEST_DIR + sub_dirs[:i])
    unittest.main()
