import * as cdk from 'aws-cdk-lib';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codecommit from 'aws-cdk-lib/aws-codecommit';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

class MyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 1. Create a AWS code commit repository
    const codeCommitRepo = new codecommit.Repository(this, 'CodeCommitRepo', {
      repositoryName: 'my-repository',
    });

    // 2. Use the AWS code commit repository to attach to a AWS code pipeline. the AWS code commit repository will have the java project we previously built
    const pipeline = new codepipeline.Pipeline(this, 'CodePipeline', {
      stages: [
        {
          stageName: 'Source',
          actions: [
            new codepipeline.Actions.CodeCommitSourceAction({
              actionName: 'CodeCommit_Source',
              repository: codeCommitRepo,
              output: new codepipeline.Artifact('CodeCommitOutput'),
            }),
          ],
        },
        // 3. Use AWS code build as a part of code pipeline to build the project
        {
          stageName: 'Build',
          actions: [
            new codepipeline.Actions.CodeBuildAction({
              actionName: 'CodeBuild',
              project: new codebuild.PipelineProject(this, 'CodeBuildProject', {
                buildSpec: codebuild.BuildSpec.fromObject({
                  version: '0.2',
                  phases: {
                    build: {
                      commands: ['mvn package'],
                    },
                  },
                  artifacts: {
                    files: ['target/*.jar'],
                  },
                }),
              }),
              input: new codepipeline.Artifact('CodeCommitOutput'),
              outputs: [new codepipeline.Artifact('CodeBuildOutput')],
            }),
          ],
        },
      ],
    });

    // 4. Create a VPC
    const vpc = new ec2.Vpc(this, 'VPC', {
      cidr: '10.0.0.0/16',
    });

    // 5. Ensure that the VPC spans at least 2 availability zones
    vpc.addAvailabilityZone('us-east-1a');
    vpc.addAvailabilityZone('us-east-1b');

    // 6. Create a public subnet
    const publicSubnet = new ec2.Subnet(this, 'PublicSubnet', {
    vpcId: vpc.vpcId,
    cidrBlock: '10.0.1.0/24',
    availabilityZone: 'us-east-1a',
    mapPublicIpOnLaunch: true,
    });

    // 7. Create a private subnet
const privateSubnet = new ec2.Subnet(this, 'PrivateSubnet', {
  vpcId: vpc.vpcId,
  cidrBlock: '10.0.2.0/24',
  availabilityZone: 'us-east-1b',
});

// 8. Provision one ec2 instance and add the a bash user data script to install docker in it
const ec2Instance = new ec2.Instance(this, 'EC2Instance', {
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
  machineImage: new ec2.AmazonLinuxImage(),
  vpc: vpc,
  vpcSubnets: {
    subnetType: ec2.SubnetType.PRIVATE,
  },
  userData: ec2.UserData.forLinux({
    shebang: '#!/bin/bash',
    inline: [
      'apt-get update',
      'apt-get install -y docker',
    ],
  }),
});

// 9. Configure classic Elastic Load Balancer to route traffic to the EC2 instances
const lb = new elbv2.LoadBalancer(this, 'LoadBalancer', {
  vpc: vpc,
  internetFacing: true,
});
lb.addTarget(ec2Instance);

// 11. Create a docker file using a project from the repo and push it as an image to amazon ECR
const ecrRepo = new ecr.Repository(this, 'ECRRepo', {
  repositoryName: 'my-repo',
});

const taskDef = new ecs.FargateTaskDefinition(this, 'TaskDefinition', {
  memoryLimitMiB: 512,
  cpu: 256,
});
taskDef.addContainer('WebContainer', {
  image: ecs.ContainerImage.fromAsset('.'),
  memoryLimitMiB: 256,
  cpu: 128,
});

// 12. Download the docker image using from AWS ecr into AWS ec2 using the userdata boot script along with all previous values of bootstrapping and run the application
const service = new ecs.FargateService(this, 'ECSService', {
  cluster: new ecs.Cluster(this, 'ECSCluster', {
    vpc: vpc,
  }),
  taskDefinition: taskDef,
  assignPublicIp: true,
});
service.connections.allowFrom(ec2Instance, ec2.Port.tcp(80));
}
}
const app = new cdk.App();
new MyStack(app, 'MyStack');

