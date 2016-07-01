# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_VERSION = "2"

INSTALL_SCRIPT = "vagrant_data/install.sh"

Vagrant.require_version ">= 1.8.4"

Vagrant.configure(VAGRANT_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.synced_folder ".", "/home/vagrant/get_a_room"
  config.vm.provision :shell, path: INSTALL_SCRIPT
  
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provider :virtualbox do |virtualbox|
    virtualbox.customize [
      'modifyvm', :id,
      '--memory', 512,
      '--cpus', 1
    ]
  end
end
