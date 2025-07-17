from aws_cdk import (
    Stage, Stack, aws_s3 as s3, Environment
)
from constructs import Construct

class MyAppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        s3.Bucket(self, "SampleBucket")

class MyAppStage(Stage):
    def __init__(self, scope: Construct, id: str, *, env: Environment):
        super().__init__(scope, id, env=env)
        MyAppStack(self, "AppStack", env=env) 