import lambda_function
import json
import logging

logger = logging.getLogger().setLevel(logging.INFO)
logging.info('Starting test')

def do_test_getfield(field, data, expectedOutput, description):
    result=lambda_function.getField(field, data)
    if result == expectedOutput:
        logging.info("Test: \"" + description + "\" passed")
    else:
        logging.error("Test: \"" + description + "\" failed, expected " + str(expectedOutput) + ", got " + str(result))

do_test_getfield("field-1",
{
  "field-1": "abc",
  "field-2": "def"
}, "abc", "Simple retrieve")

do_test_getfield("field-a",
{
  "field-1": "abc",
  "field-2": "def"
}, None, "Retrieve non-existing field")

do_test_getfield("field-1.field-1-1",
{
  "field-1": {"field-1-1": "abc"},
  "field-2": "def"
}, "abc", "Nested retrieve")

do_test_getfield("field-1.field-1-1",
{
  "field-1": {"field-2": "abc"},
  "field-2": "def"
}, None, "Nested retrieve, not exist")

do_test_getfield("field-1.field-1-1",
{
  "field-2": {"field-2-2": "abc"},
  "field-2": "def"
}, None, "Nested retrieve, not exist")

do_test_getfield("field-1.field-1-1",
{
  "field-1": "abc",
  "field-2": "def"
}, None, "Nested retrieve, not exist")
