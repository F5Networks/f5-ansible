# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = 2

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.boot_timeout = 3600

  config.vm.define "big-ip01.internal" do |v|
    v.vm.box = "#{ENV['BOX_URL']}"

    # BIG-IP cannot mount shares in Virtualbox because Guest-Additions
    # cannot be installed on it.
    config.vm.synced_folder ".", "/vagrant", disabled: true
    v.vm.network :forwarded_port, guest: 443, host: 10443

    v.vm.network :private_network, ip: "10.2.2.2", auto_config: false
    v.vm.network :private_network, ip: "10.2.3.2", auto_config: false

    v.vm.provider :virtualbox do |p|
      p.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      p.customize ["modifyvm", :id, "--memory", 4096]
      p.customize ["modifyvm", :id, "--cpus", 2]
      p.customize ["modifyvm", :id, "--name", "big-ip01.internal"]

      # NICs need to be virtio because BIG-IP doesn't have drivers for
      # the others
      p.customize ["modifyvm", :id, "--nic1", "nat"]
      p.customize ["modifyvm", :id, "--nictype1", "virtio"]
      p.customize ["modifyvm", :id, "--nic2", "hostonly"]
      p.customize ["modifyvm", :id, "--nictype2", "virtio"]
      p.customize ["modifyvm", :id, "--nic3", "hostonly"]
      p.customize ["modifyvm", :id, "--nictype3", "virtio"]
    end

    v.vm.provision "shell", inline: <<-SHELL
      while true; do
          string=`tmsh show sys failover`
          if [[ $string == *"active"* ]]
          then
              break
          else
              echo "Runlevel is 'unknown' - waiting for 10s"
              sleep 10
          fi
      done
      echo "Runlevel is now valid, kicking off provisioning..."
    SHELL

    v.vm.provision "shell", inline: <<-SHELL
      tmsh load /sys config default
      tmsh modify sys dns name-servers replace-all-with { 10.0.254.254 }
      tmsh modify sys db setup.run value false
      tmsh create net vlan net1 interfaces add { 1.1 }
      tmsh create net self net1 address 10.2.2.2/255.255.255.0 vlan net1
      tmsh create net vlan net2 interfaces add { 1.2 }
      tmsh create net self net2 address 10.2.3.2/255.255.255.0 vlan net2
      tmsh save sys config
      sleep 10
      /usr/local/bin/SOAPLicenseClient --basekey  #{ENV['BIGIP_LICENSE']}
    SHELL
  end
end
