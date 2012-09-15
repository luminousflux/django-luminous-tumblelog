$(document).ready(function() {
    $('.form.photo img').live('click', function(event) {$('#id_photo-photo').val(event.toElement.src);});
});
