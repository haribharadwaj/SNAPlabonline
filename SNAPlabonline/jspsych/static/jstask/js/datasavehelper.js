/* Function to save all the data at the end of a jsPsych experiment
by issuing an AJAX call using jQuery (which is $)*/
function saveData(data){
// Use jQuery to send an AJAX post request to savejspdata/
	$.ajax(
		{
		    type: 'POST',
		    url: 'savejspdata/',
		    data: {
		    	'jsPsychData': data
			},
		    success: function(){

		    } 
		}
	);
}

// Function to save data from single trial
function saveSingleTrial(data){
// Use jQuery to send an AJAX post request to savejsptrial/
	$.ajax(
		{
		    type: 'POST',
		    url: 'savejsptrial/',
		    data: {
		    	'jsPsychData': data
			},
		    success: function(){

		    } 
		}
	);
}
