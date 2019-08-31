/** Page Loading Effects 1.0.2
 * @Documentation https://github.com/esstat17
 * @Copyright: InnoveDesigns.com
 * @Author: Elvin D.
 */ 
 
var plePreloader={speed:5e3,elem:"ple-loader-wraps",elemInner:"",preloaderOn:function(){var e=document.getElementsByTagName("html")[0],t=document.createElement("div");t.id=this.elem,t.innerHTML='<div id="ple-animates">'+this.elemInner+"</div>",e.appendChild(t)},preloaderOff:function(){function e(e,t){var e=document.getElementById(e);if("none"!=e.style.display){document.getElementById("ple-animates").style.display="none",e.style.opacity||(e.style.opacity=1);var n=setInterval(function(){e.style.opacity-=.05,e.style.opacity<=0&&(clearInterval(n),e.style.display="none")},t/50)}}var t=this.elem,n=function(){e(t,1e3)};setTimeout(n,this.speed)},kicks:function(){this.preloaderOn(),this.preloaderOff()}};

