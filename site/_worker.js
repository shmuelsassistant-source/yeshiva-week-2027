
const MAX=400;
function json(o,s){return new Response(JSON.stringify(o),{status:s||200,headers:{'content-type':'application/json','cache-control':'no-store'}});}
function clean(s,n){return String(s==null?'':s).replace(/[\u0000-\u001f]/g,' ').slice(0,n).trim();}
export default {
  async fetch(req, env) {
    const u=new URL(req.url);
    if(u.pathname==='/api/feedback'){
      if(!env.DATA) return json({ok:false,error:'no shared store bound'},503);
      let items=[]; try{items=JSON.parse(await env.DATA.get('feedback')||'[]');}catch(e){items=[];}
      if(req.method==='GET'){return json({ok:true,items:items.map(i=>({id:i.id,family:i.family,pick:i.pick,second:i.second,nights:i.nights,note:i.note,ts:i.ts}))});}
      if(req.method==='POST'){
        let b; try{b=await req.json();}catch(e){return json({ok:false,error:'bad json'},400);}
        const it={id:crypto.randomUUID(),secret:crypto.randomUUID(),family:clean(b.family,40),pick:clean(b.pick,30),second:clean(b.second,30),nights:clean(b.nights,6),note:clean(b.note,300),ts:Date.now()};
        if(!it.family||!it.pick||!it.nights) return json({ok:false,error:'missing fields'},400);
        items.push(it); if(items.length>MAX) items=items.slice(-MAX);
        await env.DATA.put('feedback',JSON.stringify(items));
        return json({ok:true,id:it.id,secret:it.secret});
      }
      if(req.method==='DELETE'){
        const id=u.searchParams.get('id'),secret=u.searchParams.get('secret');
        const n=items.length; items=items.filter(i=>!(i.id===id&&i.secret===secret));
        if(items.length!==n) await env.DATA.put('feedback',JSON.stringify(items));
        return json({ok:true,removed:n-items.length});
      }
      return json({ok:false,error:'method'},405);
    }
    return env.ASSETS.fetch(req);
  }
};
