=============
mumuki-xce
=============

Solve `Mumuki <https://mumuki.io>`_ exercises using your favorite code editor

Description
-----------

This package allows you to load, solve and submit assignments in two different ways:

* Using an standard editor - like vim or Visual Studio Code - and the standard Python interpreter
* Using Colab

Standard Editor Usage
---------------------

Environment setup
=================

You will need to use ``python`` and ``pip`` in order to solve exercises.
Please ensure you have those commands locally installed in your
computer. Then install ``mumuki-xce``:

.. code:: shell

   pip install mumuki-xce --quiet

Now you are ready to solve exercises!

Solving an exercise
===================

Just create a new python file with ``py`` extension, and paste the
following code in it:

.. code:: python

   from mumuki import Mumuki
   mumuki = Mumuki("#...token...#", "#...locale...#")
   mumuki.visit("#...organization...#", "#...exercise_id...#")

   # ...place your solution here...

   mumuki.test()

If you want to submit your solution, just run on your terminal

.. code:: bash

   python your_file.py

If you just want to load it into a node interpreter and test and play
with your code, run:

.. code:: bash

   python -i your_file.py


Colab Usage
-----------------

Environment setup
=================

In order to solve exercises you will need to visit and log in to [`Colab`](https://colab.research.google.com/).


Solving an exercise
===================


First create a cell with the following code:

.. code:: python

  !pip install mumuki-xce --quiet

  from mumuki import IMumuki
  mumuki = IMumuki("#...token...#", "#...locale...#")
  mumuki.visit("#...organization...#", "#...exercise_id...#")

Then create another cell, whose first line must be `%%solution`. Then write your solution above it:

.. code:: python

  %%solution

  # ...your solution goes here

Now please edit and run your cells as needed. Feel free also to create aditional cells. When you are ready, add another cell will the following code:

.. code:: python

  mumuki.test()

If you modify your code, don't forget to run your cells again.

Development
============

In order to build this project, clone it and then run:

```bash
# load venv
$ source .venv/bin/activate
# configure project and run pytest
$ tox
```

If you want to test the latest version of this project in your Colab or Jupyter environment, install `xce` within a cell like this:

```
!pip install git+https://github.com/mumuki/mumuki-xce-py.git@master
```

In order to deploy the latest version, tag this project and then:

```bash
$ tox -e build
$ tox -e publish
$ tox -e publish -- --repository pypi
```