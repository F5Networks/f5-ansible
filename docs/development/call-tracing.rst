:orphan: true

Call tracing
============

This document details the process of call-tracing the F5 Ansible modules to gain insight into the actual code-execution that is occurring.

.. code-block:: guess

   from pycallgraph import PyCallGraph
   from pycallgraph.output import GraphvizOutput
   from pycallgraph import Config
   from pycallgraph import GlobbingFilter
   config = Config()
   config.trace_filter = GlobbingFilter(exclude=[
       'pycallgraph.*',
       'httplib.*',
       'mimetools.*',
       'rfc822.*',
       'cookielib.*',
       'contextlib.*',
       'threading.*',
       'Queue.*',
       'logging.*',
       'Connection.*',
       'cgi.*',
       'collections.*',
       'socket.*',
       'Context.*',
       '_asFileDescriptor',
       'base64.*',
       'urllib.*',
       'json.*',
       'functools.*',
       '_VerifyHelper.*',
       'weakref.*',
       'distutils.*',
       'string.*',
        # Ansible related
       'ansible.module_utils.basic.AnsibleModule.*',
       'ansible.module_utils.basic.*',
       'ansible.module_utils.parsing.*',
       'ansible.module_utils._text.*',
       'ansible.module_utils.six.*',
   ])
   graphviz = GraphvizOutput(output_file='/tmp/filter_exclude.png')
   with PyCallGraph(output=graphviz, config=config):
       main()
