# FEC Scraper Toolbox
The FEC Scraper Toolbox is a series of Python modules you can use to
find and download electronically filed campaign finance reports housed
on the Federal Election Commission website and load those reports into
a database manager.

Generally, the FEC Scraper Toolbox is meant to replace the [FEC Scraper](https://github.com/cschnaars/FEC-Scraper)
repository.  You might want to use the older repository, however, if
you want to limit the scope of your database to include only specific
committees.  The default behavior of the FEC Scraper Toolbox is to
download every available report whereas FEC Scraper downloads reports
only for the committees you specify.

Presently, the Toolbox consists of three major modules.  I am in the
process of cleaning up and documenting my code and will post these
modules as I go.  At this time, the first two modules are ready to go
and posted on Github.  (The final module, parse_reports, loads the
header rows of each report into the database and parses all child rows
into a separate file for each schedule.)

FEC Scraper Toolbox has been developed and tested under Python 2.7.4.

## Requirements
The following modules are required to use FEC Scraper Toolbox. All of
them are included with a standard Python 2.7.4 installation:
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
will attempt to load this file.  Default values can be specified in the
except portion of the try statement.

You can copy and paste the text below into your usersettings.py file,
then specify the values you want to use.

```python
    ARCPROCDIR = '' # Directory to house archives that have been processed
    ARCSVDIR = '' # Directory to house archives that have been downloaded but not processed
    MASTERDIR = '' # Master directory for weekly candidate and committee master files
    RPTHOLDDIR = '' # Directory to house electronically filed reports that cannot be processed
    RPTPROCDIR = '' # Directory to house electronically filed reports that have been processed
    RPTSVDIR = '' # Directory to house electronically filed reports that have been downloaded but not processed
```

## download_reports Module
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
the user to warehouse them).  Its sole purpose is to track and download
reports.

If you don't want to download archives back to 2001 or otherwise want
to manually control what is downloaded, you'll find commented out code
below as well as in the module that you can use to modify the zipinfo.p
pickle (which is described in the first bullet point below).

This module goes through the following process in this order:
* Uses the pickle module to attempt to load zipinfo.p, a dictionary
    housing the name of the most recent archive downloaded as well as a
    list of files not downloaded previously.  Commented out code available
    below and in the module can be used to modify this pickle if you
    want to control which archives will be retrieved.
* Calls build_prior_archive_list to construct a list of archives that
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
    subroutine compares the length of the downloaded file with the length
    of the source file.  If the lengths do not match, the file is deleted
    from the file system.  The subroutine tries to download a file up to
    five times.  
    __NOTE:__ You can set the NUMPROC variable in the user variables section
    to specify the number of downloads that occur simultaneously.  The
    default value is 10.
* Uses multiprocessing and calls unzip_archive to extract any files in
    the archive that have not been downloaded previously.  The second
    parameter is an overwrite flag; existing files are overwritten when
    this flag is set to 1.  Default is 0.  
    __NOTE:__ You can set the NUMPROC variable in the user variables section
    to specify the number of downloads that occur simultaneously.  The
    default value is 10.
* Again calls build_prior_archive_list to reconstruct the list of
    archives that already have been downloaded and saved to ARCPROCDIR or
    ARCSVDIR.  
    __NOTE:__ As stated above, this feature is slated for deprecation.
* Calls pickle_archives to rebuild zipinfo.p and save it to the same
    directory as this module.
* Calls build_prior_report_list to build a list of reports housed in
    RPTHOLDDIR, RPTPROCDIR and RPTSVDIR.  
    __NOTE:__ I plan to add a function that can build a list of previously
    processed files using a database call rather than combing the file
    system (though it will remain necessary to look in the RPTHOLDDIR and
    RPTSVDIR directories to find files that have not been loaded into the
	database).
* Calls consume_rss, which uses a regular expression to scan an FEC RSS
    feed listing all electronically filed reports submitted within the
    past seven days.  The function returns a list of these reports.
