# Cookiecutter for CSCI Psets

This component assignment is for your own cookiecutter fork.

We will customize our own cookiecutter repo, and use it to bootstrap our pset
repos.

Note: This problem set will involve submitting two separate assignments:

1. customized cookiecutter (here)
2. pset 3 (released shortly)

Please submit links to both Canvas assignments when you have completed!

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Create a cookiecutter for this course](#create-a-cookiecutter-for-this-course)
  - [Settings](#settings)
  - [Template](#template)
  - [Pipfile and Pipfile.lock](#pipfile-and-pipfilelock)
  - [Including your utils](#including-your-utils)
    - [Docker (optional)](#docker-optional)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Create a cookiecutter for this course

In the last problem set, you used cookiecutter to create your csci-utils
repository. If you recall, you made a bunch of changes to configurations (in
.travis.yml, tox.ini, setup.py, etc.). However, if you were to use cookiecutter
again for a new project, you would have to change all those configurations
again!

Now we will work on modifying your own version of a cookiecutter template
repository, so that every time you create a project using the cookiecutter
template, your preferred configurations are up-to-date.

You may continue to develop this repository throughout the course. If you make
any changes beyond those instructed, please ensure to mention them in the
problem set you are actively working on, and let us know if you add something
awesome!

Note that this repo will have two directories with similar contents:

```
cookiecutter-csci-pset-GITHUBID/   <- repo root directory
    .travis.yml                    <- tests for the template itself!
    {{ cookiecutter.repo_name }}/  <- template directory
        .travis.yml                <- rendered into tests for new project
```

We will be [creating our cookie cutter from
scratch](https://cookiecutter.readthedocs.io/en/latest/first_steps.html), but
you can refer to  any of the [common
cookiecutters](https://cookiecutter.readthedocs.io/en/latest/readme.html#a-pantry-full-of-cookiecutters)
for reference.

NB: this assignment was templated using
[cookiecutter-template](https://github.com/eviweb/cookiecutter-template), a
cookiecutter template to help in creating... cookiecutter templates!

### Settings

Just like you did in the previous problem set, inspect `cookiecutter.json`.

Change the defaults in this file or add any new parameters you wish.

NB: the first item in a list is the default. You can also remove other options
if you'd like.

The value of this is that every time you render a new project for this class
using this cookiecutter repo, you will not need to re-type these defaults. We
are capturing our best practices in code!

Be sure to use `csci-e-29` as the github username.

One thing to note - we will separate the `repo_name`, which should refer to the
folder name on github (eg, `2019fa-pset-6-gorlins`), vs the name of the actual
project (eg, `pset-6`).

Note, Jinja2 uses the pipe operator (`|`) to invoke
[filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#filters).

Here are some recommended params and default settings:

* `github_username`: `csci-e-29` (because it will live in our org)
* `repo_name`: `2019fa-{{ cookiecutter.project_name|lower|replace(' ','-') }}-GITHUBID`
* `project_slug`: `{{ cookiecutter.project_name|lower|replace(' ','_') }}`
* `install_csci_utils`: `yes`

### Template

Note that this is similar to what you did for csci utils, but this time, it's in
your cookiecutter template so that it is reproduced every time you make a new
project.

Within the template folder
`cookiecutter-csci-pset-<YOUR_GITHUB_ID>/{{cookiecutter.repo_name}}` (NOT in the
root directory), copy over the structure from Pset 1 including your .travis.yml,
Pipfile, and pset_1 code directory.  Do not copy the `Makefile` or anything
related to data, but include all other files (including hidden ones like
`.coveragerc`).

***Go through these files and replace all references to 'pset_1'*** with the
appropriate `{{ cookiecutter.project_slug }}` or similar.

Remove any other code that is pset 1 specific, and ensure your travis is not
downloading any files in the build. Your new travis builds should still have a
'tests' and 'answers' stage just like Pset 1.

You should ensure you have a `__main__.py` as well as a `__version__` inside
your pset `__init__.py` that works programatically (eg using setuptools_scm).

You do not need a `setup.py`.

Ensure `pytest.ini` is configured to pick up tests in your new project,
including branch coverage!

When the template is complete, you should be able to render the template with a
new project name, cd into that directory, run `pipenv install --dev`, then
`pipenv run pytest` and have things 'just work'.  If you commit and push this
code to Travis, the build should run correctly as well (though, the tests in the
rendered template need not pass immediately!).

### Pipfile and Pipfile.lock

Note you should include a `Pipfile` in the template.  Best practice would
suggest you ***not*** include the lockfile, and thus start each new project with
the most recent dependencies.  However, you may want to compromise and include a
lock file (or even make that conditional on a cookiecutter arg!) to ensure you
have an immediately working env.  This can help with Docker setup as well (see
below).

### Including your utils

The following will require you to setup your github token (see instructions in
Pset 1).

Conditionally, if `install_csci_utils == 'yes'`, your new pset should install
your utils.  Manually edit the Pipfile to look something like this, adding in
any additional cookiecutter logic:

```
[packages]
csci-utils = {editable = true,git = "https://github.com/csci-e-29/2019fa-csci-utils-GITHUBID"}
...
```

If you cannot get this to work conditionally, simply include it for partial
credit.

#### Docker (optional)

If you are using the docker workflow, your template should include the docker
components as well.

Don't forget to include this in your `Dockerfile` to ensure you can install
your utils:

```Dockerfile
ARG CI_USER_TOKEN
RUN echo "machine github.com\n  login $CI_USER_TOKEN\n" >~/.netrc
```

If you don't include your Pipfile.lock in the template, you may need to manually
'bootstrap' it in new rendered templates. To do so, after rendering the
template, comment out all lines in your Dockerfile starting with `COPY Pipfile
.`. Build the docker image, then run:

```bash
./drun_app pipenv install
```

Restore the commented lines in the Dockerfile, and you should be able to rebuild
your docker image and proceed normally. If you desire, you could take this
lockfile, template out the part with the name of the rendered package, and
commit it back to the template itself to avoid bootstrapping in the future.
