
(function(){
 var L=['zh-Hans','zh-Hant','en'];
 function cur(){var u=new URLSearchParams(location.search).get('lang');var s=localStorage.getItem('hl_lang');return (u&&L.indexOf(u)>=0)?u:(s&&L.indexOf(s)>=0?s:'zh-Hans');}
 function apply(lang){
   localStorage.setItem('hl_lang',lang); document.documentElement.lang=lang;
   var T=window.HL_T||{}; var d=T[lang]||{};
   document.querySelectorAll('[data-i18n]').forEach(function(el){var k=el.getAttribute('data-i18n');if(d[k]!=null)el.innerHTML=d[k];});
   var tk='page_title'; if(d[tk])document.title=d[tk];
   document.querySelectorAll('.hl-lang-btn').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-lang')===lang);});
 }
 window.HL_setLang=function(l){apply(l);};
 document.addEventListener('DOMContentLoaded',function(){apply(cur());});
})();
