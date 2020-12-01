// ----------------------------------
// CUSTOM JAVASCRIPT - CONTENT
// ----------------------------------


// Montrer / cacher les réponses des quiz
function montrer_cacher(quiz_id) {
  var liste;
  liste = document.getElementById(quiz_id).getElementsByClassName("itemEMPTY")
  for (i = 0; i < liste.length; i++) {
    if (liste[i].innerHTML.indexOf('[  ]') > -1) {
      liste[i].innerHTML = '[<svg width="1em" height="1em" 2.5;" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="#ff6961" style="vertical-align:middle; margin-bottom:2px" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/></svg>]'
    } else {
      liste[i].innerHTML = "[  ]"
    }
  }
  liste = document.getElementById(quiz_id).getElementsByClassName("itemFULL")
  for (i = 0; i < liste.length; i++) {
    if (liste[i].innerHTML.indexOf('[  ]') > -1) {
      liste[i].innerHTML = '[<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="#77dd77" style="vertical-align:middle; margin-bottom:2px" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>]'
    } else {
      liste[i].innerHTML = "[  ]"
    }
  }
}
