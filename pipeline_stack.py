from aws_cdk import Stack, Environment
from aws_cdk.pipelines import (
    CodePipeline, CodePipelineSource, ShellStep
)
from constructs import Construct
from my_app_stage import MyAppStage

DEV = Environment(account="111111111111", region="ap-northeast-1")
TEST = Environment(account="222222222222", region="us-east-1")

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(
            self, "Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    "your-org/my-cdk-app",       # GitHub repo
                    "main",
                    connection_arn="arn:aws:codestar-connections:..."  # 1回 GUI で作成
                ),
                commands=[
                    "npm install -g aws-cdk",   # CodeBuild 内で CDK CLI DL
                    "pip install -r requirements.txt",
                    "cdk synth"
                ],
            ),
        )

        pipeline.add_stage(MyAppStage(self, "Dev",  env=DEV))
        pipeline.add_stage(MyAppStage(self, "Test", env=TEST)) 