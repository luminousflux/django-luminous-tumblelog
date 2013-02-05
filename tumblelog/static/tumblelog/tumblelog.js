function initTumblelogLightbox() {
    $(document.body).on('click', 'img[data-large-photo]', function() {
        var el = document.createElement('div');
        var el1 = document.createElement('img');
        $(el1).attr('src', $(this).data('large-photo'));
        $(el).css('text-align', 'center');
        $(el).append(el1);
        $(el).append('<p>'+$(this).parents('.entry').find('.meta .via').html()+'</p>');
        $(el).dialog({'width': '900px', 'modal': true});
    })
}
$(document).ready(initTumblelogLightbox);
