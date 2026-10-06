const toggle=document.querySelector('.menu-button');
const drawer=document.querySelector('#main-nav');
const closeButton=document.querySelector('.drawer-close');
const scrim=document.querySelector('.menu-scrim');
const mobile=matchMedia('(max-width:760px)');
let opened=false;
function setOpen(value,restore=true){
 opened=value&&mobile.matches;
 toggle.setAttribute('aria-expanded',String(opened));
 drawer.classList.toggle('open',opened);
 scrim.classList.toggle('open',opened);
 document.body.classList.toggle('menu-open',opened);
 drawer.inert=mobile.matches&&!opened;
 if(mobile.matches){drawer.setAttribute('aria-hidden',String(!opened));}else{drawer.removeAttribute('aria-hidden');}
 if(opened){drawer.setAttribute('role','dialog');drawer.setAttribute('aria-modal','true');requestAnimationFrame(()=>closeButton.focus());}
 else{drawer.removeAttribute('role');drawer.removeAttribute('aria-modal');if(restore&&mobile.matches)toggle.focus();}
}
toggle.addEventListener('click',()=>setOpen(!opened));
closeButton.addEventListener('click',()=>setOpen(false));
scrim.addEventListener('click',()=>setOpen(false));
drawer.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false,false);});
document.addEventListener('keydown',event=>{
 if(!opened)return;
 if(event.key==='Escape'){event.preventDefault();setOpen(false);}
 if(event.key==='Tab'){
 const items=[...drawer.querySelectorAll('a,button')].filter(item=>item.getClientRects().length);
 const first=items[0],last=items[items.length-1];
 if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
 else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
 }
});
mobile.addEventListener('change',()=>setOpen(false,false));setOpen(false,false);

const search=document.querySelector('#region-search');search?.addEventListener('input',()=>{const query=search.value.toLocaleLowerCase('tr').trim();let total=0;document.querySelectorAll('.location').forEach(item=>{const match=item.textContent.toLocaleLowerCase('tr').includes(query);item.hidden=!match;if(match)total++});document.querySelector('#result-count').textContent=total+' hizmet noktası gösteriliyor.'});
