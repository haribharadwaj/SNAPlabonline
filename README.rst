SNAPlab Online -- A Web Application for Online Psychoacoustics
==============================================================

This is a bare-bones, but functional Web App for online
hearing experiments designed using the `Django Framework <https://www.djangoproject.com>`_.
The templates are rendered using basic `HTML5 <https://en.wikipedia.org/wiki/HTML5>`_ and
styled using `Bootstrap <https://getbootstrap.com/>`_.
Currently, all experiment control is event driven,
and new Django views are called to advance the experiment.
However, the design of task and response models are compatible with
future changes to front-end design.
In particular, integration with `jsPsych <https://www.jspsych.org>`_
should be relatively seamless.


The goals of this web app (once fully developed) are:

*	Serve as a standalone web app that can be hosted
	on a virtual private server in the cloud (e.g., `Linode <https://www.linode.com>`_).

* 	Make it easy to create auditory behavioral tasks
	with commonly used task structures:

	* n-AFC tasks using the method of constant stimuli
	* n-AFC adapting on a single parameter on a grid
	* open set speech recognition tasks
	* surveys

*	Make it easy to organize a collection of tasks into an experiment
	that can be linked to recruitment platforms and thereby interfacing
	with anonymous labor markets such as

	* `MTurk <https://www.mturk.com>`_
	* `Prolific <https://www.prolific.co>`_

*	Play uncompressed, high fidelity audio on a variety of browsers
	across both computers and mobile devices.

*	Implement login-based authentication for security
	and HIPAA compliance.

*	Allow users with varying privileges:

	* Users with "experimenter" status
	* Users with "admin" status
	* Users with (default) "subject" status

*	Allow response data to be written to a secure database
	and queried on the front-end.

*	Allow for future extensions and enhancements using python code.


