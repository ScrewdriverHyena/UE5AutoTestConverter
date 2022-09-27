
import json
from xml.dom import minidom

UNREAL_TEST_REPORT_PATH: str = 'C:/TestReports/index.json'

index = open(UNREAL_TEST_REPORT_PATH, encoding='utf-8-sig')
data = json.load(index)

root = minidom.Document()

testsuites = root.createElement('testsuites')
testsuites.setAttribute('id', '0')
testsuites.setAttribute('name', 'Unreal Tests')
testsuites.setAttribute('tests', str(data['succeeded'] + data['failed']))
testsuites.setAttribute('failures', str(data['failed']))
testsuites.setAttribute('time', str(data['totalDuration']))

testsuite = root.createElement('testsuite')
testsuite.setAttribute('id', '1')
testsuite.setAttribute('name', 'Unreal Test Suite')
testsuite.setAttribute('tests', str(data['succeeded'] + data['failed']))
testsuite.setAttribute('failures', str(data['failed']))
testsuite.setAttribute('time', str(data['totalDuration']))

for testcasedata in data['tests']:
    testcase = root.createElement('testcase')
    testcase.setAttribute('id', testcasedata['fullTestPath'])
    testcase.setAttribute('name', testcasedata['testDisplayName'])
    testcase.setAttribute('time', '0.0')

    if testcasedata['state'] == "Fail":
        for entry in testcasedata['entries']:
            if entry['event']['type'] != "Error":
                continue

            failure = root.createElement('failure')
            failure.setAttribute('message', entry['event']['message'])
            failure.setAttribute('type', entry['event']['type'])
            testcase.appendChild(failure)
    
    testsuite.appendChild(testcase)

testsuites.appendChild(testsuite)
root.appendChild(testsuites)

xml = root.toprettyxml(indent ="\t")
junit_file = "junit.xml"

with open(junit_file, 'w') as f:
    f.write(xml)