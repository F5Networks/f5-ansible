when RULE_INIT {
       set static::FormBaseURL "/sp-ofba-form"
       set static::FormReturnURL "/sp-ofba-completed"
       set static::HeadAuthReq "X-FORMS_BASED_AUTH_REQUIRED"
       set static::HeadAuthRet "X-FORMS_BASED_AUTH_RETURN_URL"
       set static::HeadAuthSize "X-FORMS_BASED_AUTH_DIALOG_SIZE"
       set static::HeadAuthSizeVal "800x600"
       set static::ckname "MRHSession_SP"
       set static::Basic_Realm_Text "SharePoint Authentication"
    }

    when HTTP_REQUEST {
       set apmsessionid [HTTP::cookie value MRHSession]
       set persist_cookie [HTTP::cookie value $static::ckname]
       set clientless_mode 0
       set form_mode 0
       # Identify User-Agents type
       if {[HTTP::header exists "X-FORMS_BASED_AUTH_ACCEPTED"] && (([HTTP::header "X-FORMS_BASED_AUTH_ACCEPTED"] equals "t") || ([HTTP::header "X-FORMS_BASED_AUTH_ACCEPTED"] equals "f"))} {
          set clientless_mode 0; set form_mode 1
       } else {
          switch -glob [string tolower [HTTP::header "User-Agent"]] {
             "*microsoft data access internet publishing provider*" -
             "*office protocol discovery*" -
             "*microsoft-webdav-miniredir*" -
             "*microsoft office*" -
             "*non-browser*" -
             "msoffice 12*" { set form_mode 1 }
             "*mozilla/4.0 (compatible; ms frontpage*" {
                if { [ string range [getfield [string tolower [HTTP::header "User-Agent"]] "MS FrontPage " 2] 0 1]  > 12 } {
                   set form_mode 1
                } else {
                   set clientless_mode 1
                }
             }
             "*mozilla*" -
             "*opera*" { set clientless_mode 0 }
             default { set clientless_mode 1
             }
          }
       }
       if { $clientless_mode || $form_mode } {
          if { [HTTP::cookie exists "MRHSession"] } {set apmstatus [ACCESS::session exists -state_allow $apmsessionid]} else {set apmstatus 0}
          if { !($apmstatus) && [HTTP::cookie exists $static::ckname] } {set apmpersiststatus [ACCESS::session exists -state_allow $persist_cookie]} else {set apmpersiststatus 0}
          if { ($apmpersiststatus) && !($apmstatus) } {
             # Add MRHSession cookie for non browser user-agent first request and persistent cookie present
             if { [catch {HTTP::cookie insert name "MRHSession" value $persist_cookie} ] } {log local0. "[IP::client_addr]:[TCP::client_port] : TCL error on HTTP cookie insert MRHSession : URL : [HTTP::host][HTTP::path] - Headers : [HTTP::request]"} else {return}
          }
       } else { return }
       if { $clientless_mode && !($apmstatus)} {
          if { !([HTTP::header Authorization] == "") } {
             set clientless(insert_mode) 1
             set clientless(username)    [ string tolower [HTTP::username] ]
             set clientless(password)    [HTTP::password]
             binary scan [md5 "$clientless(password)"] H* clientless(hash)
             set user_key "$clientless(username).$clientless(hash)"
             set clientless(cookie_list)             [ ACCESS::user getsid $user_key ]
             if { [ llength $clientless(cookie_list) ] != 0 } {
                set clientless(cookie) [ ACCESS::user getkey [ lindex $clientless(cookie_list) 0 ] ]
                if { $clientless(cookie) != "" } {
                   HTTP::cookie insert name MRHSession value $clientless(cookie)
                   set clientless(insert_mode) 0
                }
             }
             if { $clientless(insert_mode) } {
                HTTP::header insert "clientless-mode" 1
                HTTP::header insert "username" $clientless(username)
                HTTP::header insert "password" $clientless(password)
            }
            unset clientless
          } else {HTTP::header insert "clientless-mode" 1}
       } elseif {$form_mode && !($apmstatus) && !([HTTP::path] equals $static::FormBaseURL)}{
          HTTP::respond 403 -version "1.1" noserver \
             $static::HeadAuthReq "https://[HTTP::host]$static::FormBaseURL" \
             $static::HeadAuthRet "https://[HTTP::host]$static::FormReturnURL" \
             $static::HeadAuthSize $static::HeadAuthSizeVal \
             "Connection" "Close"
          return
       }
    }

    when HTTP_RESPONSE {
       # Insert persistent cookie for html content type and private session
       if { [HTTP::header "Content-Type" ] contains "text/html" } {
          HTTP::cookie remove $static::ckname
          HTTP::cookie insert name $static::ckname value $apmsessionid path "/"
          HTTP::cookie expires $static::ckname 300 relative
          HTTP::cookie secure $static::ckname enable
       }
       # Insert session cookie if session was recovered from persistent cookie
       if { ([info exists "apmpersiststatus"]) && ($apmpersiststatus) } {
             HTTP::cookie insert name MRHSession value $persist_cookie path "/"
             HTTP::cookie secure MRHSession enable
       }
    }

    when ACCESS_SESSION_STARTED {
       if {([info exists "clientless_mode"])} {
          ACCESS::session data set session.clientless $clientless_mode
       }
       if { [ info exists user_key ] } {
          ACCESS::session data set "session.user.uuid" $user_key
       }
    }

    when ACCESS_POLICY_COMPLETED {
       if { ([info exists "clientless_mode"]) && ($clientless_mode) && ([ACCESS::policy result] equals "deny") } {
          ACCESS::respond 401 noserver WWW-Authenticate "Basic realm=$static::Basic_Realm_Text" Connection close
          ACCESS::session remove
       }
    }

    when ACCESS_ACL_ALLOWED {
       switch -glob [string tolower [HTTP::path]] {
          "/sp-ofba-form" {
             ACCESS::respond 302 noserver Location "https://[HTTP::host]$static::FormReturnURL"
          }
          "/sp-ofba-completed" {
             ACCESS::respond 200 content {
                <html>
                   <head><title>Authenticated</title></head>
                   <body><b>Good Work, you are Authenticated</b></body>
                </html>
             } noserver
          }
          "*/signout.aspx" {
             # Disconnect session and redirect to APM logout Page
             ACCESS::respond 302 noserver Location "/vdesk/hangup.php3"
             return
          }
          "/_layouts/accessdenied.aspx" {
             # Disconnect session and redirect to APM Logon Page
             if {[string tolower [URI::query [HTTP::uri] loginasanotheruser]] equals "true" } {
                ACCESS::session remove
                ACCESS::respond 302 noserver Location "/"
                return
             }
          }
          default {
             # No Actions
          }
       }
    }