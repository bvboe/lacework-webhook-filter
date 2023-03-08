import lambda_function
import json
import logging
import os

logger = logging.getLogger().setLevel(logging.WARN)
logging.info('Starting test')

def do_test_lambda_handler(event, expectedOutput, description):
    context={}
    result=lambda_function.lambda_handler(event, context)
    logging.debug("Result:")
    logging.debug(result)

    if result == expectedOutput:
        logging.warning("Test: \"" + description + "\" passed")
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
}, "No filter, forward to non-existing server")

do_test_lambda_handler({
  "queryStringParameters": {
    "webhookurl": "https://localhost:1234"
  },
  "body": {},
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}, {
  "statusCode": 500,
  "body": "Can not connect to remote server https://localhost:1234"
}, "Empty payload, empty filter")

do_test_lambda_handler({
  "queryStringParameters": {
    "webhookurl": "https://localhost:1234"
  },
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}, {
  "statusCode": 500,
  "body": "Can not connect to remote server https://localhost:1234"
}, "Completely empty payload, empty filter")

do_test_lambda_handler({
  "queryStringParameters": {
    "filter": {
      "operator": "equals",
      "field": "field-1",
      "value": "abc"
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
}, "Completely empty payload, filter set")
