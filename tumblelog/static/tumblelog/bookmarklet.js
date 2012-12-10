$(document).ready(function() {
    $('.datetimeinput').datepicker({'dateFormat': 'yy-mm-dd'});

    $('#switcher').tabs({'active': active_tab_index});
});

$(document).ready(function() {
    $('.form.photo img').live('click', function(event) {$('#id_photo-photo').val(event.toElement.src);});
});
