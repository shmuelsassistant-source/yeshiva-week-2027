
(function(){
  var NAMES={};
  document.querySelectorAll('.card').forEach(function(c){NAMES[c.dataset.id]=c.querySelector('h3').textContent;});
  // 3/4-night toggle
  var body=document.body; body.dataset.n=localStorage.getItem('yw27-n')||'3';
  function setN(n){body.dataset.n=n;localStorage.setItem('yw27-n',n);document.querySelectorAll('.tbtn').forEach(function(b){var on=b.dataset.n===n;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on?'true':'false');});}
  document.querySelectorAll('.tbtn').forEach(function(b){b.addEventListener('click',function(){setN(b.dataset.n);});});
  setN(body.dataset.n);
  // family board
  var form=document.getElementById('pref-form'),msg=document.getElementById('form-msg'),note=document.getElementById('mode-note'),list=document.getElementById('responses'),tally=document.getElementById('tally');
  var SHARED=null; var LOCAL_KEY='yw27-local-responses', MINE_KEY='yw27-mine';
  var draft=JSON.parse(localStorage.getItem('yw27-draft')||'{}');
  ['family','pick','second','note'].forEach(function(k){if(draft[k]&&form.elements[k])form.elements[k].value=draft[k];});
  if(draft.nights){var r=form.querySelector('input[name=nights][value="'+draft.nights+'"]');if(r)r.checked=true;}
  form.addEventListener('input',function(){var d=read();localStorage.setItem('yw27-draft',JSON.stringify(d));});
  function read(){var n=form.querySelector('input[name=nights]:checked');return {family:form.elements.family.value.trim(),pick:form.elements.pick.value,second:form.elements.second.value,nights:n?n.value:'',note:form.elements.note.value.trim()};}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function render(items){
    var counts={};items.forEach(function(i){counts[i.pick]=(counts[i.pick]||0)+1;});
    tally.innerHTML=Object.keys(counts).sort(function(a,b){return counts[b]-counts[a];}).map(function(k){return '<span>'+esc(NAMES[k]||k)+': '+counts[k]+'</span>';}).join('')||'<span>No responses yet.</span>';
    var mine=JSON.parse(localStorage.getItem(MINE_KEY)||'{}');
    list.innerHTML=items.slice().reverse().map(function(i){
      var when=i.ts?new Date(i.ts).toLocaleString():'';
      var del=(SHARED&&mine[i.id])||(!SHARED)?' <button type="button" class="del" data-id="'+esc(i.id)+'">remove</button>':'';
      return '<li><strong>'+esc(i.family)+'</strong> → '+esc(NAMES[i.pick]||i.pick)+(i.second?' (2nd: '+esc(NAMES[i.second]||i.second)+')':'')+' · '+esc(i.nights==='either'?'3 or 4 nights':i.nights+' nights')+(i.note?'<br><em>'+esc(i.note)+'</em>':'')+'<br><span class="meta">'+esc(when)+'</span>'+del+'</li>';
    }).join('');
  }
  function localItems(){return JSON.parse(localStorage.getItem(LOCAL_KEY)||'[]');}
  function setMode(shared){SHARED=shared;
    note.className='notice'+(shared?' shared':'');
    note.innerHTML=shared?'<strong>Shared board.</strong> Responses you post are stored on this site\'s server and shown to everyone who opens this link (no login, no accounts). Use a nickname and keep notes free of private details. You can remove a response from the device that posted it. Your draft is also saved on this device.'
      :'<strong>Device-local mode.</strong> The shared server is not reachable right now, so responses are saved only in this browser and nobody else sees them. Use “Copy my pick for WhatsApp” to share.';
  }
  function load(){fetch('/api/feedback',{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(j){setMode(true);render(j.items||[]);}).catch(function(){setMode(false);render(localItems());});}
  form.addEventListener('submit',function(ev){ev.preventDefault();var d=read();if(!d.family||!d.pick||!d.nights){msg.textContent='Please fill in your family name, a top pick and a stay length.';return;}
    msg.textContent='Posting…';
    if(SHARED){fetch('/api/feedback',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json();}).then(function(j){if(!j.ok)throw new Error(j.error||'failed');var mine=JSON.parse(localStorage.getItem(MINE_KEY)||'{}');mine[j.id]=j.secret;localStorage.setItem(MINE_KEY,JSON.stringify(mine));msg.textContent='Posted to the shared board.';load();}).catch(function(e){msg.textContent='Could not post ('+e.message+'). Saved on this device instead.';var it=localItems();d.id='l'+Date.now();d.ts=Date.now();it.push(d);localStorage.setItem(LOCAL_KEY,JSON.stringify(it));render(it);});}
    else{var it=localItems();d.id='l'+Date.now();d.ts=Date.now();it.push(d);localStorage.setItem(LOCAL_KEY,JSON.stringify(it));render(it);msg.textContent='Saved on this device only.';}
  });
  list.addEventListener('click',function(ev){var b=ev.target.closest('.del');if(!b)return;var id=b.dataset.id;
    if(SHARED){var mine=JSON.parse(localStorage.getItem(MINE_KEY)||'{}');fetch('/api/feedback?id='+encodeURIComponent(id)+'&secret='+encodeURIComponent(mine[id]||''),{method:'DELETE'}).then(load);}
    else{localStorage.setItem(LOCAL_KEY,JSON.stringify(localItems().filter(function(i){return i.id!==id;})));render(localItems());}
  });
  document.getElementById('copy').addEventListener('click',function(){var d=read();var txt='Yeshiva Week 2027 — '+(d.family||'our family')+': top pick '+(NAMES[d.pick]||'(none yet)')+(d.second?', second '+NAMES[d.second]:'')+'; '+(d.nights==='either'?'3 or 4 nights':d.nights?d.nights+' nights':'')+(d.note?' — '+d.note:'')+'\n'+location.origin+location.pathname+'#family';
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){msg.textContent='Copied — paste it into WhatsApp.';}).catch(function(){window.prompt('Copy this text:',txt);});});
  load();
})();
