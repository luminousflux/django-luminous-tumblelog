{% load url from future %}var es=['body','frameset','head'];
var u='http://{{site.domain}}{% url 'tumblelog:bookmarklet.js' %}';
var fn='{{site.name}}_bookmarklet';
var u1 = 'http://{{site.domain}}{% url 'tumblelog:bookmarklet.html' %}';

window.open(u1,fn,'toolbar=0,resizable=1,scrollbars=yes,status=1,width=500,height=600');

try
{
    var s=document.createElement('script');
    s.setAttribute('src',u);
    s.setAttribute('type', 'text/javascript')
    for (var i=0;i<es.length;i++) {
        var e=document.getElementsByTagName(es[i])[0];
        if(e) {
            e.appendChild(s);
            break;
        }
    }
}
catch(e)
{
      alert("This doesn't work here.");
}
void(0);
