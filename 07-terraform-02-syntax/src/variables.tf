# Заменить на ID своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_cloud_id" {
  default = "b1gh01mgrk9pekc59m0f"
}

# Заменить на Folder своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_folder_id" {
  default = "b1g5sdiiskl135r2jmcv"
}

# Заменить на ID своего образа
# ID можно узнать с помощью команды yc compute image list
variable "image_id" {
  default = "fd8q9honj0ga5pjdkk0u"
}

#
variable "OAUTH" {
  type = string
}