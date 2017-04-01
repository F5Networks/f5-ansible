
Deprecating parameters
----------------------

        2.0                           2.1                          2.2

+----------------------+    +-----------------------+    +------------------------+
|                      |    |                       |    |                        |
| Version to Deprecate |    |  Deprecated version   |    |  Final version         |
|                      |    |                       |    |                        |
|                      |    |                       |    |                        |
|  params:             |    |  params:              |    |  params:               |
|     change_me=dict() |    |    change_me=dict()   |    |    change_to=dict()    |
|                      |    |    change_to=dict()   |    |                        |
|                      |    |                       |    |                        |
|                      |    |  raise warnings about |    |  remove warnings about |
|                      |    |  usage of change_me   |    |  usage of change_me    |
|                      |    |                       |    |                        |
+----------------------+    +-----------------------+    +------------------------+
