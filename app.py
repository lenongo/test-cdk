from aws_cdk import App, Environment
from pipeline_stack import PipelineStack
import os

app = App()

# 環境変数から取得、なければサンプル値を使用
account = os.environ.get("CDK_DEFAULT_ACCOUNT", "123456789012")
region = os.environ.get("CDK_DEFAULT_REGION", "ap-northeast-1")

PipelineStack(app, "CdkGhPipeline", env=Environment(
    account=account, 
    region=region
))
app.synth() 