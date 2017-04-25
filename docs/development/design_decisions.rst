Code Conventions
================

The following is a document that describes some of the design decisions that
went into the F5 Ansible modules and why they were made. This document is
intended to address any contributor, or customer, questions on why I did
what I did and the known limitations for this design.

SSH is not used. REST is
------------------------

This is a question that comes up rather frequently.

  Why don't the modules use ssh?

After all, the "other" networking modules use SSH for their communication
with their remote devices.

This is a complicated question to answer because there are __many__ reasons
why this was decided upon. I will try to explain all of those reasons below.

TMSH is not an API
^^^^^^^^^^^^^^^^^^

At F5, regardless of what you might here or read online, `tmsh` is not considered
to be a formal API.

Now, there are some people who will try to argue about this and justify their
argument by saying that, "well, tmsh is a publicly available way to interact
with the BIG-IP, therefore it is implicitly an API".

While `tmsh` is indeed a publicly available way to interact with the BIG-IP,
it is not considered by anyone at F5 to be an API. You will notice, compared
to other APIs that are formal, that it has none of the features of "real"
APIs.

In addition to missing many features of "normal" APIs, it also is not guaranteed
to be consistent across versions of BIG-IP.

You should not rely on `tmsh` for anything except in cases where you have no other
choice. And in those cases, you must handle the versioning of it yourself.

The company had decided to put all their effort into REST
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the REST pattern of API development became popular, F5 put some work into
making a REST wrapper around `tmsh`. That is what you have today; a wrapper around
calls to `tmsh`.

To understand why the REST API is where the company has put more effort, you need
to understand the history of the SOAP API at F5.

It is surprisingly difficult for a team to develop for the SOAP API. The REST API
is easier to code for. Additionally, the REST APIs curiously map almost directly
to the `tmsh` command you would use. Coincidence? Hardly. Remember, it's `tmsh`.

There is still new functionality being added to SOAP, but most of the engineers at
F5 are focused on providing REST functionality.

* It's natively built into most all programming languages
* It's more easily supported in our future javascript-based iAppLX effort
* It's pretty close to native `tmsh`

SSH on BIG-IP can cause auth errors when under heavy load
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For better or worse, while SSH is about as native today as telnet was in the
past, it actually takes a fair amount of resources to establish an SSH connection
to a remote device.

You see this in Ansible today with their use of `ControlMaster` and `pipelining`.
Ansible saw that just the act of repeatedly connecting to the remote device over
SSH caused a significant amount of lag.

A real-life example, a customer had been using modules (that they had developed)
that used SSH under the hood to connecto the BIG-IP and were seeing "F5 Authorization
Required" 95% of the time. With SOAP this dropped to 4% and with REST this dropped to 1%.

When we investigated things further, we noticed that when the BIG-IP was under
load, the normal behavior of Ansible, namely this,

.. code-block:: bash

   sshpass -d57 ssh -C -o ControlMaster=auto -o ControlPersist=60s
   -o StrictHostKeyChecking=no -o User=ansible -o ConnectTimeout=10 -o
   ControlPath=/tmp/ansible_tower_JR8zTS/cp/ansible-ssh-%h-%p-%r -tt
   10.192.73.218 'tmsh delete sys connection'

When set in an infinite loop would cause failures rather consistently.

Diagnosis? The act of SSH'ing to frequently to BIG-IP causes intermittent authentication
failures. Solution? Don't use SSH because it's resource-intensive "enough" to be
unreliable for things that need to be reliable.

Now, this creates an issue. By giving up SSH, you also implicitly give up on SSH
certificate based access. Many customers made a stink about this. Well, on one hand
their frustration is justified. On the other hand though, it would be a herculean
amount of work to support SSH.

First, because of the above problem, but also because,

* You don't always have root shell access to your box. The cloud versions of BIG-IP
  come with "Appliance mode" turned on which puts you directly into `tmsh`
* `tmsh` has no structured output format like JSON. There's no consistent way to
  parse `tmsh` output. This means we would have to commit serious amounts of code
  to, ultimately, poorly parsing free-form text output. This would impact how long
  it took us to bring new modules to market and how reliably we could do that.
