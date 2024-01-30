# OSINT Search and File Analysis

## Google Dorks

Solution steps: 

1. Navigate to google.com
    *  Note: The following "dorks" can be entered in any order. 
1. Enter the following "dorks" into the search bar, adding onto the search query each time: 
    * site:microsoft.com
        * There should be over 100 million results. 
    * filetype:pdf
      * Should be down to about 150,000 results.
    * language:en
      * Should be under 20,000 results now!
1.  Finally, just add "wasabi" to the search bar as a keyword.
    * Should be down to five of results!
1. Review the preview text for the remaining search results to find the one PDF that talks about buying wasabi in Phoenix. 
1. Open the PDF, and note the authors listed at the top. 
1. The answer/flag the last name of the first listed author, Bauer.

Flag/Answer: Bauer

* Link to PDF for refernce: 
  * https://www.microsoft.com/en-us/research/uploads/prod/2016/04/2016-ProductSearch.pdf

* Example, full dork:
  * site:microsoft.com filetype:pdf language:en wasabi

## File Analysis

Solution steps: 

There are several ways to view metadata for files, starting with those that are most accessible during the CTF:

* Open the file in a raw text editor, then Ctrl+F for target field, Producer.
  * This may be the easiest way to get the flag.
* Use an online file metadata viewer.
  * Recommend: metadata2go.com as one that is less spammy.
  * Never upload sensitive or private files!
* Use the `strings <filename>` command on the file.
  * This comes pre-installed on some Mac and Linux systems.
  * Can then pipe the output to `grep`(*nix)/`findstr`(Windows)
    * `strings <filename> | grep Producer`
* Use a purpose-built forensics tool like `exiftool` from exiftool.org
  * Probably not recommended during the CTF since it requires installation, etc.

Flag/Answer: MiKTeX