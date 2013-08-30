# FEC Scraper Toolbox
The FEC Scraper Toolbox is series of Python modules you can use to find
and download electronically filed campaign finance reports housed on
the Federal Election Commission website and load those reports into a
database manager. It replaces the [FEC Scraper](https://github.com/cschnaars/FEC-Scraper) repository.

Presently, the toolbox consists of three major modules. I am in the
process of cleaning up and documenting my code and will post these
modules as I go. At this time, only the first module is ready to go and
has been posted on Github.

FEC Scraper Toolbox has been developed and tested under Python 2.7.4.

## Requirements
The following modules are required to use FEC Scraper Toolbox. All of
them are included with a standard Python 2.7.4 installation.
installation:
* ftplib
* glob
* multiprocessing
* os
* pickle
* re
* urllib
* urllib2
* zipfile

## User Settings
You can add an optional usersettings.py file to the directory housing
your Python modules to customize database connection strings and file
locations. In each module, you'll see a try statement, where the module
will attempt to load this file. Default values can be specified in the
except portion of the try statement.

You can copy and paste the text below into your usersettings.py file,
then set the values you want to use.

    ARCPROCDIR = '' # Directory to house archives that have been processed
    ARCSVDIR = '' # Directory to house archives that have been downloaded but not processed
    RPTHOLDDIR = '' # Directory to house electronically filed reports that cannot be processed
    RPTPROCDIR = '' # Directory to house electronically filed reports that have been processed
    RPTSVDIR = '' # Directory to house electronically filed reports that have been downloaded but not processed

## download_reports module
This module tracks and downloads all electronically filed reports
housed on the Federal Election Commission website.  Specifically, it
ensures all daily archives of reports (which go back to 2001) have been
downloaded and extracted.  It then consumes the FEC's RSS feed listing
all reports filed within the past seven days to look for new reports.

Electronic reports filed voluntarily by a handful of Senators presently
are not included here.

This module does not load any data or otherwise interact with a
database manager (though I plan to add functionality to ping a database
to build a list of previously downloaded reports rather than require
the user to warehouse them). Its sole purpose is to track and download
reports.

If you don't want to download archives back to 2001 or otherwise want
to manually control what is downloaded, you'll find commented out code
below as well as in the module that you can use to modify the zipinfo.p
pickle (which is described in the first bullet point below).

This module goes through the following process in this order:
* Uses pickle to attempt to load zipinfo.p, a dictionary housing the
    name of the most recent archive downloaded as well as a list of
    files not downloaded previously.  Commented out code available
    below and in the module can be used to modify this pickle if you
    want to control which archives will be retrieved.
* Calls build_prior_archive_list to build a list of archives that
    already have been downloaded and saved to ARCPROCDIR or ARCSVDIR.
    __NOTE:__ I plan to deprecate this function.  I added this feature for
    development and to test the implementation of the zipinfo.p pickle.
    Using the pickle saves a lot of time and disk space compared to
    warehousing all the archives.
* Calls build_archive_download_list, which processes the zipinfo.p
    pickle to build a list of available archive files that have not
    been downloaded.
* Uses multiprocessing and calls download_archive to download each
    archive file.  These files are saved in the directory specified
    with the ARCSVDIR variable.  After downloading an archive, the
    subroutine compares the length of the downloaded file with the
    length of the source file and will try to download a file up to
    five times.
* Uses multiprocessing and calls unzip_archive to extract any files in
    the archive that have not been downloaded previously.  The second
    parameter is an overwrite flag; existing files are overwritten when
    this flag is set to 1.  Default is 0.
* Again calls build_prior_archive_list to build a list of archives that
    already have been downloaded and saved to ARCPROCDIR or ARCSVDIR.
    __NOTE:__ As stated above, this feature is slated for deprecation.
* Calls pickle_archives to rebuild zipinfo.p and save it in the same
    directory as this module.
* Calls build_prior_report_list to build a list of reports housed in
    RPTHOLDDIR, RPTPROCDIR and RPTSVDIR.
    __NOTE:__ I plan to add a function that can build a list of previously
    processed files using a database call rather than combing RPTPROCDIR.
* Calls consume_rss, which uses a regular expression to scan an FEC RSS
    feed listing all electronically filed reports submitted within the
    past seven days.  The function returns a list of these reports.
* Calls verify_reports to test whether filings filed for download by
    consume_rss already have been downloaded. If so, the function
    verifies the length of the downloaded file matches the length of
    the file posted on the FEC website.  When the lengths do not match,
    the saved file is deleted and retained in the download list.
* Uses multiprocessing and calls download_report to download each
    report returned by verify_reports.  This subroutine verifies the
    length of each downloaded file and will attempt to download a file
    up to five times.

### Modifying the zipinfo pickle
Here is the commented-out code available in the download_reports module
that you can use to manually control the zipinfo.p pickle if you don't
want to download all available archives back to 2001:

```python
    # Set mostrecent to the last date you DON'T want, so if you want
    # everything since Jan. 1, 2013, set mostrecent to: '20121231.zip'
    zipinfo['mostrecent'] = '20121231.zip' # YYYYMMDD.zip
    zipinfo['badfiles'] = [] # You probably want to leave this blank
```