* The `tmsh` commands and output changes across nearly all versions of BIG-IP
* There is no SDK to consistently interact with `tmsh`

REST is, frankly, easy to code for
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This constraint is relevant to the developers who actually code these modules. For
the first iteration of the modules, what I refer to 1st-gen, the modules were written
by primarily two people who were not F5 employees.

For the 2nd-gen modules, they were all written by one guy; me, an F5 employee. This was
when F5 began put more skin in the Ansible game.

For the 3rd-gen modules, they were written primarily by myself and one other F5 employee.
Then, they were tested and promoted by several other F5 employees.

The reason that I bring these points up is to emphasize just how __few__ people are
actually working on the modules that you are using.

There is no "Ansible team" at F5. Due to my limited resources, I placed a priority on
ease-of-development and testing. I needed to churn reliable product out at a rather
fast pace compared to the pace that all other F5 products are released. My timeline
was weeks, not bi-yearly like BIG-IP releases.

SOAP has different APIs for every configuration point. Literally. If you need to set
the description of a Virtual Server, you need to use the `set_description`_ API, but
if you need to set a `destination` of the same Virtual Server you need to use the
`set_destination_v2`_ API. It's `v2` because there is also a `set_destination`_ API
that must be used for anything before version 11 of BIG-IP.

This is kinda frustrating from a developer point of view because you need to know
all these different APIs.

It's frustrating from the admin's point of view because each API is another round-trip
to the BIG-IP. Each time we need to talk to BIG-IP it means a slow-down and a chance
that a failure could happen.

This can be worked around through the use of Transactions in SOAP, but that just _another_
thing that the users of the API need to be aware of when writing any sort of integrations
with BIG-IP.

REST configures based on a "resource" so many APIs are implicitly transactional without
needing to use transactions. Additionally, these resources mean that you only need to
refer to __one__ API when changing most things about a particular object in BIG-IP.

For example, using our virtual server example above, instead of 2 or more APIs, there
is only one; `/mgmt/tm/ltm/virtual`. Sending a `GET` request to the resource returns
a single JSON payload where you can change the `description` or `destination` as needed
and then send a `PATCH` back to the BIG-IP with those changed values.

Also, it works like this across __all__ of the resources in BIG-IP. Which means once
you have learned how to use one resource, you've essentially learned how to use all
of them.

.. note::

   It should be noted that due to bugs in the REST API this is not __always__ true,
   but it is true enough that you can consider it "the way things are" and handle
   the edge cases as you encounter them. Indeed, we handle just such edge cases
   for you in the f5-sdk so that you don't need to care. That is one of the many
   reasons to use the SDK; we iron out the inconsistencies in the API.

From a developer point-of-view, this requirement to learn a convention instead of
learning a library of API calls means that new developers can be onboarded more
quickly and existing developers can more easily add new functionality and support
existing functionality.

From an admin point of view, this means that we need to make fewer round-trips to
your BIG-IP and this should therefore speed up the operations that we do perform
on the BIG-IP.

The F5 Python SDK is built on REST
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The tool underlying all future Ansible F5 module development is the F5 Python SDK.

First, some history of this SDK.

F5 is notorious for writing half-baked "SDKs". These "SDKs" always have the following
things in common.

- Written by one engineer
- The "SDK" covers Pools, Virtuals, and pool members
- The engineer has left the company
- No resources were ever dedicated to the "SDK"

I didnt want this to be the same story with the Python SDK that had been developed
by the OpenStack team. Since the OpenStack integration was a project at F5 that had
real resources dedicated to it, and the OpenStack integration relied implicitly on
the Python SDK, it was safe-enough to consider the Python SDK "supported".

I wanted to further re-enforce the need to keep this SDK alive though, so I chose
to build all the Ansible modules to use it. My hope was that if one project (OpenStack)
had resources dedicated to it, then maybe I could get a second major project (Ansible)
to also get resources dedicated to it to give the SDK a greater chance of surviving.

I also wanted to focus developer effort and expertise instead of fragmenting it
unnecessarily. My goal was that more engineers contributing to this SDK would negate
the need for fragmenting this development effort and that we would ultimately be building
everything off of this one SDK and dog-fooding it appropriately.

