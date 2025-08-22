cidr_block           = "10.0.0.0/16"
public_subnet_cidr   = "10.0.1.0/24"
availability_zone    = "us-east-1a"
name                 = "ml-platform-vpc"
cluster_name         = "ml-platform-eks"
cluster_role_arn     = "arn:aws:iam::123456789012:role/EKSClusterRole"
subnet_ids           = ["subnet-0abcd1234efgh5678"]
