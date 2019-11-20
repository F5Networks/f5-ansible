when LB_SELECTED {
   # {{ inventory_hostname }}
   set wipHost [LB::server addr]
}

when LB_FAILED {
   set wipHost [LB::server addr]
}