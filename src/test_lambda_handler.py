import lambda_function
import json

def do_test_lambda_handler(event, expectedOutput, description):
    context={}
    result=lambda_function.lambda_handler(event, context).get('body')

    if result == expectedOutput:
        print("Test: \"" + description + "\" passed")
    else:
        print("Test: \"" + description + "\" failed, expected " + str(expectedOutput) + ", got " + str(result))

do_test_lambda_handler({
  "queryStringParameters": {
    "filter": {
      "operator": "equals",
      "field": "field-1",
      "value": "abc"
    }
  },
  "body": {
    "field-1": "abc",
    "field-2": "def"
  }
}, True, "Simple test")

do_test_lambda_handler({
  "queryStringParameters": {
    "filter": {
      "operator": "equals",
      "field": "field-1",
      "value": "abc"
    }
  },
  "body": {
    "field-1": "aaa",
    "field-2": "def"
  }
}, False, "Simple test")
