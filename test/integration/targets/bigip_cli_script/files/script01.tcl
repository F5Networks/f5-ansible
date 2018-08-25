proc script::run {} {
  set state [lindex $tmsh::argv 1]

  if { $state ne "disabled" && $state ne "enabled" } {
    puts "Requires one argument: \[enabled/disabled\] "
  } else {
    foreach {address} [tmsh::get_config /ltm virtual-address] {
      tmsh::modify /ltm virtual-address [tmsh::get_name $address] arp $state
      puts "ARP $state for virtual address [tmsh::get_name $address]"
    }
  }
}

proc script::help {} {
  tmsh::add_help "Enable/Disable ARP for all virtual addresses on this unit\n\ntoggle-virtual-address-arp \[enabled/disabled\]"
}

