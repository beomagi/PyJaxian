var __mx=0;
var __my=0;
var __ox=0;
var __oy=0;
var __dx=0;
var __dy=0;
var __dmaxx=0;
var __dmaxy=0;
var __dmaxz=0;
var __draggingnow=0;
var __dragitem;

var windowlist = new Array();
var windowcount = 0;

$(document).ready(function(){
	$(document).mousemove(function(e){
		__mx=e.pageX;
		__my=e.pageY;
		if (__draggingnow==1) {
			var newy=__dy+__my-__oy;
			var newx=__dx+__mx-__ox;
			if (newy < 0) {newy=0;}
			if (newx < 0) {newx=0;}
			if (newy > __dmaxy) {newy=__dmaxy;}
			if (newx > __dmaxx) {newx=__dmaxx;}
			__dragitem.offset({ top: (newy), left: (newx) });
		}
	});
});



function setdrag(elementid){
	__dragitem=elementid;
	divpos=__dragitem.position();
	__dy=divpos.top;
	__dx=divpos.left;
	__ox=__mx;
	__oy=__my;
	__dmaxx=$('body').width()-__dragitem.width()
	__dmaxy=$('body').height()-__dragitem.height()
	__draggingnow=1;
	curz=__dragitem.css('z-index');
	if (curz < __dmaxz) {
		__dmaxz+=1;
		__dragitem.css('z-index',__dmaxz);
	}
}

function candrag(elementid){
	$('body').mouseup(function(){__draggingnow=0});
	elementid.mousedown(function(){setdrag(elementid);});
	__dmaxz+=1;
	elementid.css('z-index',__dmaxz);
	windowlist[windowcount]=elementid;
	windowcount+=1;
}

function draggers_cascade(draglist){
	dragscount=draglist.length
	for (var i=0;i<windowcount;i++){
			draglist[i].css('z-index',1);
			draglist[i].animate({ top: (10+i*20), left: (10+i*20) },100);
	}
}
