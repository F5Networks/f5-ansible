when LB_SELECTED {
   # Capture IP address chosen by WIP load balancing
   set wipHost [LB::server addr]
}

when LB_FAILED {
   # Chose datagroup name based on LDNS IP
   set natDatagroup [class match -value [IP::client_addr] equals "/Common/LDNS_datagroup" ]
}