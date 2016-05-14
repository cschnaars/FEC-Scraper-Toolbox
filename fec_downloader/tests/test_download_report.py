import os
import unittest2

from fec_downloader.report import Report


# Tests for lib\download_report
class TestDownloadReport(unittest2.TestCase):
    """
    Short test reports (<=1 KB): 1071819, 1071830, 1071839, 1071846, 1071856, 1071857, 1071858
    """
    @staticmethod
    def ascii_28_directory():
        return 'C:/data/fec/test/reports/text/ascii28/'

    @staticmethod
    def csv_directory():
        return 'C:/data/fec/test/reports/text/csv/'

    @staticmethod
    def report_id():
        return '1071819'

    @staticmethod
    def remove_file(file_name):
        if os.path.isfile(file_name):
            os.remove(file_name)

    def test_download_none_delimiter_with_defaults(self):
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        x = Report(self.report_id)
        self.assertEqual((False, 'Report not downloaded. You must specify a valid delimiter.'),
                         x.download(delimiter=None, save_file_as=save_file_name))

    def test_download_invalid_delimiter_with_defaults(self):
        x = Report(self.report_id())
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        self.assertEqual((False, 'Report not downloaded. You must specify a valid delimiter.'),
                         x.download(delimiter='abc', save_file_as=save_file_name))

    def test_download_ascii28_with_save_file_as(self):
        x = Report(self.report_id())
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        self.remove_file(save_file_name)
        self.assertEqual((True, 'Report downloaded.'),
                         x.download(delimiter=chr(28), save_file_as=save_file_name))

    def test_verify_download_ascii28_with_save_file_as(self):
        x = Report(self.report_id())
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        self.remove_file(save_file_name)
        x.download(delimiter=chr(28), save_file_as=save_file_name)
        self.assertEqual(True, os.path.isfile(save_file_name))

    def test_download_csv_with_save_file_as(self):
        x = Report(self.report_id())
        save_file_name = self.csv_directory() + self.report_id() + '.csv'
        self.remove_file(save_file_name)
        self.assertEqual((True, 'Report downloaded.'),
                         x.download(delimiter=',', save_file_as=save_file_name))

    def test_verify_download_csv_with_save_file_as(self):
        x = Report(self.report_id())
        save_file_name = self.csv_directory() + self.report_id() + '.csv'
        self.remove_file(save_file_name)
        x.download(delimiter=',', save_file_as=save_file_name)
        self.assertEqual(True, os.path.isfile(save_file_name))

    def test_download_ascii28_with_save_directory_and_extension(self):
        x = Report(self.report_id())
        self.remove_file(self.ascii_28_directory() + self.report_id() + '.txt')
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=chr(28),
                                                                  save_directory=self.ascii_28_directory(),
                                                                  save_file_extension='.txt'))

    def test_verify_download_ascii28_with_save_directory_and_extension(self):
        x = Report(self.report_id())
        self.remove_file(self.ascii_28_directory() + self.report_id() + '.txt')
        x.download(delimiter=chr(28), save_directory=self.ascii_28_directory(), save_file_extension='.txt')
        self.assertEqual(True, os.path.isfile(self.ascii_28_directory() + self.report_id() + '.txt'))

    def test_download_csv_with_save_directory_and_extension(self):
        x = Report(self.report_id())
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=',',
                                                                  save_directory=self.csv_directory(),
                                                                  save_file_extension='.csv'))

    def test_verify_download_csv_with_save_directory_and_extension(self):
        x = Report(self.report_id())
        self.remove_file(self.csv_directory() + self.report_id() + '.csv')
        x.download(delimiter=',', save_directory=self.csv_directory(), save_file_extension='.csv')
        self.assertEqual(True, os.path.isfile(self.csv_directory() + self.report_id() + '.csv'))

    def test_download_ascii28_with_save_directory_and_extension_without_dot(self):
        x = Report(self.report_id())
        self.remove_file(self.ascii_28_directory() + self.report_id() + '.txt')
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=chr(28),
                                                                  save_directory=self.ascii_28_directory(),
                                                                  save_file_extension='txt'))

    def test_verify_download_ascii28_with_save_directory_and_extension_without_dot(self):
        x = Report(self.report_id())
        self.remove_file(self.ascii_28_directory() + self.report_id() + '.txt')
        x.download(delimiter=chr(28), save_directory=self.ascii_28_directory(), save_file_extension='txt')
        self.assertEqual(True, os.path.isfile(self.ascii_28_directory() + self.report_id() + '.txt'))

    def test_download_csv_with_save_directory_and_extension_without_dot(self):
        x = Report(self.report_id())
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=',',
                                                                  save_directory=self.csv_directory(),
                                                                  save_file_extension='csv'))

    def test_verify_download_csv_with_save_directory_and_extension_without_dot(self):
        x = Report(self.report_id())
        self.remove_file(self.csv_directory() + self.report_id() + '.csv')
        x.download(delimiter=chr(28), save_directory=self.csv_directory(), save_file_extension='csv')
        self.assertEqual(True, os.path.isfile(self.csv_directory() + self.report_id() + '.csv'))

    def test_download_ascii28_with_save_directory_and_no_extension(self):
        x = Report(self.report_id())
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=chr(28),
                                                                  save_directory=self.ascii_28_directory(),
                                                                  save_file_extension=''))
        self.assertEqual(True, os.path.isfile(self.ascii_28_directory() + self.report_id()))

    def test_download_csv_with_save_directory_and_no_extension(self):
        x = Report(self.report_id())
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=',', save_directory=self.csv_directory(),
                                                                  save_file_extension=''))
        self.assertEqual(True, os.path.isfile(self.csv_directory() + self.report_id()))

    def test_download_ascii28_with_zero_tries(self):
        x = Report(self.report_id())
        self.assertEqual((False, 'Report not downloaded. The tries parameter must be an integer >= 1.'),
                         x.download(delimiter=chr(28), download_tries=0))

    def test_download_csv_with_zero_tries(self):
        x = Report(self.report_id())
        self.assertEqual((False, 'Report not downloaded. The tries parameter must be an integer >= 1.'),
                         x.download(delimiter=',', download_tries=0))

    def test_download_ascii28_with_string_tries(self):
        x = Report(self.report_id())
        self.assertEqual((False, 'Report not downloaded. The tries parameter is invalid. Set to an integer >= 1.'),
                         x.download(delimiter=chr(28), download_tries='abc'))

    def test_download_csv_with_string_tries(self):
        x = Report(self.report_id())
        self.assertEqual((False, 'Report not downloaded. The tries parameter is invalid. Set to an integer >= 1.'),
                         x.download(delimiter=',', download_tries='abc'))

    def test_download_ascii28_with_none_tries(self):
        x = Report(self.report_id())
        self.assertEqual((False, 'Report not downloaded. The tries parameter is invalid. Set to an integer >= 1.'),
                         x.download(delimiter=chr(28), download_tries=None))

    def test_download_csv_with_none_tries(self):
        x = Report(self.report_id())
        self.assertEqual((False, 'Report not downloaded. The tries parameter is invalid. Set to an integer >= 1.'),
                         x.download(delimiter=',', download_tries=None))

    def test_download_ascii28_with_overwrite_false(self):
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        x = Report(self.report_id())
        y = Report(self.report_id())
        x.download(delimiter=chr(28), save_file_as=save_file_name)
        self.assertEqual((False, 'Report not downloaded. File already exists, and overwriting the file is not allowed. '
                                 'To override this behavior, delete the file or set overwrite_file to True.'),
                         y.download(delimiter=chr(28), save_file_as=save_file_name, overwrite_file=False))

    def test_download_csv_with_overwrite_false(self):
        save_file_name = self.csv_directory() + self.report_id() + '.csv'
        x = Report(self.report_id())
        y = Report(self.report_id())
        x.download(delimiter=',', save_file_as=save_file_name)
        self.assertEqual((False, 'Report not downloaded. File already exists, and overwriting the file is not allowed. '
                                 'To override this behavior, delete the file or set overwrite_file to True.'),
                         y.download(delimiter=',', save_file_as=save_file_name, overwrite_file=False))

    def test_download_ascii28_with_overwrite_true(self):
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        x = Report(self.report_id())
        y = Report(self.report_id())
        x.download(delimiter=chr(28), save_file_as=save_file_name)
        self.assertEqual((True, 'Report downloaded.'), y.download(delimiter=chr(28), save_file_as=save_file_name,
                                                                  overwrite_file=True))

    def test_download_csv_with_overwrite_true(self):
        save_file_name = self.csv_directory() + self.report_id() + '.csv'
        x = Report(self.report_id())
        y = Report(self.report_id())
        x.download(delimiter=',', save_file_as=save_file_name)
        self.assertEqual((True, 'Report downloaded.'), y.download(delimiter=',', save_file_as=save_file_name,
                                                                  overwrite_file=True))

    def test_download_ascii28_with_check_file_length_false(self):
        x = Report(self.report_id())
        save_file_name = self.ascii_28_directory() + self.report_id() + '.txt'
        self.assertEqual((True, 'Report downloaded.'),
                         x.download(delimiter=chr(28), save_file_as=save_file_name, check_file_length=False))

    def test_download_csv_with_check_file_length_false(self):
        x = Report(self.report_id())
        save_file_name = self.csv_directory() + self.report_id() + '.csv'
        self.assertEqual((True, 'Report downloaded.'),
                         x.download(delimiter=',', save_file_as=save_file_name, check_file_length=False))


if __name__ == '__main__':
    # Make sure test directories exist
    # if not os.path.isdir(ascii28_test_directory):
    #     os.mkdir(ascii28_test_directory)
    # if not os.path.isdir(csv_test_directory):
    #     os.mkdir(csv_test_directory)

    unittest2.main()
