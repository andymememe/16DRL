window.onkeyup = function(e) {
   var key = e.keyCode ? e.keyCode : e.which;
   var userid = document.getElementById('hashid').innerHTML;

   if (key == 87 || key == 38) {
       window.location.href = '/move/' + userid + '/up';
   }
   else if (key == 83 || key == 40) {
       window.location.href = '/move/' + userid + '/down';
   }
   else if (key == 65 || key == 37) {
       window.location.href = '/move/' + userid + '/left';
   }
   else if (key == 68 || key == 39) {
       window.location.href = '/move/' + userid + '/right';
   }
}