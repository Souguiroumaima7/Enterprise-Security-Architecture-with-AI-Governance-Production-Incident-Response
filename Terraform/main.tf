module "vpc" { source = "./modules/vpc" project = var.project_name }
module "eks" { source = "./modules/eks" vpc_id = module.vpc.vpc_id subnet_ids = module.vpc.private_subnets }
module "iam" { source = "./modules/iam" }


resource "random_id" "suffix" { byte_length = 3 }


resource "aws_s3_bucket" "model_artifacts" {
bucket = "${var.project_name}-model-artifacts-${random_id.suffix.hex}"
acl = "private"
server_side_encryption_configuration {
rule { apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" kms_master_key_id = aws_kms_key.model_key.arn } }
}
}


resource "aws_kms_key" "model_key" { description = "KMS key for model artifacts" }