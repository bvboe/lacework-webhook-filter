import lambda_function
import json
import logging

logger = logging.getLogger().setLevel(logging.INFO)
logging.info('Starting test')

def do_test_eval_filter(filter, data, expectedOutput, description):
    result=lambda_function.eval_filter(filter, data)
    if result == expectedOutput:
        logging.info("Test: \"" + description + "\" passed")
    else:
        logging.error("Test: \"" + description + "\" failed, expected " + str(expectedOutput) + ", got " + str(result))

do_test_eval_filter({
  "operator": "equals",
  "field": "field-1.field-1-1",
  "value": "abc"
}, {
  "field-1": {"field-1-1": "abc"},
  "field-2": "def"
}, True, "Nested equals return true")

do_test_eval_filter({
  "operator": "equals",
  "field": "field-1.field-1-1",
  "value": "abc"
}, {
  "field-1": {"field-1-1": "qqq"},
  "field-2": "def"
}, False, "Nested equals return false")

do_test_eval_filter({
  "operator": "equals",
  "field": "field-1.field-1-1",
  "value": "abc"
}, {
  "field-1": "abc",
  "field-2": "def"
}, False, "Nested equals return false - nested field don't exist")

do_test_eval_filter({
  "operator": "equals",
  "field": "field-1",
  "value": "abc"
}, {
  "field-1": "abc",
  "field-2": "def"
}, True, "Simple equals return true")

do_test_eval_filter({
  "operator": "equals",
  "field": "field-1",
  "value": "abc"
}, {
  "field-1": "abd",
  "field-2": "def"
}, False, "Simple equals return false")

do_test_eval_filter({
  "operator": "equals",
  "field": "field-1",
  "value": "abc"
}, {
  "field-dont-exist": "abc",
  "field-2": "def"
}, False, "Equals, field missing")

do_test_eval_filter({
  "operator": "contains",
  "field": "field-1",
  "value": "abc"
}, {
  "field-1": "aaaaabcdddd",
  "field-2": "def"
}, True, "Contains, return true")

do_test_eval_filter({
  "operator": "contains",
  "field": "field-1",
  "value": "abc"
}, {
  "field-1": "xyz",
  "field-2": "def"
}, False, "Contains, return false")

do_test_eval_filter({
  "operator": "contains",
  "field": "field-1",
  "value": "abc"
}, {
  "field-1111": "aaaaabcdddd",
  "field-2": "def"
}, False, "Contains, missing field")

do_test_eval_filter({
  "operator": "not",
  "filter": {
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  }
}, {
  "field-1": "abc",
  "field-2": "def"
}, False, "Not equals, return false")

do_test_eval_filter({
  "operator": "not",
  "filter": {
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  }
}, {
  "field-1": "qqq",
  "field-2": "def"
}, True, "Not equals, return true")

do_test_eval_filter({
  "operator": "and",
  "filters": [{
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  },
  {
    "operator": "equals",
    "field": "field-2",
    "value": "def"
  }]
}, {
  "field-1": "abc",
  "field-2": "def"
}, True, "And filter, return true")

do_test_eval_filter({
  "operator": "and",
  "filters": [{
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  },
  {
    "operator": "equals",
    "field": "field-2",
    "value": "def"
  }]
}, {
  "field-1": "abc",
  "field-2": "qqq"
}, False, "And filter, return false")

do_test_eval_filter({
  "operator": "or",
  "filters": [{
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  },
  {
    "operator": "equals",
    "field": "field-2",
    "value": "def"
  }]
}, {
  "field-1": "abc",
  "field-2": "def"
}, True, "Or filter, return true")

do_test_eval_filter({
  "operator": "or",
  "filters": [{
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  },
  {
    "operator": "equals",
    "field": "field-2",
    "value": "def"
  }]
}, {
  "field-1": "abc",
  "field-2": "qqq"
}, True, "Or filter, partial, return true")

do_test_eval_filter({
  "operator": "or",
  "filters": [{
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  },
  {
    "operator": "equals",
    "field": "field-2",
    "value": "def"
  }]
}, {
  "field-1": "qqq",
  "field-2": "def"
}, True, "Or filter, partial ii, return true")

do_test_eval_filter({
  "operator": "or",
  "filters": [{
    "operator": "equals",
    "field": "field-1",
    "value": "abc"
  },
  {
    "operator": "equals",
    "field": "field-2",
    "value": "def"
  }]
}, {
  "field-1": "qqq",
  "field-2": "qqq"
}, False, "Or filter, return false")

do_test_eval_filter({
  "operator": "in",
  "field": "field-1",
  "values": ["aaa", "abc"]
}, {
  "field-1": "abc",
  "field-2": "def"
}, True, "Simple in return true")

do_test_eval_filter({
  "operator": "in",
  "field": "field-1",
  "values": ["aaa", "bbb"]
}, {
  "field-1": "abc",
  "field-2": "def"
}, False, "Simple in return false")

do_test_eval_filter({
  "operator": "in",
  "field": "field-1",
  "values": []
}, {
  "field-1": "abc",
  "field-2": "def"
}, False, "Empty in operator")

do_test_eval_filter({
  "operator": "true"
}, {
  "field-1": "abc",
  "field-2": "def"
}, True, "True operator")

do_test_eval_filter({
  "operator": "false"
}, {
  "field-1": "abc",
  "field-2": "def"
}, False, "False operator")

do_test_eval_filter({
  "operator": "contains",
  "field": "fields.summary",
  "value": "Test Event"
}, {
  "fields": {
    "summary": "Event: 0 (20 Jan 2023 19:33 GMT) Test Event",
    "description": "This is a test Message.\n\n*Details*\n|Event Id|0|\n|Event Type|TestEvent|\n|Event Category|TestEvent|\n|Severity|0|\n|Start Time|20 Jan 2023 19:33 GMT|\n|Link|[Event Link | https://login.lacework.net]|\n|LW Account Name|LWINT-SE-BJORNBOE|\n\n\n",
    "issuetype": {
      "name": "Candidate"
    },
    "project": {
      "key": "LT"
    },
    "priority": {
      "id": "5"
    }
  }
}
, True, "Jira test")
