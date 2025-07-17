# CDK CI/CD パイプライン サンプルアプリケーション

## 🎯 アプリケーションの目的

このプロジェクトは、**AWS CDK**を使った**CI/CD パイプライン**の学習・理解を深めるための最小構成サンプルです。

### 主な学習目標

- **CDK Pipelines**を使った CI/CD 自動化の理解
- **マルチ環境デプロイ**（Dev ⇄ Test）の実装方法
- **GitHub 連携**による**GitOps**の実践
- **Infrastructure as Code**でのパイプライン管理

### 実現される機能

1. GitHub リポジトリにコードを push
2. AWS CodePipeline が自動実行
3. Dev 環境と Test 環境に同一コードを順次デプロイ
4. S3 バケットが各環境に作成される

---

## 📂 プロジェクト構成

```
my-cdk-app/
├── app.py               # CDK エントリーポイント
├── pipeline_stack.py    # CodePipeline 定義
├── my_app_stage.py      # デプロイ対象リソース（S3バケット）
├── requirements.txt     # Python依存関係
├── .gitignore          # Git除外設定（仮想環境等）
├── .venv/              # Python仮想環境（Git除外済み）
├── README.md           # このファイル
└── .github/
    └── workflows/
        └── cdk-ci.yml   # GitHub Actions ワークフロー（選択肢）
```

---

## 🚀 セットアップ手順

### 前提条件

- AWS CLI 設定済み
- Python 3.8 以上
- Node.js 18 以上
- Git

### 0. Python 仮想環境設定（重要）

CDK プロジェクトを開始する前に、Python の仮想環境を設定することを強く推奨します。これにより、プロジェクト固有の依存関係を分離し、システム全体の Python 環境を汚染することを防げます。

#### 0-1. 仮想環境作成

```bash
# プロジェクトディレクトリに移動
cd my-cdk-app

# Python仮想環境を作成
python -m venv .venv

# 【macOS/Linux】仮想環境を有効化
source .venv/bin/activate

# 【Windows】仮想環境を有効化
.venv\Scripts\activate
```

#### 0-2. 仮想環境有効化の確認

```bash
# コマンドプロンプトの先頭に(.venv)が表示されることを確認
(.venv) $ which python
# /your/path/my-cdk-app/.venv/bin/python

# pip も仮想環境のものが使われることを確認
(.venv) $ which pip
# /your/path/my-cdk-app/.venv/bin/pip
```

**⚠️ 重要**: 以降の全ての作業は、仮想環境を有効化した状態で実行してください。

#### 0-3. 依存関係のインストール

```bash
# 仮想環境が有効化されていることを確認してから実行
(.venv) $ pip install --upgrade pip
(.venv) $ pip install -r requirements.txt
```

### 1. リポジトリ設定

#### 1-1. GitHub リポジトリ作成

1. GitHub で新しいリポジトリを作成
2. このコードを push

**💡 ヒント**: `.gitignore`ファイルが自動作成されており、仮想環境ディレクトリ（`.venv/`）や CDK 一時ファイルが Git で追跡されないよう設定済みです。

#### 1-2. pipeline_stack.py の修正

```python
# pipeline_stack.py の19行目を実際のリポジトリ名に変更
input=CodePipelineSource.git_hub(
    "your-org/my-cdk-app",       # ← ここを変更
    "main",
    connection_arn="arn:aws:codestar-connections:..."
),
```

### 2. AWS アカウント準備

#### 2-1. アカウント ID の設定

```python
# 【初学者推奨】同一アカウント・異なるリージョン
DEV = Environment(account="123456789012", region="ap-northeast-1")    # 東京
TEST = Environment(account="123456789012", region="us-east-1")       # バージニア

# 【本番推奨】異なるアカウント
DEV = Environment(account="111111111111", region="ap-northeast-1")    # ← 実際のアカウントID
TEST = Environment(account="222222222222", region="us-east-1")       # ← 実際のアカウントID
```

