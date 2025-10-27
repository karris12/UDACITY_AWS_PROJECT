provider "aws" {
  region = "us-west-2"
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb"

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  # --- Aurora configuration from Stack 1 ---
  aurora_arn                 = "arn:aws:rds:us-west-2:635949072774:cluster:my-aurora-serverless"
  aurora_db_name             = "myapp"
  aurora_endpoint            = "my-aurora-serverless.cluster-cma45dxths2o.us-west-2.rds.amazonaws.com"
  aurora_table_name          = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field   = "id"
  aurora_metadata_field      = "metadata"
  aurora_text_field          = "chunks"
  aurora_verctor_field       = "embedding"
  aurora_username            = "dbadmin"
  aurora_secret_arn          = "arn:aws:secretsmanager:us-west-2:635949072774:secret:my-aurora-serverless-f4WIPG"

  # --- S3 configuration from Stack 1 ---
  s3_bucket_arn              = "arn:aws:s3:::bedrock-kb-635949072774"
}
