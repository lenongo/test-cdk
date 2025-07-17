from aws_cdk import Stack, Environment
from aws_cdk.pipelines import (
    CodePipeline, CodePipelineSource, ShellStep
)
from constructs import Construct
from my_app_stage import MyAppStage
import os

# 環境変数から取得、なければサンプル値を使用
DEFAULT_ACCOUNT = os.environ.get("CDK_DEFAULT_ACCOUNT", "123456789012")
DEFAULT_REGION = os.environ.get("CDK_DEFAULT_REGION", "ap-northeast-1")

DEV = Environment(account=DEFAULT_ACCOUNT, region="ap-northeast-1")
TEST = Environment(account=DEFAULT_ACCOUNT, region="us-east-1")

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # GitHubリポジトリ名とConnection ARNは環境変数から取得
        github_repo = os.environ.get("GITHUB_REPO", "your-username/your-repo")
        connection_arn = os.environ.get("CODECONNECTION_ARN", 
                                      f"arn:aws:codeconnections:{DEFAULT_REGION}:{DEFAULT_ACCOUNT}:connection/your-connection-id")

        pipeline = CodePipeline(
            self, "Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    github_repo,       # GitHub repo
                    "main",
                    connection_arn=connection_arn
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