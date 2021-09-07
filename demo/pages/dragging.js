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
var newwinx=10;
var newwiny=10;

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

function candrag(elementname){
    //make a div draggable directly
    elementid=$("#"+elementname);
    $('body').mouseup(function(){__draggingnow=0});
    elementid.mousedown(function(){setdrag(elementid);});
    __dmaxz+=1;
    elementid.css('z-index',__dmaxz);
    windowlist[windowcount]=elementname;
    windowcount+=1;
}

function candrag2(draggabledivname,dragpointdivname){
    //make a div draggable by another div
    $('body').mouseup(function(){__draggingnow=0});
    var dragpointelement=$("#"+dragpointdivname);
    var dragmainelement=$("#"+draggabledivname);
    dragpointelement.mousedown(function(){setdrag(dragmainelement);});
    //dragpointelement.mouseup(function(){__dragitem=null;});
    __dmaxz+=1;
    dragmainelement.css('z-index',__dmaxz);
    windowlist[windowcount]=draggabledivname;
    windowcount+=1;
}

function cleanNullWindows(){
    var newwindowlist=[]
    var newwindowcount=0;
    for (var i=0;i<windowcount;i++){
        if (document.getElementById(windowlist[i]) !== null){
            newwindowlist[newwindowcount]=windowlist[i];
            newwindowcount+=1;
        }
    }
    windowlist=newwindowlist;
    windowcount=newwindowcount;
}

function draggers_cascade(){
    cleanNullWindows();
    dragscount=windowlist.length
    for (var i=0;i<windowcount;i++){
            $("#"+windowlist[i]).css('z-index',1);
            var increment=Math.min(document.body.clientWidth,document.body.clientHeight);
            xpoint=(1+i*increment*0.05) % (document.body.clientWidth/2);
            ypoint=(1+i*increment*0.05) % (document.body.clientHeight/2);
            $("#"+windowlist[i]).animate({ top: ypoint, left: xpoint },250);
    }
}


function newDivWindow(idname,titletext){
    
    if (windowlist.includes(idname)) {
        var switchto = $("#"+idname);
        oldz=switchto.css('z-index');
        if (oldz < __dmaxz) {
            __dmaxz+=1;
            switchto.css('z-index',__dmaxz);
        };
        return;
    };

    var tempdiv = document.createElement("div");
    tempdiv.id = idname;
    tempdiv.className = "floaterdiv";

    var tempdivtitle = document.createElement("div");
    tempdivtitle.id = idname+"_drag";
    tempdivtitle.className = "titlebar";
    tempdivtitle.innerHTML = titletext;
    tempdivtitle.style.width = '97%';

    var tempdivX = document.createElement("div");
    tempdivX.id = idname+"_close";
    tempdivX.className = "titleX"
    tempdivX.innerHTML = "X";
    tempdivX.onclick = function(){document.getElementById(idname).remove();cleanNullWindows();};

    var tempdivcontent=document.createElement("div");
    tempdivcontent.id = idname+"_content";
    tempdivcontent.className = "windowcontent";

    tempdiv.appendChild(tempdivtitle);
    tempdiv.appendChild(tempdivX);
    tempdiv.appendChild(tempdivcontent);
    document.body.appendChild(tempdiv);
    tempdiv.style.top="10%";
    tempdiv.style.left="10%";
    candrag2(idname,idname+"_drag");
}


