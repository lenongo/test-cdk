from aws_cdk import (
    Stage, Stack, aws_s3 as s3, aws_lambda as lambda_,
    Environment, RemovalPolicy, Duration
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
        
        # 🆕 Lambda関数を追加
        my_lambda = lambda_.Function(
            self,
            "MyPythonFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_inline("""
import json
import boto3
import os

def handler(event, context):
    '''
    CDKでデプロイしたPythonファイルの実行例
    '''
    
    # 環境変数から情報取得
    bucket_name = os.environ.get('BUCKET_NAME')
    env_name = os.environ.get('ENV_NAME')
    
    # S3クライアント作成
    s3 = boto3.client('s3')
    
    try:
        # S3バケットの操作例
        s3.put_object(
            Bucket=bucket_name,
            Key=f'lambda-execution-{env_name}.txt',
            Body=f'Hello from {env_name} Lambda! Executed at: {context.aws_request_id}'
        )
        
        # バケット内のオブジェクト一覧取得
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Python function executed successfully in {env_name}!',
                'bucket': bucket_name,
                'objects_in_bucket': objects,
                'execution_id': context.aws_request_id
            }, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error: {str(e)}',
                'env': env_name
            })
        }
"""),
            environment={
                'BUCKET_NAME': bucket.bucket_name,
                'ENV_NAME': env_name
            },
            timeout=Duration.seconds(60)
        )
        
        # LambdaにS3への読み書き権限を付与
        bucket.grant_read_write(my_lambda)

class MyAppStage(Stage):
    def __init__(self, scope: Construct, id: str, env_name: str, *, env: Environment):
        super().__init__(scope, id, env=env)
        # 環境名をStack IDに含めて一意性を確保
        MyAppStack(self, f"{env_name}AppStack", env_name=env_name, env=env) 