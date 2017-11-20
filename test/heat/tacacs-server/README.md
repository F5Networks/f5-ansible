Configuration
=============

To configure your BIG-IP to use this TACACS+ configuration, you will need to issue the
following `tmsh` commands. Note that you need to replace **IP_ADDRESS** with the IP address
of your TACACS+ server

```
tmsh create auth tacacs system-auth { debug enabled protocol ip service ppp secret f5networks servers add { IP_ADDRESS } }
tmsh modify auth source type tacacs

tmsh modify auth remote-user { default-role guest remote-console-access tmsh }

tmsh modify auth remote-role role-info add { adm { attribute F5-LTM-User-Info-1=adm console tmsh line-order 1 role administrator user-partition All } }
tmsh modify auth remote-role role-info add { appEd { attribute F5-LTM-User-Info-1=appEd console disabled line-order 2 role application-editor user-partition Common } }
tmsh modify auth remote-role role-info add { userMgr { attribute F5-LTM-User-Info-1=userMgr console disabled line-order 3 role user-manager user-partition Common } }
```

Usage
=====

With the above configured, you should be able to log in with administrator access using
the `f5user1` user; password `letmein`.
