proc validateCerFromFile {} {
    set hsl [HSL::open -proto TCP -pool JSA-MONITOR]
    if { [DIAMETER::command] == 257 && [DIAMETER::is_request]} {
        set originhost [DIAMETER::avp data get 264]
        if {$originhost ne ""} {
            set value [class lookup $originhost realm-list]
        }
        if {$value == ""} {
            call Diameter-procDropMessage::dropMessage 5008
            return
        }

        #Origin-Realm
        set value1 ""
        #Vendor-Id
        set value2 ""
        #Product-Name
        set value3 ""
        #First IP-Address
        set value4 ""
        #Second IP-Address if exists
        set value5 ""
        set ip1 ""
        set ip2 ""

        scan $value {%[^,],%[^,],%[^,],%[^,],%s} value1 value2 value3 value4 value5


        if { [DIAMETER::avp count 257] > 0 } {
            set data [DIAMETER::avp data get 257]
            binary scan $data S family
            log local0. "$family"
            switch $family {
                1 {
                    # ipv4 should contains 4 bytes
                    set ip1 [IP::addr parse -ipv4 $data 2]
                    log local0. "ip1 = $ip1"
                }
                2 {
                    # ipv6 should contains 16 bytes
                    set ip1 [IP::addr parse -ipv6 $data 2]
                    log local0. "ip1 = $ip1"
                }
                default {
                    log local0.alert "address family $family is not supported"
                }
            }
        }
        if { [DIAMETER::avp count 257] == 2 } {
            #Delete the first Host-IP-Address for Multi-Homing
            DIAMETER::avp delete 257
            set data [DIAMETER::avp data get 257]
            binary scan $data S family
            switch $family {
                1 {
                    # ipv4 should contains 4 bytes
                    set ip2 [IP::addr parse -ipv4 $data 2]
                    log local0. "ip2 = $ip2"
                }
                2 {
                    # ipv6 should contains 16 bytes
                    set ip2 [IP::addr parse -ipv6 $data 2]
                    log local0. "ip2 = $ip2"
                }
                default {
                    log local0.alert "address family $family is not supported"
                }
            }
        }

        #"slrf01001-fep3_fep-out" := "traffixsystems.com,27611,F5 Traffix Systems Control Plane Function,10.2.37.48,10.2.46.48" ,
        #log local0. "$value1 $value2 $value3 $value4 $value5"

        set productname [DIAMETER::avp data get 269]
        set origrealm [DIAMETER::realm origin]
        set vendorid [DIAMETER::avp data get 266 integer32]
        HSL::send $hsl "[IP::client_addr] [DIAMETER::command] HSL is working"
        #ISTATS::incr "ltm.virtual /Common/Diameter_iAPP.app/Diameter_iAPP_vs C $originhost" 1

        if {$productname equals $value3} {
            log local0. "CER - productname ok!!!"
        }

        if {$origrealm equals $value1} {
            log local0. "CER - originrealm ok!!!"
        }

        if {$vendorid == $value2} {
            log local0. "CER - vendorid ok!!!"
        }

        if {$ip1 == $value4} {
            log local0. "CER - ipaddr1 is ok!!!"
        }
        if {$ip2 ne ""} {
            if {$ip2 == $value5} {
                log local0. "CER - ipaddr2 is ok!!!"
            }
        }
    }
}
when DIAMETER_INGRESS {

    call validateCerFromFile
}
