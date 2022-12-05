# Welcome to the CDK implementation of FA-RID

This is a project hosting the service code for FA-RID.

## Database schema

### Database choice

Will be using dynamoDB as the database of choice. It is serverless, so maintenance overhead. It scales with the service and can service requests as required and cost will be pay per request model.

### Tables

* `${appName}-subscriber-application-table-${stage}` - example: `fa-rid-subscriber-application-table-dev`
   * Description: This table will host the application profiles of subscribers.
   * primaryKey: `appName` | `^[A-Za-z][A-Za-z0-9_-]{4,29}$`
   * attributes

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
