import lambda_function
import json
import logging

logger = logging.getLogger().setLevel(logging.INFO)
logging.info('Starting test')

def do_test_lambda_handler(event, expectedOutput, description):
    context={}
    result=lambda_function.lambda_handler(event, context)
    logging.debug("Result:")
    logging.debug(result)

    if result == expectedOutput:
        logging.info("Test: \"" + description + "\" passed")
    else:
        logging.error("Test: \"" + description + "\" failed, expected " + str(expectedOutput) + ", got " + str(result))

do_test_lambda_handler({
  "queryStringParameters": {
    "filter": {
      "operator": "equals",
      "field": "field-1",
      "value": "abc"
    },
    "webhookurl": "https://localhost:1234"
  },
  "body": {
    "field-1": "abc",
    "field-2": "def"
  },
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}, {
  "statusCode": 500,
  "body": "Can not connect to remote server https://localhost:1234"
}, "Forward to non-existing server")

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
  },
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}, {
  "statusCode": 200,
  "body": "Message not forwarded"
}, "Message not forwarded")




do_test_lambda_handler({
  "queryStringParameters": {
    "filter": {
      "operator": "contains",
      "field": "fields.summary",
      "value": "Test Event"
    },
    #"webhookurl": "https://webhook.site/1657c436-9bfb-4916-aa9e-bd0f5a107458/rest/api/2/issue/",
    "webhookurl": "https://bjornvb.atlassian.net/rest/api/2/issue/",
    "webhookusername":"bvboe@pobox.com",
    "webhookpassword":"cTasyPGBrFVUbFL5hhH9FB32"
  },
  "body": {  
    "fields": {
      "summary": "Does this work???? Test Event",
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
  },
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}, {
  "statusCode": 200,
  "body": "Message not forwarded"
}, "JiraTest")


