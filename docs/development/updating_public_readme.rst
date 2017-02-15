Updating the public README file
===============================

The README file landing page that you see when you visit the Github repository
is served from the `master` branch of code. This, however, differs from where
the code for the project is developed.

Since development happens on the `devel` branch, it may be necessary to update
the `master` branches README file to reflect changes made in the devel branch.

To do this, the repo includes a `make` target called `update-master-readme`.

When this command runs, the following will happen.

