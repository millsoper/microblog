document.addEventListener('DOMContentLoaded', function(event){
  var path = document.querySelector('#swirl')
  console.log(path);
  var length = path.getTotalLength();
 
  path.style.transition = path.style.WebkitTransition = 'none';

  path.style.strokeDasharray = length + ' ' + length;
  path.style.strokeDashoffset = length;

  path.getBoundingClientRect();

  path.style.transition = path.style.WebkitTransition = 'stroke-dashoffset 12s ease-in-out';

  path.style.strokeDashoffset = '0';
});
