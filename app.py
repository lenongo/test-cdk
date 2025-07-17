from aws_cdk import App, Environment
from pipeline_stack import PipelineStack

app = App()
PipelineStack(app, "CdkGhPipeline", env=Environment(
    account="357178285063", 
    region="ap-northeast-1"
))
app.synth() 