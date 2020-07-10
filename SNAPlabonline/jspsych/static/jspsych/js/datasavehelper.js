/* Function to save all the data at the end of a jsPsych experiment
by issuing an AJAX call using jQuery (which is $)*/
function saveData(data, subjid, task_url, interactionData){
// Use jQuery to send an AJAX post request to savejspdata/
	$.ajax(
		{
		    type: 'POST',
		    url: '/savejspdata/',
		    data: {
		    	// Need to add parent study fields
		    	'jsPsychData': data,
		    	'subjid': subjid,
		    	'task_url': task_url,
		    	'interactionData': interactionData,
			},
		    success: function(){
		    	window.location.href = '/study/redirecthome/';
		    } 
		}
	);
}


// Function to save data from single trial
function saveSingleTrial(data, subjid, task_url, trialnum, correct){
// Use jQuery to send an AJAX post request to savejsptrial/
	$.ajax(
		{
		    type: 'POST',
		    url: '/savejsptrial/',
		    data: {
		    	// Need to add parent study fields
		    	'jsPsychData': data,
		    	'subjid': subjid,
		    	'task_url': task_url,
		    	'trialnum': trialnum,
		    	'correct': correct
			},
		    success: function(){

		    } 
		}
	);
}

