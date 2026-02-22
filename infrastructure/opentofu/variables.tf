variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "doc-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "acr_name" {
  description = "Name of the container registry (must be globally unique)"
  type        = string
}

variable "aks_cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "doc-aks"
}

variable "aks_node_count" {
  description = "Number of nodes in the AKS cluster"
  type        = number
  default     = 1
}

variable "aks_node_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_E2s_v5"
}

