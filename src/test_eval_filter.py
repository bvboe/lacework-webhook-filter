import lambda_function
import json

def do_test_eval_filter(filter, data, expectedOutput, description):
    result=lambda_function.eval_filter(filter, data)
    if result == expectedOutput:
        print("Test: \"" + description + "\" passed")
    else:
        print("Test: \"" + description + "\" failed, expected " + str(expectedOutput) + ", got " + str(result))

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
