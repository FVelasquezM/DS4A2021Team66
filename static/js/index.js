const urlVerifyImage = "http://127.0.0.1:5000/app";

/* Inicio */
const $btnImage = document.getElementById('loadImage')
const $photoLoader = document.getElementById('photo')
const $effectLoader = document.getElementById('loader')
const $labelPhoto = document.getElementById('label-photo')
/* App */ 
const $visualMap = document.getElementById('visual-map2')
const $imagePreview = document.querySelector('.image_preview')

$photoLoader.addEventListener("change", function() {
    loadImage('images/test.TIF')
});

var loadImage = function (filename) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', filename);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function (e) {
      var buffer = xhr.response;
      var tiff = new Tiff({buffer: buffer});
      var canvas = tiff.toCanvas();
      var width = tiff.width();
      var height = tiff.height();
      if (canvas) {
        $visualMap.innerHTML = '<div><div><a href="' + filename + '">' +
                      filename +
                      ' (width: ' + width + ', height:' + height + ')' +
                      '</a></div></div>';
        $visualMap.append(canvas);
        $('body').append($elem);
      }
    };
    xhr.send();
};