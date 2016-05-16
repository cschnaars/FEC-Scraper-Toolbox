import glob
import os
import tempfile
import unittest2

from fec_downloader.report import Report


class TestDownloadReport(unittest2.TestCase):
    """
    Short test reports (<=1 KB): 1071819, 1071830, 1071839, 1071846, 1071856, 1071857, 1071858
    """
    def setUp(self):
        self.delimiter = chr(28)
        self.report_id = '1071819'
        self.save_directory = tempfile.mkdtemp()
        self.save_file_extension = '.csv'
        self.save_file_name = os.path.join(self.save_directory, self.report_id) + self.save_file_extension

    def tearDown(self):
        for datafile in glob.glob(os.path.join(self.save_directory, '*.*')):
            os.remove(datafile)
        os.rmdir(self.save_directory)

    def test_download_ascii28_with_save_file_as(self):
        x = Report(self.report_id)
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=self.delimiter, check_file_length=True,
                         save_file_as=self.save_file_name, overwrite_file=True, download_tries=1))

    def test_download_ascii28_with_save_directory_and_extension(self):
        x = Report(self.report_id)
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=self.delimiter, check_file_length=True,
                         save_directory=self.save_directory, save_file_extension=self.save_file_extension,
                         overwrite_file=True, download_tries=1))

    def test_download_ascii28_with_save_directory_and_extension_without_dot(self):
        x = Report(self.report_id)
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=self.delimiter, check_file_length=True,
                         save_directory=self.save_directory, save_file_extension=self.save_file_extension.lstrip('.'),
                         overwrite_file=True, download_tries=1))

    def test_download_ascii28_with_save_directory_and_no_extension(self):
        x = Report(self.report_id)
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=self.delimiter, check_file_length=True,
                         save_directory=self.save_directory, save_file_extension='',
                         overwrite_file=True, download_tries=1))

    def test_download_ascii28_with_overwrite_false(self):
        x = Report(self.report_id)
        y = Report(self.report_id)
        x.download(delimiter=self.delimiter, check_file_length=True, save_file_as=self.save_file_name,
                   overwrite_file=True, download_tries=1)
        self.assertEqual((False, 'Report not downloaded. File already exists, and overwriting the file is not allowed. '
                                 'To override this behavior, delete the file or set overwrite_file to True.'),
                         y.download(delimiter=self.delimiter, check_file_length=True, save_file_as=self.save_file_name,
                                    overwrite_file=False, download_tries=1))

    def test_download_ascii28_with_zero_tries(self):
        x = Report(self.report_id)
        self.assertEqual((False, 'Report not downloaded. The download_tries parameter must be an integer >= 1.'),
                         x.download(delimiter=self.delimiter, check_file_length=True,
                                    save_file_as=self.save_file_name, overwrite_file=True, download_tries=0))

    def test_download_ascii28_with_string_tries(self):
        x = Report(self.report_id)
        self.assertEqual((False, 'Report not downloaded. The download_tries parameter is invalid. Set to an integer >= '
                                 '1.'), x.download(delimiter=self.delimiter, check_file_length=True,
                                                   save_file_as=self.save_file_name, overwrite_file=True,
                                                   download_tries='abc'))

    def test_download_ascii28_with_none_tries(self):
        x = Report(self.report_id)
        self.assertEqual((False, 'Report not downloaded. The download_tries parameter is invalid. Set to an integer >= '
                                 '1.'), x.download(delimiter=self.delimiter, check_file_length=True,
                                                   save_file_as=self.save_file_name, overwrite_file=True,
                                                   download_tries=None))

    def test_download_ascii28_with_check_file_length_false(self):
        x = Report(self.report_id)
        self.assertEqual((True, 'Report downloaded.'), x.download(delimiter=self.delimiter, check_file_length=False,
                         save_file_as=self.save_file_name, overwrite_file=True, download_tries=1))


if __name__ == '__main__':
    unittest2.main()
