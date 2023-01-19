# Lacework Webhook Filter
Lambda function for filtering webhook calls from Lacework. This tool is implemented as a Webhook running as a Lambda function and is helpful when you want more detailed filtering of alerts from Lacework using webhooks. The tool is using filters defined in a json format that gives rich options for configuration. See https://docs.lacework.com/onboarding/webhook for more information about the Lacework alert webhook support.
## Deployment Guide
Open your AWS console, navigate to the CloudFormation console and select Create Stack
![image](https://user-images.githubusercontent.com/8701191/213553699-f1836c81-b8b6-400d-8ba1-6472615ac0a4.png)
Add the following URL as the template and click Next:
https://bboe-lambda-code.s3.amazonaws.com/lacework-webhook-filter/LaceworkWebhookFilter.yaml

![image](https://user-images.githubusercontent.com/8701191/213554605-6c7e56ad-12d6-41e6-8c1a-9d07bc4963d5.png)
* The destination URL will be the location the webhook requests will be forwarded to.
* The filter defines what calls to forward to the destination. The default filter will forward test alerts and specific compliance alerts. See below for more information about the filtering language used.

Click Next until the Webhook has been deployed.

Look up the Webhook in the Lambda UI and copy the function URL.
<img width="1840" alt="image" src="https://user-images.githubusercontent.com/8701191/213567305-ba3ff311-14be-4d4e-b5b9-2ec234fc0bd9.png">

Create a new alert channel in the Lacework UI and add the URL to the function.
<img width="764" alt="image" src="https://user-images.githubusercontent.com/8701191/213567942-661d2fc8-44b4-45da-b059-7e0b8ce11e23.png">

Click test in the Lacework UI to send a test message.
## Webhook Filtering Language
The webhook supports a number of filtering operators and the operators can be chained more complicated use cases. Given the following use case from https://docs.lacework.com/onboarding/webhook, you can do a number of different kinds of filters:
```
{
    "event_title": "Compliance Changed",
    "event_link": "https://myLacework.lacework.net/ui/investigate/Event/120884?startTime=1565370000000&endTime=1565373600000",
    "lacework_account": "myLacework",
    "event_source": "AzureCompliance",
    "event_description":"Azure Account myLacework Pay-As-You-Go: Azure_CIS_2_1 Ensure that standard pricing tier is selected changed from compliant to non-compliant",
    "event_timestamp":"27 May 2021 17:00 GMT",
    "event_type": "Compliance",
    "event_id": "120884",
    "event_severity": "4",
    "rec_id": "Azure_CIS_2_1"
    }
```
### Equals
`event_severity` equals 4:
```
{
  "operator": "equals",
  "field": "event_severity",
  "value": "4"
}
```
### Contains
`event_title` includes the string "Changed":
```
{
  "operator": "contains",
  "field": "event_title",
  "value": "Changed"
}
```
### Not
`rec_id` not equals "Azure_CIS_2_1":
```
{
  "operator": "not",
  "filter": {
    "operator": "equals",
    "field": "rec_id",
    "value": "Azure_CIS_2_1"
  }
}
```
### In
`rec_id` contains one of the following values: "Azure_CIS_2_1" or "Azure_CIS_2_2":
```
{
  "operator": "in",
  "field": "rec_id",
  "values": ["Azure_CIS_2_1", "Azure_CIS_2_2"]
}
```
### And
`event_source` equals "AzureCompliance" and `event_severity` equals "4":
```
{
  "operator": "and",
  "filters": [{
    "operator": "equals",
    "field": "event_source",
    "value": "AzureCompliance"
  },
  {
    "operator": "equals",
    "field": "event_severity",
    "value": "4"
  }]
}
```
### Or
`event_title` equals "Test Event" or `rec_id` equals "AWS_CIS_1_1" or "AWS_CIS_1_16":
```
{
  "operator": "or",
  "filters": [{
    "operator": "equals",
    "field": "event_title",
    "value": "Test Event"
  },
  {
    "operator": "in",
    "field": "rec_id",
    "values": ["AWS_CIS_1_1", "AWS_CIS_1_16"]
  }]
}
```
