document.addEventListener("DOMContentLoaded", function(event) {
  var path = document.getElementById('swirl');
  
  var pathLength = path.getTotalLength();

  path.style.strokeDasharray = pathLength + ' ' + pathLength;

  path.style.strokeDashoffset = pathLength;

  path.getBoundingClientRect();

  window.addEventListener('scroll', function(e) {
    var scrollPercentage = (document.Element.scrollTop + document.body.scrollTop) /
    (document.documentElement.scrollHeight - document.documentElement.clientHeight);

    var drawLength = pathLength * scrollPercentage;

    path.style.strokeDashoffset = pathLength - drawLength;

    if (scrollPercentage >= 0.99) {
      path.style.strokeDasharray = "none";
    } else {
      path.style.strokeDasharray = pathLength + ' ' + pathLength;
    }
  });
});
