package s3

deny[msg] {
  input.ACL == "public-read"
  msg := "S3 bucket is public"
}
