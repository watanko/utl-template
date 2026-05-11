variable "project_name" {
  description = "プロジェクト名。resource name と tag の prefix として使います。"
  type        = string
  default     = "utl-template"
}

variable "environment" {
  description = "環境名。local, staging, production などを指定します。"
  type        = string
  default     = "local"

  validation {
    condition     = contains(["local", "staging", "production"], var.environment)
    error_message = "environment は local, staging, production のいずれかを指定してください。"
  }
}
