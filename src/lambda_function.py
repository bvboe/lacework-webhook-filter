import logging
import json
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Retrieved new message!')
    logger.info(event)
    logger.info(context)
    
    logger.info('Load filter')
    filter=load_parameter(event, 'filter')
    logger.info('Load Webhook URL')
    webhookUrl=load_parameter(event, 'webhookurl')
    
    logger.info('Load body')
    data=event.get('body')

    logger.info('Parse filter')
    filter=parse_json(filter)
    logger.info('Parse body')
    data=parse_json(data)

    logger.info('Evaluate filter')
    result=eval_filter(filter, data)
    
    if result == True and webhookUrl is not None:
        logger.info('Forward data using Webhook')
        requests.put(webhookUrl, headers={'Content-type': 'application/json'}, data=json.dumps(data))
    else:
        logger.info('Do not forward data')

    logger.info('End processing message!')
    return {
        'statusCode': 200,
        'body': result
    }

def load_parameter(event, parameter):
    queryStringParameters=event.get('queryStringParameters')
    if queryStringParameters is None:
        r=os.getenv(parameter)
    else:
        r=queryStringParameters.get(parameter)
        if r is None:
            r=os.getenv(parameter)
    return r
    
def parse_json(input):
    if isinstance(input, dict):
        return input
    else:
        return json.loads(input)

def eval_filter(filter, data):
    operator=filter.get('operator')

    if operator == 'equals':
        return eval_equals(filter, data)
    elif operator == 'contains':
        return eval_contains(filter, data)
    elif operator == 'in':
        return eval_in(filter, data)
    elif operator == 'not':
        return eval_not(filter, data)
    elif operator == 'and':
        return eval_and(filter, data)
    elif operator == 'or':
        return eval_or(filter, data)
    else:
        return 'not implemented'

def eval_equals(filter, data):
    field=filter.get('field')
    expectedValue=filter.get('value')
    actualValue=data.get(field)
    return expectedValue == actualValue

def eval_contains(filter, data):
    field=filter.get('field')
    expectedValue=filter.get('value')
    actualValue=data.get(field)
    
    if actualValue is None:
        return False
    else:
        return expectedValue in actualValue

def eval_in(filter, data):
    field=filter.get('field')
    values=filter.get('values')
    actualValue=data.get(field)
    for v in values:
       if v == actualValue:
           return True
    return False

def eval_not(filter, data):
    f=filter.get('filter')
    return not eval_filter(f, data)

def eval_and(filter, data):
    filters=filter.get('filters')
    for f in filters:
       if not eval_filter(f, data):
           return False
    return True
    
def eval_or(filter, data):
    filters=filter.get('filters')
    for f in filters:
       if eval_filter(f, data):
           return True
    return False
