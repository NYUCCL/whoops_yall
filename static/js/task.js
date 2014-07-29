/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to
// they are not used in the stroop code but may be useful to you



/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/


// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
// $(window).load( function(){
//     psiTurk.doInstructions(
//     	instructionPages, // a list of pages you want to display in sequence
//     	function() { currentview = new StroopExperiment(); } // what you want to do when you are done with instructions
//     );
// });
