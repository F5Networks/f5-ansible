when HTTP_REQUEST priority 500 {

    switch -glob [string tolower [HTTP::uri]] {
    
        "/b2b/connexion/service/v1*" {
            HTTP::uri "/backend/prx/connexion"
            pool $SYSTEM_F_CONSOLIDATED_POOL
        }
        
        "/b2b/mngr/service/v1*" {
            HTTP::uri "/backend/prx/mngr"
            pool $SYSTEM_F_CONSOLIDATED_POOL
        }
                
        "/sbus/proxy_services/laboratory_noise_proxy_service*" {
            HTTP::uri "/backend/prx/noise"
            pool $SYSTEM_F_CONSOLIDATED_POOL
        }
        
        "/prevaricate*" {		
            HTTP::uri "/backend/prx/prevaricate"
            pool $SYSTEM_F_CONSOLIDATED_POOL
        }
        
        "/backend/prx/system_f/web*" -
        "/backend/also*" -
        "/backend/prx/mngr*" -
        "/backend/prx/connexion*" -
        "/backend/prx/prevaricate*" -
        "/backend/prx/noise*" -
        "/backend/rest2*" {
            pool $SYSTEM_F_CONSOLIDATED_POOL 
        }
            
        
        "/mule-engine/services*" {
            pool $SYSTEM_R_POOL 
        }
        
        default { 
            if {[catch {pool $LEGACY_POOL}]}{
                log local0. "LEGACY_POOL is not configured for this environment. Discarding [HTTP::uri] request."
                discard
            }
        }
    }
}