**⚠️ 注意**: 同じアカウント・同じリージョンにすると、CloudFormation スタック名や S3 バケット名が衝突してエラーになります。

#### 2-2. CDK Bootstrap 実行

```bash
# Dev環境用
cdk bootstrap aws://[実際のアカウントID]/ap-northeast-1

# Test環境用（異なるアカウントの場合）
cdk bootstrap aws://[実際のアカウントID]/us-east-1
```

### 3. CodeStar Connections 設定

#### 3-1. GitHub 接続作成

**⚠️ 重要**: 2024 年 3 月より、「CodeStar Connections」は「**CodeConnections**」に名称変更されました。

参考 URL
https://docs.aws.amazon.com/ja_jp/dtconsole/latest/userguide/connections-create-github.html

**詳細手順**:

1. **AWS Console にログイン**し、検索バーで「**Developer Tools**」を検索

2. **Developer Tools Console** を開き、左側メニューで「**Settings**」→「**Connections**」を選択

3. 「**Create connection**」ボタンをクリック

4. **プロバイダー選択画面**で：

   - 「**GitHub**」を選択
   - 「**Connection name**」に接続名を入力（例：`my-github-connection`）

5. 「**Connect to GitHub**」ボタンをクリック

6. **GitHub 認証画面**が新しいタブで開くので：

   - 「**Authorize AWS Connector for GitHub**」ボタンをクリック
   - GitHub のユーザー名・パスワードでログイン（必要に応じて）

7. **GitHub Apps インストール画面**で：

   - 既存のインストールがある場合：リストから選択
   - 新規インストールの場合：「**Install a new app**」をクリック

8. **AWS Connector for GitHub のインストール**：

   - インストール先の GitHub アカウント/組織を選択
   - リポジトリアクセス権限を設定：
     - 「**All repositories**」（全リポジトリ）
     - 「**Only select repositories**」（特定リポジトリのみ）
   - 「**Install**」をクリック

9. **権限更新画面**（表示される場合）：

   - 「**Accept new permissions**」をクリック

10. **AWS Console に戻り**：

    - インストールが完了すると、Connection ID が表示される
    - 「**Connect**」ボタンをクリック

11. **作成完了**：
    - Connection ARN をコピーして保存
    - ステータスが「**Available**」になることを確認

#### 3-2. ARN の設定

`pipeline_stack.py`の 21 行目に実際の ARN を設定：

```python
connection_arn="arn:aws:codestar-connections:ap-northeast-1:123456789012:connection/abcdef12-3456-7890-abcd-ef1234567890"  # ← 実際のARN
```

### 4. 初回デプロイ

**⚠️ 前提**: 「0. Python 仮想環境設定」が完了していることを確認してください。

```bash
# 仮想環境が有効化されていることを確認
(.venv) $ python --version
# Python 3.8.x または以上が表示される

# CDK CLI インストール（未インストールの場合）
npm install -g aws-cdk

# CDK バージョン確認
cdk --version

# パイプライン デプロイ
(.venv) $ c
```

**💡 ヒント**:

- 初回デプロイには 5-10 分程度かかります
- デプロイ中に AWS リソースが作成される様子を AWS Console で確認できます

---

## 🔄 使用方法

### 通常の開発フロー

1. コードを修正
2. Git に commit & push
3. 自動的にパイプラインが実行される
4. Dev 環境 → Test 環境の順にデプロイ

### 確認方法

CDK デプロイ後は以下の手順で正常にリソースが作成されたことを確認できます。

#### 🎯 1. デプロイ完了の確認

**コマンドライン出力例**:

```bash
(.venv) $ cdk deploy CdkGhPipeline --require-approval never

✅  CdkGhPipeline

✨  Deployment time: 156.78s

Outputs:
CdkGhPipeline.PipelineName = CdkGhPipeline-Pipeline-AbCdEfGhIjKl
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:123456789012:stack/CdkGhPipeline/12345678-abcd-1234-abcd-123456789012

✨  Total time: 162.45s
```

