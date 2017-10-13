Faking idempotency with bigip_command
=====================================

This Playbook provides an example of how one can turn the non-idempotent module
`bigip_command` into a slightly more idempotent module.

To accomplish this, we use some Task trickery related to storing output and then
checking that output. It requires more Tasks to accomplish what you want to do,
but it can also increase the chances of idempotent behavior while you want for
official idempotent modules to be released.

Note that this approach will not work if you specify many items in the `commands` list
which all need to be checked for idempotence.

The key bigip_command syntax that you need to apply this technique to are commands
that `create` or `delete` resources in BIG-IP. Commands that only `modify` resources
do not need to be checked for idempotence because there is not the same level of risk
as there is with `create` (duplicating resources) or `delete` (removing non-existing
resources).

The important point to take away in this example is the usage of the `when` conditional
in the second Task. By using `when`, we can tell specific future tasks to fire based
on the existing configuration we query from the device.
