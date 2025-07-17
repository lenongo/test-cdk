from aws_cdk import (
    Stage, Stack, aws_s3 as s3, Environment, RemovalPolicy
)
from constructs import Construct

class MyAppStack(Stack):
    def __init__(self, scope: Construct, id: str, env_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # 環境名をバケット名に含めて一意性を確保
        bucket = s3.Bucket(
            self, 
            "SampleBucket",
            bucket_name=f"my-cdk-app-{env_name.lower()}-{self.account}",  # 環境名+アカウントIDで一意性確保
            removal_policy=RemovalPolicy.DESTROY,  # 学習目的なので削除可能
            auto_delete_objects=True
        )

class MyAppStage(Stage):
    def __init__(self, scope: Construct, id: str, env_name: str, *, env: Environment):
        super().__init__(scope, id, env=env)
        # 環境名をStack IDに含めて一意性を確保
        MyAppStack(self, f"{env_name}AppStack", env_name=env_name, env=env) 