**✅ デプロイ成功のサイン**:

- `✅ CdkGhPipeline` の表示
- `Outputs:` で Pipeline 名が表示される
- エラーメッセージが出ていない

#### 🔍 2. AWS Console での確認

##### 2-1. CodePipeline の確認

1. **AWS Console** にログインし、「**CodePipeline**」を検索
2. **パイプライン一覧**で `CdkGhPipeline-Pipeline-xxxxx` を確認
3. **パイプライン詳細画面**で：
   - **Status**: `Succeeded` または実行中の場合は各ステージの進行状況
   - **Source**: GitHub リポジトリからの取得状況
   - **Build**: CDK Synth（CloudFormation テンプレート生成）の実行状況
   - **UpdatePipeline**: パイプライン自体の更新状況
   - **Assets**: アセットファイルの発行状況
   - **DevStage**: Dev 環境へのデプロイ状況
   - **TestStage**: Test 環境へのデプロイ状況

**💡 ステージごとの詳細確認**:

- 各ステージをクリック → **Details** → **View in CodeBuild** でビルドログを確認

##### 2-2. CloudFormation スタックの確認

1. **AWS Console** で「**CloudFormation**」を検索
2. **スタック一覧**で以下を確認：
   ```
   ├── CdkGhPipeline                    # パイプライン本体
   ├── MyApp-Dev-DevAppStack            # Dev環境のアプリスタック
   └── MyApp-Test-TestAppStack          # Test環境のアプリスタック
   ```
3. 各スタックの **Status** が `CREATE_COMPLETE` または `UPDATE_COMPLETE` であることを確認

##### 2-3. S3 バケットの確認

1. **AWS Console** で「**S3**」を検索
2. **バケット一覧**で以下のバケットを確認：
   ```
   my-cdk-app-dev-123456789012     # Dev環境用バケット
   my-cdk-app-test-123456789012    # Test環境用バケット
   ```
3. 各バケットをクリックして詳細を確認：
   - **バケット名**: 環境名 + アカウント ID で一意性が確保されている
   - **リージョン**: 設定したリージョンに作成されている
   - **バケットポリシー**: 現在は設定なし（学習用の最小構成）

#### 🔧 3. AWS CLI での確認

```bash
# 現在のAWSアカウントID確認
aws sts get-caller-identity --query Account --output text

# CloudFormationスタック一覧
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query 'StackSummaries[?contains(StackName, `CdkGhPipeline`) || contains(StackName, `MyApp`)].{Name:StackName,Status:StackStatus}' --output table

# S3バケット一覧（my-cdk-appで始まるもの）
aws s3 ls | grep my-cdk-app

# 特定バケットの詳細確認
aws s3api get-bucket-location --bucket my-cdk-app-dev-123456789012
aws s3api get-bucket-versioning --bucket my-cdk-app-dev-123456789012
```

#### 🚨 4. トラブル時の確認ポイント

##### 4-1. パイプライン実行失敗の場合

**確認箇所**:

1. **CodePipeline Console** → 失敗したステージをクリック
2. **Details** → **View in CodeBuild** → **Build logs** タブ
3. エラーメッセージを確認

**よくあるエラー**:

```bash
# Bootstrap未実行
Error: Need to perform AWS CDK bootstrap

# 権限不足
Error: User: arn:aws:iam::123456789012:user/xxx is not authorized to perform: sts:AssumeRole

# Connection ARN 設定ミス
Error: CodeStar connection arn:aws:codestar-connections:... not found
```

##### 4-2. スタック作成失敗の場合

**確認箇所**:

1. **CloudFormation Console** → 失敗したスタック → **Events** タブ
2. **Status Reason** でエラー詳細を確認

**よくあるエラー**:

```bash
# リソース名重複
Resource with name [my-cdk-app-dev-123456789012] already exists

# 権限不足
Insufficient permissions to create resource
```

