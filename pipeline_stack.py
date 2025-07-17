from aws_cdk import Stack, Environment
from aws_cdk.pipelines import (
    CodePipeline, CodePipelineSource, ShellStep
)
from constructs import Construct
from my_app_stage import MyAppStage

DEV = Environment(account="357178285063", region="ap-northeast-1")
TEST = Environment(account="357178285063", region="us-east-1")

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(
            self, "Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    "lenongo/test-cdk",       # GitHub repo
                    "main",
                    connection_arn="arn:aws:codeconnections:ap-northeast-1:357178285063:connection/125c95dc-7a8a-4102-aa7e-a9934c65ac4f"
                ),
                commands=[
                    "npm install -g aws-cdk",   # CodeBuild 内で CDK CLI DL
                    "pip install -r requirements.txt",
                    "cdk synth"
                ],
            ),
        )

        pipeline.add_stage(MyAppStage(self, "Dev", "Dev", env=DEV))
        pipeline.add_stage(MyAppStage(self, "Test", "Test", env=TEST)) 