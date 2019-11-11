Fake idempotency with bigip_command
===================================

This playbook provides an example of how you can turn the non-idempotent module
`bigip_command` into a slightly more idempotent module.

To accomplish this, we use some task trickery related to storing output and then
checking that output. It requires more tasks to accomplish what you want to do,
but it can also increase the chances of idempotent behavior while you wait for
official idempotent modules to be released.

Note that this approach will not work if, in the `commands` list, you specify many items
that all need to be checked for idempotence.

The key bigip_command syntax that you need to apply this technique to are commands
that `create` or `delete` resources in BIG-IP. Commands that only `modify` resources
do not need to be checked for idempotence because there is not the same level of risk
as there is with `create` (duplicating resources) or `delete` (removing non-existing
resources).

The important point to take away in this example is the usage of the `when` conditional
in the second task. By using `when`, you can tell specific future tasks to fire based
on the existing configuration you query from the device.
