# Lacework Webhook Filter
Lambda function for filtering webhook calls from Lacework. This tool is implemented as a Webhook running as a Lambda function and is helpful when you want more detailed filtering of alerts from Lacework using webhooks. The tool is using filters defined in a json format that gives rich options for configuration. See https://docs.lacework.com/onboarding/webhook for more information about the Lacework alert webhook support.

## Deployment Guide
Open your AWS console, navigate to the CloudFormation console and select Create Stack
![image](https://user-images.githubusercontent.com/8701191/213553699-f1836c81-b8b6-400d-8ba1-6472615ac0a4.png)
Add the following URL as the template and click Next:
https://bboe-lambda-code.s3.amazonaws.com/lacework-webhook-filter/LaceworkWebhookFilter.yaml

![image](https://user-images.githubusercontent.com/8701191/213804241-3c2b258c-fa78-4de0-91b9-e87be4b22fdd.png)
* The filter defines what calls to forward to the destination. The default filter will forward test alerts and specific compliance alerts. See below for more information about the filtering language used.
* The destination URL will be the location the webhook requests will be forwarded to.
* Username and password can be provided for endpoints that require basic authentication

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
## Notes For Integrating with Jira Cloud
This webhook can also be put in front of Jira cloud. These messages tend to look as follows:
```
{
  "fields": {
    "summary": "Event: 0 (20 Jan 2023 20:41 GMT) Test Event",
    "description": "This is a test Message.\n\n*Details*\n|Event Id|0|\n|Event Type|TestEvent|\n|Event Category|TestEvent|\n|Severity|0|\n|Start Time|20 Jan 2023 20:41 GMT|\n|Link|[Event Link | https://login.lacework.net]|\n|LW Account Name|ABC|\n\n\n",
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
```

Do the following to setup this integration:
* Setup an integration with Jira Server in the Lacework Dashboard.
* Add link to Lambda Webhook
* Configure Webhook to point to a URL that looks as follows: `https://<your-site>.atlassian.net/rest/api/2/issue/`
* Set username to the user creating the issue
* Set password to an API key generated at https://id.atlassian.com/manage-profile/security/api-tokens
* Configure a filter that can look as follows to let test messages through: `{"operator": "contains","field": "fields.summary","value": "Test Event"}`

## Notes for testing filters
Install a separate instance of the webhook, following the instructions above, but leave all default settings as default, including no destination URL.
<img width="1611" alt="image" src="https://user-images.githubusercontent.com/8701191/223752115-84df0baa-10d3-4d40-bc28-706111683234.png">

Open the Lambda function you just created.
<img width="1611" alt="image" src="https://user-images.githubusercontent.com/8701191/223752629-bbabee59-8c37-4aa3-aba7-dc21f4b4f1db.png">

Create a new test event.
<img width="1611" alt="image" src="https://user-images.githubusercontent.com/8701191/223752765-4d3c621f-ff1c-4b0a-a68a-f221e5c4b2a9.png">

Set the event JSON as follows:
```
{
  "body": {
    "event_title": "Test Event",
    "event_link": "https://login.lacework.net",
    "lacework_account": "MY_ACCOUNT",
    "event_source": "TestEventSource",
    "event_description": "This is a test Message.",
    "event_timestamp": "08 Mar 2023 00:04 GMT",
    "event_type": "TestEvent",
    "event_id": "0",
    "event_severity": "0"
  },
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}
```
<img width="1611" alt="image" src="https://user-images.githubusercontent.com/8701191/223753367-e17c85e9-ad23-4f30-8faa-9bc8a663868c.png">

Save the event and run test:
<img width="1611" alt="image" src="https://user-images.githubusercontent.com/8701191/223753810-e257643c-080e-4006-9042-4ca28baa5175.png">

In this case we simulated sending a payload using POST, looking as follows:
```
{
  "event_title": "Test Event",
  "event_link": "https://login.lacework.net",
  "lacework_account": "MY_ACCOUNT",
  "event_source": "TestEventSource",
  "event_description": "This is a test Message.",
  "event_timestamp": "08 Mar 2023 00:04 GMT",
  "event_type": "TestEvent",
  "event_id": "0",
  "event_severity": "0"
}
```

This payload was evaluated using the following default filter:
```
{
  "operator": "or",
  "filters": [
    {
      "operator": "equals",
      "field": "event_title",
      "value": "Test Event"
    },
    {
      "operator": "in",
      "field": "rec_id",
      "values": [
        "AWS_CIS_1_1",
        "AWS_CIS_1_16"
      ]
    }
  ]
}
```

This means the webhook would try to forward the message to a destination, which in this configureation is not specified. We'll therefore see the following output, which is a sign of a message passing the filter, but not forwarded:
```
[INFO]	2023-03-08T15:25:48.161Z	6040bc26-d023-47cf-b9a7-6bbb447ec187	Forward data using Webhook
[INFO]	2023-03-08T15:25:48.162Z	6040bc26-d023-47cf-b9a7-6bbb447ec187	Result: {'statusCode': 500, 'body': 'Can not connect to remote server '}
```

If we were to change the payload to the following:
```
{
  "body": {
    "event_title": "Failing event",
    "event_link": "https://login.lacework.net",
    "lacework_account": "MY_ACCOUNT",
    "event_source": "TestEventSource",
    "event_description": "This is a test Message.",
    "event_timestamp": "08 Mar 2023 00:04 GMT",
    "event_type": "TestEvent",
    "event_id": "0",
    "event_severity": "0"
  },
  "requestContext": {
    "http": {
      "method": "POST"
    }
  }
}
```

This would to pass the filter and we'll see the following in the output:
```
[INFO]	2023-03-08T15:27:48.313Z	55eaddd1-f643-46e9-8df5-c6ed047e7edb	Do not forward data
[INFO]	2023-03-08T15:27:48.313Z	55eaddd1-f643-46e9-8df5-c6ed047e7edb	Result: {'statusCode': 200, 'body': 'Message not forwarded'}
```

To change the filter, navigate to configuration and look at the environment variables:
<img width="1611" alt="image" src="https://user-images.githubusercontent.com/8701191/223756042-ebb4a160-1ba0-4a8e-84a7-cdd2b4b8b311.png">

The filter is configured as an environment variable and can easily be changed.

### Testing with Jira
Testing with Jira follows a very similar procedure, but with different filters and inputs.
    
A good starting point would be to configure the webhook to use the following filter:
```
{
  "operator": "contains",
  "field": "fields.summary",
  "value": "Test Event"
}
```

Then test the filter using the following payload:
```
{
  "body": {
    "fields": {
      "summary": "Event: 0 (20 Jan 2023 20:41 GMT) Test Event",
      "description": "This is a test Message.\n\n*Details*\n|Event Id|0|\n|Event Type|TestEvent|\n|Event Category|TestEvent|\n|Severity|0|\n|Start Time|20 Jan 2023 20:41 GMT|\n|Link|[Event Link | https://login.lacework.net]|\n|LW Account Name|ABC|\n\n\n",
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
}
```
