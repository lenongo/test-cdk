from aws_cdk import App
from pipeline_stack import PipelineStack

app = App()
PipelineStack(app, "CdkGhPipeline")
app.synth() 