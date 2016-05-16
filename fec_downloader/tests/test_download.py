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
        self.delimiter = ','
        self.report_id = '1071819'
        self.save_directory = tempfile.mkdtemp()
        self.save_file_extension = '.csv'
        self.save_file_name = os.path.join(self.save_directory, self.report_id) + self.save_file_extension

    def tearDown(self):
        for datafile in glob.glob(os.path.join(self.save_directory, '*.*')):
            os.remove(datafile)
        os.rmdir(self.save_directory)

    def test_download_none_delimiter_with_defaults(self):
        x = Report(self.report_id)
        self.assertEqual((False, 'Report not downloaded. You must specify a valid delimiter.'),
                         x.download(delimiter=None, check_file_length=True, save_file_as=self.save_file_name,
                                    overwrite_file=True, download_tries=1))

    def test_download_invalid_delimiter_with_defaults(self):
        x = Report(self.report_id)
        self.assertEqual((False, 'Report not downloaded. You must specify a valid delimiter.'),
                         x.download(delimiter='abc', check_file_length=True, save_file_as=self.save_file_name,
                                    overwrite_file=True, download_tries=1))


if __name__ == '__main__':
    unittest2.main()
