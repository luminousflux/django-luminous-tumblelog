{% load url from future %}
var _BOOKMARKLET = function() {
  function get_selection() {
    var selection = '';
    if(window.getSelection) {
      selection = window.getSelection();
        if (!selection || selection == ''){
          for(var i=0;i<window.frames.length;i++){
            try{
              if(window.frames[i].window.getSelection()!=''){
                  selection = window.frames[i].window.getSelection();
                  break;
              }
            }catch(e){}
          }
        }
      if(selection && selection != '') {
        var div = document.createElement('div');
        div.appendChild(selection.getRangeAt(0).cloneContents());
        selection = div.innerHTML;
      }
    } else if(document.getSelection) {
      selection = document.getSelection();
    } else if(document.selection) {
      var range = document.selection.createRange();
      if (range && range.htmlText)
        selection = range.htmlText;
      else if (range)
        selection = range.text;
    }
    return selection;
  }

  function add_input(form, name, value){
    if (value) {
      var x = document.createElement('input');
      x.setAttribute('type', 'hidden');
      x.setAttribute('name', name);
      x.setAttribute('value', value);
      form.appendChild(x);
    }
  }

  var form = document.createElement('form');
  form.setAttribute('method', 'post');
  form.setAttribute('accept-charset', 'utf-8');
  form.setAttribute('action', 'http://{{site.domain}}{% url 'tumblelog:bookmarklet.html' %}?api_key={{api_key}}');
  form.target = '{{site.name}}_bookmarklet';
  add_input(form, 'url', document.location.href);
  add_input(form, 'selection', get_selection());
  add_input(form, 'title', document.title);

  // images
  for(var i = 0; i < document.images.length; i++) {
    var img = document.images[i];
    if (img.offsetWidth && img.offsetHeight && img.offsetWidth*img.offsetHeight > 70*70) {
      add_input(form, 'img_'+i, img.src);
      add_input(form, 'img_'+i+'_w', img.offsetWidth);
      add_input(form, 'img_'+i+'_h', img.offsetHeight);
    }
  }

  var elts = ['body', 'frameset', 'head'];
  var worked=false;
  for (var i = 0; i < elts.length; i++) {
    var elt=document.getElementsByTagName(elts[i])[0];
    if (elt) {
      elt.appendChild(form);
      form.submit();
      worked=true;
    }
  }
  if (!worked) {
    alert("Sorry, but we couldn't initialize the bookmarklet with this page.");
  }

}();