REST was also chosen because native ability to speak "REST via HTTP" is built into
all programming languages these days. We were using Python in this case, but it is
not much of a leap to expand this same functionality to Ruby or Go or JavaScript or
any language you may be interested in. All of them have native support for speaking
HTTP.

Another reason to use this REST SDK is that it is easy to debug JSON payloads with
common toolchains. For instance, working with Chrome developer tools, Postman, or
other REST clients is simple. SOAP envelopes are more difficult to humanly consume
as they are usually in an XML formatted payload and it's not readily obvious what
tools one would use to send payloads like this back and forth to a BIG-IP.

Finally, the Python packages `suds` and `bigsuds` are not Python 3 compatible, and
(at least in `bigsuds` case) supported or used by anyone at F5. There was no demand
for building an SDK that supported an API that only a minority of colleagues was
using at F5 or in the community.

Other F5 products made REST a first-class citizen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BIG-IP is not F5's only product. BIG-IQ and iWorkflow are two other products that we
make. Both of these products natively use REST API communication for __all__ of their
functionality.

Indeed, if you use a network inspector like those built-into Chrome or Firefox, you
can see the actual APIs these F5 products communicate with and the payloads that they
use.

Ok, fine, but "these products ship on something that has SSH access" you might say.
That's true, but in the future they won't. Teams developing these products are rapidly
turning them into standalone applications; what we refer to as "TMOS independence".

So in the future they will __not__ have CLI's other than whatever is provided by the
operating system that hosts them.

Also, each of these products provides functionality that allows they to proxy requests
directly to the BIG-IPs that they manage. We refer to this as "REST Proxy". That these
tools provide such native support is testament to how REST is considered to be a first-class
citizen for configuring our devices.

Other vendor APIs are always REST-like
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you look at the API landscape, nearly every vendor API is REST-like. It's becoming
increasingly uncommon to see SOAP APIs because, compared to JSON-over-HTTP using HTTP
verbs, SOAP is just a little too heavy-handed.

Most applications can represent their data structures just fine using JSON. Its largely
unnecessary to provide anything bigger than just a JSON payload. Languages can natively
transform scalars, lists, and dictionaries to the data structures native to the language.

Indeed, even in a complicated system like BIG-IP, all of our data structures can be
represented by a JSON payload.

To make the adoption of our APIs easier for those admining our box and integrating with
it, it was important to use technology that was already familiar to them.

Since customers are already largely exposed to REST-like APIs from their dealings with
other vendors, it was natural to make use of the REST API instead of some other format,
or, direct SSH communication.

The people working on this codebase work with REST and the SDK every day
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The F5 OpenStack team began the trend of SDK development with their work on our Openstack
integration. This progressed to include my adopting their work in Ansible. Today, the
people who are working on Ansible modules are the same developers who were initially
working on the F5 Python SDK.

Furthermore, we are introducing more teams at F5 to the Python SDK so that they too may
integrate it into their testing procedures.

So as you can see, the majority of the new work being done at F5 is being done by people
who are familiar with REST.

There is a sizable amount of pre-existing work in test harnesses and other stuff at F5
that is based on SSH, but the experts that were involved in writing that have since
left the company and no expertise exists to further develop it; nor do those teams want
to put further development into it.

With this increasing body of knowledge around our REST API, it makes less sense to
attempt to support SSH.

The Ansible persistent network connection was not mature at the time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Persistent network device connections was released in Ansible 2.3. A __significant__
amount of work on the modules however, had already been done prior to this release.

To expect that one guy (Tim) to,

* change all those 30 modules
* support both modes (API and SSH) of configuring the remote device
* that had taken multiple years to write

was not something I wanted to undertake.

I honestly leave this open as an exercise for the end user. If you are deeply interested
in making SSH happen, then by all means go after it. Modules that come out of F5 directly
though will remain REST based for the foreseeable future.

.. _set_description: https://devcentral.f5.com/wiki/iControl.LocalLB__VirtualServer__set_description.ashx
.. _set_destination: https://devcentral.f5.com/wiki/iControl.LocalLB__VirtualServer__set_destination.ashx
.. _set_destination_v2: https://devcentral.f5.com/wiki/iControl.LocalLB__VirtualServer__set_destination_v2.ashx
