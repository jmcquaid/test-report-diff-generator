Test-report-diffs
=======================
Script that generates a report of the differences between multiple xunit test report (xml) files. 
- Lists the suite, test case and (pass/fail) status for each test whose status varied across reports.
- Useful for summarising failure diffs across test runs.

Requirements
------------
Linux/Unix OS. The project does not yet support windows file paths.

Installation
------------
```python
git clone https://github.com/jmcquaid/test-report-diffs.git
python setup.py install
```

Usage
-----
python testreportdiffs/create_junit_diff_report.py folders.txt

- folders.txt is a list of file paths for the xunit xml report files.