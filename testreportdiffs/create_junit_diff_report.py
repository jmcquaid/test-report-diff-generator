import xml.etree.cElementTree as ET
import os
import sys
import argparse

def get_report_paths_file_name():
    """
    Get the file path supplied on the command line by user. 
    This file contains a list of file paths- for the unit test report files.
    """
    parser = argparse.ArgumentParser(
        description='Create diff report from multiple xunit report.xml files.'
        )
    parser.add_argument(
        'report_paths_file', 
        metavar='paths_file',
        help='A path to a file containing report.xml file paths.')
    args = parser.parse_args()
    return args.report_paths_file

def clean_path_strings(file_paths):
    """
    Remove end of line chars from list of file_paths
    """
    clean_paths = []
    print "List of report.xml files that will be used in diff report:"
    for i in file_paths:
    	clean_path = i.replace("\n", "")
        clean_paths.append(clean_path)
        print clean_path
    return clean_paths

def get_directory_name(file_path_str):
    """
    Return the (base) folder name for the specified file path. This will
    identify the report on the diff report.
    """
    return os.path.basename(os.path.dirname(file_path_str))

def create_diff_report(report_paths):
    """
    Merge the specified reports and create a single summary report
    
    :param report_paths: file paths for report.xml in xunit folder
    :type list
        
    :returns:
        String (html markup)
    """
    print "Generating report ...."

    html_str = ('<table style="width:100%"> \n '
            '<tr> <th>Suite</th> <th>TestCase</th>')

    # Add headings for the status of each of the files:
    for ele in report_trees:
        html_str = html_str + '<th>{0}</th>'.format(ele['folder_name'])
    
    for suite_name in get_test_suite_names():
        for test_case_name in get_test_case_names(suite_name):
            # Get statuses for all of the files
            statuses = []

            for ele in report_trees:
                report_tree = ele['xml_tree']
                status = make_status_pretty(
                            test_case_passed(report_tree, 
                                             suite_name, 
                                             test_case_name)
                )
                statuses.append(status)
            if not statuses_same(statuses):
                html_str = html_str + '<tr><td>{0}</td><td>{1}</td>'.format(
                    suite_name, 
                    test_case_name
                    )

                for status in statuses:
                    html_str = html_str + '<td>{0}</td>\n'.format(status)

                html_str = html_str + '</tr>'
    html_str = html_str + '</table>'
    return html_str

def get_test_suite_names():
    """
    Return list of all suite names in xml report tree
    """    
    # It doesn't matter which report we get the suite names from-
    # so we pick the first one
    report_tree = report_trees[0]['xml_tree']
    doc = report_tree.getroot()
    l = []
    
    for elem in doc.findall('testsuite'):
        l.append(elem.get('name'))
    return l

def get_test_case_names(suite_name):
    
    # It doesn't matter which report we get the suite names from-
    # so we pick the first one
    report_tree = report_trees[0]['xml_tree']
    doc = report_tree.getroot()
    test_case_names = []
    for elem in doc.findall("testsuite[@name='{0}']/testcase".format(
                    suite_name)):
        name = elem.get('name')
        test_case_names.append(name)
    return test_case_names

def test_case_passed(tree, suite_name, test_case_name):
    """
    Determine if a test case in a specified testsuite passed
    """
    doc = tree.getroot()
    test_case_names = []
    test_case_elems = doc.findall(
        "testsuite[@name='{0}']/testcase[@name='{1}']".format(
            suite_name, 
            test_case_name
            )
        )

    if len(test_case_elems) == 0:
        raise Exception("Test case : {0} not in test suite: {1}!!!".format(
            test_case_name, 
            suite_name)
        )
    
    # If test has failed there will be a failure elem in the testcase node
    test_case_failure_elems = doc.findall(
        "testsuite[@name='{0}']/testcase[@name='{1}']/failure".format(
            suite_name, 
            test_case_name
            )
        )

    if len(test_case_failure_elems) == 0:
        return True
    else:
        return False

def make_status_pretty(status):
    if status:
        return "PASS"
    else:
        return "FAIL"

def statuses_same(statuses):
	"""
	Determine if a list of statuses (pass/fail) are the same
	"""
	statuses_set = set(statuses)
	return len(statuses_set) == 1

def output_report(merged_report):
    """
    Output report string to file
    
    :param merged_report: html representation of the summary of all xunit 
    report.xml files. 
    :type string
    """
    output_file = "regression_test_diffs.html" 
    with open(output_file, "w+") as html_file:
        html_file.write(merged_report)

    print "Report generation complete- output file: {0}".format(output_file)

def suite_passed(report_tree, suite_name):
    """
    Determine if suite passed
    """    
    return get_number_of_suite_failures(report_tree, suite_name) == 0

def get_number_of_suite_failures(report_tree, suite_name):
    """
    Get number of suite failures
    """
    doc = tree.getroot()
    for elem in doc.findall('testsuite'):
        name = elem.get('name')
        if name == suite_name:
            return int(elem.get("failures"))                
    raise Exception("Suite {0} not in report!!".format(suite_name))


# Generate report- using list of paths supplied by user
report_paths_file_name = get_report_paths_file_name()

with open(report_paths_file_name) as f:
    report_paths = f.readlines()

report_paths = clean_path_strings(report_paths)

# Xml report trees
report_trees = []
for i in report_paths:
    d = {'folder_name': get_directory_name(i),
         'xml_tree': ET.parse(i)}
    report_trees.append(d)
        
# Merge all xunit reports and create a single summary report
diff_report = create_diff_report(report_paths)

# Output report to a file
output_report(diff_report)
