import os
import requests

from fec_downloader.utils.get_report_url import get_report_url


class Report:
    """
    Report base class.
    """
    def __init__(self, report_id, delimiter=chr(28)):
        self.report_id = report_id
        self.delimiter = delimiter

    def download(self, delimiter=chr(28), download_tries=5, overwrite_file=False, chunk_size=1024*1024,
                 check_file_length=True, save_file_as=None, save_directory='C:/data/fec/reports/text/ascii28/',
                 save_file_extension='.txt'):
        """
        Download and save a specific report. You must set delimiter to either ',' or chr(28).

        :param delimiter: The delimiter used in the data. This parameter is passed to the get_report_url function and is
        not used directly by this method. If you set this parameter to either ',' or chr(28), url_patterns and
        a_tag_id will be determined automatically and any values set explicitly for those parameters ignored by
        get_report_url. The delimiter parameter is needed only so the get_report_url function can set the default
        url_patterns and a_tag_id. The delimiter is not used by this method to parse the data. If you want to override
        these defaults, set delimiter to None.
        :type delimiter: str

        :param download_tries: Download tries. Number of times the function should attempt to download the file before
        giving up.
        :type download_tries: int

        :param overwrite_file: Overwrite existing file. When set to True, the function will overwrite existing files
        without prompting the user.
        :type overwrite_file: bool

        :param chunk_size: File chunk size in bytes. Some files are large enough to cause memory errors on some systems.
        To get around this problem, report downloads are chunked. Set this value to the number of bytes that should be
        downloaded per chunk.
        :type chunk_size: int

        :param check_file_length: Check file length. When set to True, the function will compare the length of the
        downloaded file with the length of the file hosted on the FEC website. When the two lengths are not the same,
        the function will delete the downloaded file and might try to download it again, depending on the download_tries
        setting.
        :type check_file_length: bool

        :param save_file_as: Report save path. The full path that should be used to save the report. If this parameter
        is not provided, the method will attempt to retrieve save_path from the instance. If this value does not exist,
        the method will attempt to construct a save path using save_directory, the instance value of report_id and the
        optional save_file_extension. When save_file_as is provided, it overwrites self.save_path.
        NOT SURE ABOUT THIS BEHAVIOR. MAYBE I SHOULD STOP TRYING TO SAVE URLs AND OTHER INFO.
        :type save_file_as: str

        :param save_directory: The directory where the downloaded report should be saved. This parameter is ignored when
        save_file_as is supplied or self.save_path is not None.
        :type save_directory: str

        :param save_file_extension: An optional file extension for the downloaded report. This parameter is ignored when
        save_file_as is supplied or self.save_path is not None.
        :type save_file_extension: str

        :return: A two-item tuple containing a boolean value to indicate whether the download was successful and an
        optional message for the user/log.
        :rtype: tuple
        """

        # Exit if tries is invalid or < 0:
        try:
            if int(download_tries) < 1:
                return False, 'Report not downloaded. The download_tries parameter must be an integer >= 1.'
        except (TypeError, ValueError):
            return False, 'Report not downloaded. The download_tries parameter is invalid. Set to an integer >= 1.'

        # Determine a valid url.
        get_url = get_report_url(self.report_id, delimiter)
        if not get_url[0]:
            return False, get_url[1]
        url = get_url[1]

        # Make sure either save_file_as or save_directory was provided.
        if save_file_as is None:
            if save_directory is None:
                return False, 'You must provide a value for either the save_file_as or the save_directory parameter.'
            else:
                save_file_as = save_directory + self.report_id
                if save_file_extension is not None:
                    if not save_file_extension.startswith('.'):
                        save_file_as += '.'
                    save_file_as += save_file_extension

        # Make sure Python can write to the save directory
        if not os.access(os.path.dirname(save_file_as), os.W_OK):
            return False, 'Report not downloaded. The application lacks write permissions on that directory.'

        # Exit if file already downloaded and overwrite is False
        if not overwrite_file:
            if os.path.isfile(save_file_as):
                return False, 'Report not downloaded. File already exists, and overwriting the file is not allowed. ' \
                              'To override this behavior, delete the file or set overwrite_file to True.'

        # Get content-length of file to be downloaded, if check_file_length is True
        source_length = -1
        if check_file_length:
            try:
                source_length = int(requests.head(url).headers['content-length'])
            except ValueError:
                return False, 'Report not downloaded. Unable to determine file length via ' + url + '.'

        # Download the file
        for i in range(int(download_tries)):
            try:
                response = requests.get(url, stream=True)
                with open(save_file_as, mode='wb') as outfile:
                    for chunk in response.iter_content(chunk_size):
                        if chunk:
                            outfile.write(chunk)
                            outfile.flush()

                # Take no other action if user does not want to compare file lengths
                if not check_file_length:
                    return True, 'Report downloaded.'

                # Otherwise, compare length of downloaded file with source length
                save_length = os.path.getsize(save_file_as)

                # Exit loop if file downloaded and lengths are the same
                if source_length == save_length:
                    return True, 'Report downloaded.'

                # Otherwise, delete the file and try again
                if os.path.isfile(save_file_as):
                    os.remove(save_file_as)

                    # Return a message to the user if this was the last attempt to download
                    if i == download_tries - 1:
                        return False, 'Downloaded file did not match length of file posted at ' + url + '. ' \
                                      'Downloaded file deleted.'

            except PermissionError:
                return False, 'File not downloaded. The application might lack permission to write to this ' \
                              'directory, or the file might be write protected.'

        # If we get to this point, the file was not downloaded
        return False, 'The report could not be downloaded. Check the url (' + url + ') and save path (' + \
                      save_file_as + ').'

    # def header(self, reload=False):
    #     """
    #     Load and display data contained in the report's header.
    #
    #         :param reload: Force the method to ignore header data stored in memory and reload.
    #         :type reload: bool
    #
    #         :return: A two-item tuple containing a boolean value to indicate whether the download was successful and
    #         an optional message for the user/log.
    #         :rtype: tuple
    #     """
    #
    #     # Delete existing header from memory if reload True:
    #     if reload:
    #         self.header = None
    #
    #     # If header have already been loaded, just display.
    #     if self.header is not None:
    #         print('Displaying header previously loaded into memory.')
    #
    #         # Attempt to display header data; exit if successful
    #         # if display_header():
    #         #     return True, None
    #
    #     # If save_path exists, attempt to retrieve the file.
    #     if self.save_path:
    #         try:
    #             with open(self.save_path, encoding='utf-8') as report_file:
    #                 old_style_header = False
    #                 file_header_data = ''
    #                 report_header_data = ''
    #                 for line in report_file:
    #                     # Test whether this is an old style header
    #                     if line.lower().find('/* header') != -1:
    #                         old_style_header = True
    #                         file_header_data = line[:line.lower().find('/* header')] + \
    #                             line[line.lower().find('/* header') + 9:].strip()
    #                         continue
    #
    #                     if old_style_header:
    #                         if line.lower().find('/* end header') != -1:
    #                             old_style_header = False
    #                             file_header_data += '\n' + line[:line.lower().find('/* end header')] + \
    #                                 line[line.lower().find('/* end header') + 13:].strip()
    #                         else:
    #                             file_header_data += '\n' + line.strip()
    #                         continue
    #
    #                     if file_header_data == '':
    #                         file_header_data = line
    #                     else:
    #                         report_header_data = line
    #                         break
    #
    #         except FileNotFoundError:
    #             return False, 'The header could not be retrieved because the file at ' + self.save_path + ' could ' \
    #                 'not be found.'
    #
    #         except PermissionError:
    #             return False, 'The header could not be retrieved because of insufficient permissions to access the ' \
    #                 'file at ' + self.save_path + '.'

        # If there is no save path or save path is invalid, attempt to
        # retrieve header data from the database.
        # STILL NEED TO WRITE THIS CODE

        # As a last resort, attempt to fetch the report from the fec
        # website.

        # Fetch the first line of the file.

        # Convert the first line to a list.

        # Grab the second element of the list. If it's a paper report,
        # this is the header version. If not, grab the third element.

        # Verify the version retrieved is valid.

        # Load the pretty header.

        # Display the data. Do this in another method?

    # def display_header(self):
    #     pass
