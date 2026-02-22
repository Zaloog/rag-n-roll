# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.aks_cluster_name}-dns"

  default_node_pool {
    name                        = "default"
    node_count                  = var.aks_node_count
    vm_size                     = var.aks_node_size
    temporary_name_for_rotation = "temp"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Development"
    Project     = "DocAssist"
  }
}

# Attach ACR to AKS (allows AKS to pull images)
resource "azurerm_role_assignment" "aks_acr" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}