#### 📊 5. 動作確認のテスト

**基本動作テスト**:

```bash
# 1. S3バケットにファイルアップロード（テスト）
echo "Hello CDK!" > test.txt
aws s3 cp test.txt s3://my-cdk-app-dev-123456789012/

# 2. ファイルが正常にアップロードされたか確認
aws s3 ls s3://my-cdk-app-dev-123456789012/

# 3. ファイルダウンロード（確認）
aws s3 cp s3://my-cdk-app-dev-123456789012/test.txt downloaded-test.txt
cat downloaded-test.txt

# 4. テストファイル削除
rm test.txt downloaded-test.txt
aws s3 rm s3://my-cdk-app-dev-123456789012/test.txt
```

#### 🔄 6. 継続的な監視

**定期確認項目**:

- **CodePipeline**: 新しいコミット後の自動実行状況
- **CloudWatch**: リソースの使用状況とエラーログ
- **AWS Config**: コンプライアンス状況（本番環境の場合）

**コスト確認**:

```bash
# 現在の月間推定コスト確認
aws ce get-dimension-values --dimension SERVICE --time-period Start=2024-01-01,End=2024-01-31
```

---

## 🛠️ CI/CD 方式の選択

### パターン 1: CDK Pipelines（推奨）

- **使用ファイル**: `pipeline_stack.py`
- **特徴**: AWS 内でパイプライン完結、自己更新機能
- **適用**: 本番運用、マルチアカウント

### パターン 2: GitHub Actions

- **使用ファイル**: `.github/workflows/cdk-ci.yml`
- **特徴**: GitHub 内で完結、OIDC 認証
- **適用**: 簡単な検証、個人プロジェクト

#### GitHub Actions 使用時の追加設定

1. **OIDC プロバイダー作成**

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com
```

2. **IAM ロール作成**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:your-org/my-cdk-app:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

---

## 📖 学習ポイント

### CDK 概念の理解

- **App**: CDK アプリケーション全体
- **Stack**: CloudFormation スタック単位
- **Stage**: 環境単位（Dev, Test, Prod 等）
- **Construct**: 再利用可能なコンポーネント

### パイプライン概念

- **Source**: ソースコード取得（GitHub）
- **Build**: CDK Synth によるテンプレート生成
- **Deploy**: 各環境への順次デプロイ

---

## 🐛 トラブルシューティング

### よくあるエラー

#### 1. Python 仮想環境関連

```
Error: ModuleNotFoundError: No module named 'aws_cdk'
```

**原因**: 仮想環境が有効化されていない、または依存関係がインストールされていない

**解決**:

```bash
# 仮想環境を有効化
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate     # Windows

# 依存関係を再インストール
(.venv) $ pip install -r requirements.txt
```

#### 2. Bootstrap 未実行

```
Error: Need to perform AWS CDK bootstrap
```

**解決**: `cdk bootstrap`を実行

#### 3. 権限不足

```
Error: AccessDenied
```

**解決**: IAM ロールの権限を確認

#### 4. Connection ARN 未設定

```
Error: CodeStar connection not found
```

**解決**: CodeStar Connections で接続を作成

---

## 🎓 次のステップ

1. **リソース追加**: `my_app_stage.py`に Lambda、DynamoDB などを追加
2. **テスト追加**: パイプラインにユニットテスト、統合テストを組み込み
3. **セキュリティ強化**: IAM ロールの最小権限設定
4. **監視追加**: CloudWatch、X-Ray による可観測性向上
5. **本番運用**: Prod 環境の追加、承認プロセスの組み込み

---

## 📚 参考リンク

- [AWS CDK Developer Guide](https://docs.aws.amazon.com/cdk/v2/guide/)
- [CDK Pipelines Documentation](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/README.html)
- [CodeStar Connections](https://docs.aws.amazon.com/codepipeline/latest/userguide/connections.html)
- [GitHub OIDC 設定](https://docs.github.com/ja/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
