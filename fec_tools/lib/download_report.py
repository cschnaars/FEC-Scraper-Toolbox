import os
import requests

from FEC_Toolbox.settings import DOWN_TRIES, DOWN_OVERWRITE, DOWN_VERIFY, DOWN_CHUNK_SIZE


def download_report(url, save_path, tries=DOWN_TRIES, overwrite=DOWN_OVERWRITE, chunk_size=DOWN_CHUNK_SIZE,
                    ck_file_len=DOWN_VERIFY):
    """
    Download a specific report found at url and save it to save_path.

    :param url: Report URL. The download URL for a specific report to be downloaded.
    :type url: str

    :param save_path: Report save path. The full path that should be used to save the report.
    :type save_path: str

    :param tries: Download tries. Number of times the function should attempt to download the file before giving up.
    :type tries: int

    :param overwrite: Overwrite existing file. When set to True, the function will overwrite existing files without
    prompting the user.
    :type overwrite: bool

    :param chunk_size: File chunk size. Some files are large enough to cause memory errors on some systems. To get
    around this problem, report downloads are chunked. Set this value to the number of bytes that should be downloaded
    per chunk.
    :type chunk_size: int

    :param ck_file_len: Check file length. When set to True, the function will compare the length of the downloaded file
    with the length of the file hosted on the FEC website. When the two lengths are not the same, the function will
    delete the downloaded file and might try to download it again, depending on the tries setting.
    :type ck_file_len: bool

    :return: A two-item tuple containing a boolean value to indicate whether the download was successful and an
    optional message for the user/log.
    :rtype: tuple
    """

    # Exit if tries is invalid or < 0:
    try:
        if int(tries) < 1:
            return False, 'File not downloaded. The tries parameter must be an integer >= 1.'
    except ValueError:
        return False, 'File not downloaded. The tries parameter is invalid. Set to an integer >= 1.'

    # Get content-length of file to be downloaded, if ck_file_len is True
    src_len = 0
    if ck_file_len:
        try:
            response = requests.head(url)
            src_len = int(response.headers['content-length'])
        except ValueError:
            return False, 'File not downloaded. Unable to determine length of file to be downloaded.'

    # Exit if file already has been downloaded and overwrite is False
    if not overwrite:
        if os.path.isfile(save_path):
            return False, 'File not downloaded. File already exists, and overwriting the file is not allowed. To ' \
                'override this behavior, delete the file or set the overwrite parameter to True.'

    # Download the file
    for i in range(int(tries)):
        try:
            response = requests.get(url, stream=True)
            with open(save_path, 'wb') as outfile:
                for chunk in response.iter_content(chunk_size):
                    if chunk:
                        outfile.write(chunk)
                        outfile.flush()

            # Take no other action if user does not want to compare file lengths
            if not ck_file_len:
                return True, 'File downloaded.'

            # Otherwise, compare length of downloaded file with source length
            dest_len = os.path.getsize(save_path)

            # Exit loop if file downloaded and lengths are the same
            if src_len == dest_len:
                return True, 'File downloaded.'

            # Otherwise, delete the file and try again
            if os.path.isfile(save_path):
                os.remove(save_path)

        except FileNotFoundError:
            try:
                os.mkdir(save_path[:len(save_path) - save_path[::-1].find('/')])
            except PermissionError:
                return False, 'File not downloaded. Directory does not exist, and insufficient permissions to create.'

        except PermissionError:
            return False, 'File not downloaded. Either the application lacks permission to write to this directory ' \
                'or the file already exists and is read only.'

    # If we get to this point, the file was not downloaded
    return False, 'The file could not be downloaded. Check the url and save_path parameters.'