* Calls verify_reports to test whether filings flagged for download by
    consume_rss already have been downloaded.  If so, the function
    verifies the length of the downloaded file matches the length of
    the file posted on the FEC website.  When the lengths do not match,
    the saved file is deleted and retained in the download list.
* Uses multiprocessing and calls download_report to download each
    report returned by verify_reports.  After downloading a report, the
    subroutine compares the length of the downloaded file with the length
    of the source file.  If the lengths do not match, the file is deleted
    from the file system. The subroutine tries to download a file up to
    five times.  
    __NOTE:__ You can set the NUMPROC variable in the user variables section
    to specify the number of downloads that occur simultaneously. The
    default value is 10.

### Modifying the zipinfo Pickle
Here is the commented-out code available in the download_reports module
that you can use to manually control the zipinfo.p pickle if you don't
want to download all available archives back to 2001:

```python
    # Set mostrecent to the last date you DON'T want, so if you want
    # everything since Jan. 1, 2013, set mostrecent to: '20121231.zip'
    zipinfo['mostrecent'] = '20121231.zip' # YYYYMMDD.zip
    zipinfo['badfiles'] = [] # You probably want to leave this blank
```

## download_master_files Module
This module can be used to download and extract the weekly master files
housed on the [FEC website](http://www.fec.gov/finance/disclosure/ftpdet.shtml).  The FEC updates these files every Sunday
evening.

### Warehousing Master Files
By default, the download_master_files module archives the compressed
master files downloaded each week (but not the extracted data files).
  This was done to preserve the source data during development and
because the FEC overwrites the data each week.

To disable this behavior, set the value of the ARCHIVEFILES user
variable (see the user variables section near the top of the module) to
zero. When ARCHIVEFILES is set to any value other than one (1), the
master files are not archived.

### How the download_master_files Module Works
This module goes through the following process in this order:
* Calls delete_data to remove all .txt and .zip files from the working
    directory specified by the MASTERDIR variable. (The .zip files from the
    previous week will be in this directory only if they were not
    archived the week before.)
* Uses multiprocessing and calls download_file to download each master
    file specified by the MASTERFILES user variable. (By default, all nine
    master files are downloaded.) These files are saved in the directory
    specified by the MASTERDIR variable.  
    After downloading a file, the subroutine compares the length of the
    downloaded file with the length of the source file of the FEC
    website.  If the lengths do not match, the file is deleted from the
    file system. The subroutine tries to download a file up to five times.  
    __NOTE:__ You can set the NUMPROC variable in the user variables section
    to specify the number of downloads that occur simultaneously.  The
    default value is 10.
* Uses multiprocessing and calls unzip_master_file to extract the data
    files from each master file.  If the extracted filename does not
    include a year reference, the subroutine appends a two-digit year.  
    __NOTE:__ You can set the NUMPROC variable in the user variables section
    to specify the number of downloads that occur simultaneously.  The
    default value is 10.
* When the ARCHIVEFILES user variable is set to 1, the module calls the
    archive_master_files subroutine, which creates a YYYYMMDD directory for
    the most recent Sunday date (if that directory does not already exist)
    and moves all .zip files in the MASTERDIR directory to the new
    directory.

### About the Master Files
The FEC recreates the master files every Sunday evening, overwriting
the master files posted the week before. The archive filenames include
a two-digit year to identify the election cycle, but the files housed
in those archives often do not. For that reason, this module appends a
two-digit election cycle to extracted filenames that do not include a year
reference.

There are nine compressed files for each election cycle. You can click
the links below to view the data dictionary for a particular file:
* __add:__ [New Individual Contributions](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividualsAdditions.shtml)
    Lists all contributions added to the master Individuals file in the
    past week.  
    Files extracted from these archives are named addYYYY.txt.
* __ccl:__ [Candidate Committee Linkage](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCandCmteLinkage.shtml)  
    Houses all links between candidates and committees that have
    been reported to the FEC. Strangely, this file does not include
    candidate ties to Leadership PACs, which are reported on Form 1.  
    Files extracted from these archives are named ccl.txt.
* __changes:__ [Individual Contribution Changes](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividualsChanges.shtml)
    Lists all transactions in the master Individuals file that have been
    changed during the past month.  
    Files extracted from these archives are
    named chgYYYY.txt.
* __cm:__ [Committee Master File](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCommitteeMaster.shtml)  
    Lists all committees registered with the FEC for a
    specific election cycle. Among other information, you can use this file
    to see a committee's FEC ID, name, address and treasurer. You can use
    the Committee Designation field (CMTE_DSGN) to find a specific
    committee type (such as principal campaign committees, joint
    fundraisers, lobbyist PACs and leadership pacs). Additionally, you can
    look for code O in the Committee Type field (CMTE_TP) to identify
    independent expenditure only committees commonly known as Super PACs.  
    Files extracted from these archives are named cm.txt.
* __cn:__ [Candidate Master File](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCandidateMaster.shtml)
    Lists all candidates registered with the FEC for a
    specific election cycle. You can use this file to see all candidates
    who have filed to run for a particular seat as well as information
    about their political parties, addresses, treasurers and FEC IDs.  
    Files extracted from these archives are named cn.txt.
* __delete:__ [Deleted Individual Contributions](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividualsDeletes.shtml)
    Lists all contributions deleted from the master Individuals file in the
    past week.  
    Files extracted from these archives are named delYYYY.txt.
* __indiv:__ [Individual Contributions](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml)
    For the most part, lists all itemized contributions of $200 or more
    made by INDIVIDUALS to any committee during the election cycle. Does
    not include most contributions from businesses, PACs and other
    organizations.  
    Files extracted from these archives are named itcont.txt.
* __oth:__ [Committee-to-Committee Transactions](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCommitteetoCommittee.shtml)
    Lists contributions and independent expenditures made by one committee
    to another.  
    Files extracted from these archives are named itoth.txt.
* __pas2:__ [Committee-to-Candidate Transactions](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml)
    Lists contributions made by a committee to a candidate.  
    Files extracted from these archives are named itpas2.txt.

### Using the indiv, add, changes and delete files
The indiv file generated every Sunday for each election cycle is
comprehensive, meaning it is a current (as of that Sunday) snapshot of
all individual contributions currently in the database.  Many users
simply drop and recreate this table every week.  If you do this, you do
not need the add, changes and delete files.  The FEC generates these
files to provide an alternative to rebuilding the indiv table each
week simply because of the sheer volume of data it houses.

I presently don't use any of these files and instead rely on the raw
filings themselves, which are immediately available on the FEC website
once they're filed and contain more data that the indiv files.  But
many journalists I know who do use these files say they just rebuild
the indiv table each week because it's easier and less error-prone than
trying to patch it each week.

If you decide to use the add, changes and delete files rather than
rebuild the indiv table each week, just be aware that if you ever miss
a weekly download, you will have to rebuild the indiv table.

## Next Steps
I house all of my campaign-finance data in a SQL Server database and
tend to use SQL Server Integration Services packages to load the data
generated/extracted by the FEC Scraper Toolbox.  I do this because of
the sheer volume of the data (The table housing all Schedule A data,
for example, contains more than 120 million rows so far.) and because I
can use SSIS to bulk load the data rather than load it from Python a
row at a time.

The lone exception is the parse_reports module (which I have not posted
yet).  That module attempts to load a report's header row into the
database to test whether that report previously has been loaded.  All
child rows in new reports are parsed and moved to separate data files
(one for Schedule A, one for Schedule B and so on).

Understandably, the lack of code to load the data makes the Toolbox
less attractive to some potential users, who must manually import the
data files or develop their own Pythonic means of doing
so.  Nevertheless, the modules presently provide very fast and efficient
means of downloading massive quantities of data, managing that data and
preparing it for import.

At some point, I plan to develop Python functions to handle the data
imports, and of course I welcome any contributions from the open-source
community. I also plan to open source my entire database design so
others can recreate it in any database manager they choose.

Stay tuned!
