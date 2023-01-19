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
