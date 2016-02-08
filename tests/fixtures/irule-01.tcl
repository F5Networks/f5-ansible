when HTTP_REQUEST priority 100 {

    #######################################################################
    # PURPOSE:  Establish environment specific object variables
    #
    # This iRule has a priority of 100 and will therefore run before
    # any iRules with default priority of 500 (lower priority number runs first)
    #
    # This iRule sets the properties for (and must be present when using):
    #######################################################################
    
    ## Configure Pool names ##
    
    set SYSTEM_F_CONSOLIDATED_POOL  "dev-raw" 
    set SYSTEM_T_CONSOLIDATED_POOL  "dev-raw" 
    # No LEGACY pool configured in dev
    set LEGACY_POOL            ""  

    set SYSTEM_R_POOL   "dev-ule"
    set SKUNKWORKS_JETTY_POOL      "dev-skunk"
    


    
}
