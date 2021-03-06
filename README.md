[![DOI](https://zenodo.org/badge/267509217.svg)](https://zenodo.org/badge/latestdoi/267509217)

# SNAPlab Online -- A Web Application for Online Psychoacoustics


This is a bare-bones, but functional Web App for online
hearing experiments designed using the [Django Framework](https://www.djangoproject.com).
The templates are rendered using basic [HTML5](https://en.wikipedia.org/wiki/HTML5) and
styled using [Bootstrap](https://getbootstrap.com/).
Task pages are implemented client-side using [jsPsych](https://www.jspsych.org)
within the ```jspsych``` app.
However, a rudimentary server-side implementation 
with new HTTP responses to advance the experiment
is also available within the ```tasks``` app.


## Goals

The goals of this web app (some features not fully developed/tested) are:

-	Serve as a standalone web app that can be hosted
	on a virtual private server in the cloud (e.g., [Linode](https://www.linode.com)).

- 	Make it easy to create auditory behavioral tasks
	with commonly used task structures:

	* n-AFC tasks using the method of constant stimuli
	* n-AFC adapting on a single parameter on a grid
	* open set speech recognition tasks
	* surveys

-	Make it easy to organize a collection of tasks into an experiment
	that can be linked to recruitment platforms and thereby interfacing
	with anonymous labor markets such as [Prolific](https://www.prolific.co).

-	Play uncompressed, high fidelity audio on a variety of browsers
	across both computers and mobile devices.

-	Implement anonymous sessions for subjects for security
	and HIPAA compliance.

-	Allow users with varying privileges:

	- Users with "experimenter" status
	- Users with "admin" status
	- Anonymous Users with (default) "subject" status

-	Allow response data to be written to a secure database
	and queried on the front-end.

-	Allow for future extensions and enhancements using python code.

## License
### Text and images
The text and images contained in this repository (c) 2020 by Hari Bharadwaj are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

![CC](https://mirrors.creativecommons.org/presskit/icons/cc.svg)![BY](https://mirrors.creativecommons.org/presskit/icons/by.svg)![NC](https://mirrors.creativecommons.org/presskit/icons/nc.svg)![SA](https://mirrors.creativecommons.org/presskit/icons/sa.svg)

### Code
The source code for SNAPlabOnline (c) 2020 by Hari Bharadwaj is licensed under the [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause)

