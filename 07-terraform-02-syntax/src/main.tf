# Create vm01
resource "yandex_compute_instance" "vm01" {
  name                      = "vm01"
  zone                      = "ru-central1-b"
  hostname                  = "vm01.netology.cloud"
  allow_stopping_for_update = true

  resources {
    cores  = 2
    memory = 8
  }

  boot_disk {
    initialize_params {
      image_id = var.image_id
      name     = "vm01"
      type     = "network-ssd"
      size     = "50"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.default.id
    nat       = true
  }

  metadata = {
    ssh-keys = "cloud-user:${file("~/.ssh/id_rsa.pub")}"
  }
}
