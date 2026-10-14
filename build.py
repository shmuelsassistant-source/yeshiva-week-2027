
import json, html, os
P=os.path.dirname(os.path.abspath(__file__)); S=os.path.join(P,'site')
d=json.load(open(os.path.join(P,'data.json')))
e=html.escape
def status_badge(s):
    return {'in':'<span class="badge ok">within 3 h</span>','borderline':'<span class="badge warn">borderline (~3 h)</span>','out':'<span class="badge bad">out of range</span>'}[s]
def qk(k):
    return {'exact':'<span class="badge exact">exact-date quote</span>','indicative':'<span class="badge ind">indicative / public rate</span>','pending':'<span class="badge pend">quote pending</span>'}[k]
cards=[]
for c in d['candidates']:
    q=c['quote']; dr=c['drive']
    rows=''.join(f"<tr><th scope='row'>{e(r['unit'])}</th><td class='n3'>{e(r['n3'])}</td><td class='n4'>{e(r['n4'])}</td></tr>" for r in q['per_night'])
    items=''
    for it in q.get('itemized',[]):
        lines=''.join(f'<li>{e(l)}</li>' for l in it['lines'])
        evd=f"<p><a href='{it['evidence']}'>Screenshot of this checkout screen</a></p>" if it.get('evidence') else ''
        items+=f"<details class='item'><summary>{e(it['label'])}</summary><ul>{lines}</ul>{evd}</details>"
    srcs=''.join(f"<li><a href='{u}' rel='noopener'>{e(t)}</a></li>" for t,u in c['sources'])
    evs=''.join(f"<li><a href='{u}'>{e(t)}</a></li>" for t,u in c['evidence'])
    cross=f"<li><strong>Cross-check:</strong> {e(dr['cross'])}</li>" if dr.get('cross') else ''
    cards.append(f"""
<article class="card" id="{c['id']}" data-id="{c['id']}">
  <header class="card-head">
    <h3>{e(c['name'])}</h3>
    <p class="place">{e(c['place'])}</p>
    <p class="badges">{status_badge(c['status'])} {qk(c['quote_kind'])}</p>
  </header>
  <section class="block" aria-labelledby="{c['id']}-drive">
    <h4 id="{c['id']}-drive">Drive from Hallandale Beach, FL</h4>
    <ul>
      <li><strong>OSRM routing:</strong> {dr['osrm_mi']} mi, {e(dr['osrm_h'])} (open-source routing, no live traffic; read Oct 14 2026).</li>
      {cross}
      <li>{e(dr['note'])}</li>
      <li><a href="{c['map']}" rel="noopener">Open directions in Google Maps</a></li>
    </ul>
  </section>
  <section class="block" aria-labelledby="{c['id']}-price">
    <h4 id="{c['id']}-price">Price — <span class="n3-label">3 nights (Sun Jan 24 – Wed Jan 27)</span><span class="n4-label">4 nights (Sun Jan 24 – Thu Jan 28)</span></h4>
    <p class="meta"><strong>Source:</strong> <a href="{q['url']}" rel="noopener">booking page</a> · <strong>Checked:</strong> {e(q['when'])}</p>
    <p class="meta"><strong>Occupancy entered:</strong> {e(q['occupancy'])}</p>
    <div class="tablewrap"><table class="rates">
      <caption class="sr-only">Per-night rates by unit</caption>
      <thead><tr><th scope="col">Unit</th><th scope="col" class="n3">3 nights · per night</th><th scope="col" class="n4">4 nights · per night</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
    {('<p class="meta">'+e(q['per_night_note'])+'</p>') if q.get('per_night_note') else ''}
    {('<h5>Itemized totals</h5>'+items) if items else ''}
    {('<p class="meta"><strong>Benchmark:</strong> '+e(c['benchmark'])+'</p>') if c.get('benchmark') else ''}
  </section>
  <details class="block"><summary>Units, kitchen &amp; self-catering</summary>
    <p><strong>Units / occupancy:</strong> {e(c['units'])}</p>
    <p><strong>Kitchen, fridge, grills, fuel:</strong> {e(c['kitchen'])}</p>
    <p><strong>Groceries, delivery, nearest Chabad:</strong> {e(c['grocery'])}</p>
  </details>
  <details class="block"><summary>Activities &amp; January weekday schedule</summary>
    <p><strong>Included:</strong> {e(c['activities_included'])}</p>
    <p><strong>Paid extras:</strong> {e(c['activities_paid'])}</p>
    <p><strong>Late-January weekdays / weather:</strong> {e(c['schedule'])}</p>
    <p><strong>Indoor fallback:</strong> {e(c['indoor'])}</p>
  </details>
  <details class="block"><summary>Cancellation, group booking, clustering &amp; gathering space</summary>
    <p><strong>Cancellation:</strong> {e(c['cancel'])}</p>
    <p><strong>Group booking route (no property was contacted):</strong> {e(c['group'])}</p>
    <p><strong>Communal / minyan space:</strong> {e(c['gathering'])}</p>
  </details>
  <details class="block"><summary>Sources &amp; evidence (access date Oct 14 2026)</summary>
    <ul class="sources">{srcs}</ul>
    {('<p><strong>Screenshots captured by us:</strong></p><ul class="sources">'+evs+'</ul>') if evs else ''}
  </details>
  <p class="verdict"><strong>Verdict:</strong> {e(c['verdict'])}</p>
</article>""")
rej=''.join(f"<li><strong>{e(n)}</strong> — {e(w)} <a href='{u}' rel='noopener'>source</a></li>" for n,w,u in d['rejected'])
opts=''.join(f"<option value='{c['id']}'>{e(c['name'])}</option>" for c in d['candidates'])
summary_rows=''.join(f"<tr><th scope='row'><a href='#{c['id']}'>{e(c['name'])}</a></th><td>{e(c['drive']['osrm_h'])}{(' / '+e(c['drive']['cross'].split(' /')[0])) if c['drive'].get('cross') else ''}</td><td>{status_badge(c['status'])}</td><td>{qk(c['quote_kind'])}</td><td class='n3'>{e(c['quote']['per_night'][0]['n3'][:70])}{'…' if len(c['quote']['per_night'][0]['n3'])>70 else ''}</td><td class='n4'>{e(c['quote']['per_night'][0]['n4'][:70])}{'…' if len(c['quote']['per_night'][0]['n4'])>70 else ''}</td></tr>" for c in d['candidates'])
page=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yeshiva Week 2027 getaway — comparison of ranches, cabins and activity resorts within 3 h of Hallandale Beach</title>
<meta name="description" content="Independent comparison for a multi-family Jan 24–27 or Jan 24–28, 2027 getaway within three hours of Hallandale Beach, FL: exact-date quotes vs indicative rates, kitchens and grills, activities, cancellation, drive times, and a shared family preference board.">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <h1>Yeshiva Week 2027 getaway</h1>
  <p class="lede">Multi-family trip, <strong>Sun Jan 24 – Wed Jan 27 (3 nights)</strong> or <strong>Sun Jan 24 – Thu Jan 28 (4 nights)</strong>, home before Shabbos Jan 29. Target: within 3 hours' drive of Hallandale Beach, FL; self-catering; lots to do on site.</p>
  <p class="meta">Research snapshot: {e(d['generated'])}. Prices are labelled <em>exact-date quote</em> (read from the property's own booking engine for these dates, timestamp given) or <em>indicative</em> (a public "from" rate or third-party figure — not a quote). Nothing was reserved, nobody was contacted. No kosher certification is claimed for any property.</p>
</header>
<nav class="toc" aria-label="Sections"><ul>
<li><a href="#top3">Top 3</a></li><li><a href="#summary">Summary table</a></li><li><a href="#options">All options</a></li><li><a href="#rejected">Rejected</a></li><li><a href="#family">Family board</a></li><li><a href="#method">Method &amp; limits</a></li><li><a href="#source">Source code</a></li>
</ul></nav>
<main id="main">
<section id="toggle" class="toggle" aria-label="Stay length">
  <span id="toggle-label">Show prices for:</span>
  <div role="group" aria-labelledby="toggle-label">
    <button type="button" class="tbtn active" data-n="3" aria-pressed="true">3 nights · Jan 24–27</button>
    <button type="button" class="tbtn" data-n="4" aria-pressed="false">4 nights · Jan 24–28</button>
    <button type="button" class="tbtn" data-n="both" aria-pressed="false">Both</button>
  </div>
</section>
<section id="top3" class="panel">
  <h2>Top 3</h2>
  <ol class="top">
    <li><strong><a href="#westgate">Westgate River Ranch</a></strong> — the only real "ranch + activities + full-kitchen units" match, with exact-date prices verified (Rail Car all-in: 3 nights <strong>$660.87</strong> prepaid or <strong>$716.25</strong> refundable; 4 nights <strong>$955.00</strong> refundable). Borderline drive (2 h 47 – 3 h 32 depending on routing).</li>
    <li><strong><a href="#hawkscay">Hawks Cay Resort villas</a></strong> — the water-based alternative with full kitchens, pools, marina and a 7-day cancellation policy; 2 h 32 – 2 h 52; expect the highest price; exact quote pending.</li>
    <li><strong><a href="#riverpalm">River Palm Cottages &amp; Fish Camp</a></strong> — the practical self-catering fallback: ~20 cottages with full kitchens on one riverfront property 2 h away, cheap published rates, 25% cancellation fee; no activity program (bring your own). <em>Okeechobee KOA was dropped: its office says no Premium / full-kitchen units are available for either stay (phone, Oct 14).</em></li>
  </ol>
  <p class="meta">Honest ranking caveat: only Westgate has exact-date prices today; Hawks Cay and River Palm are placed on fit, not on a dated quote. Phone quotes for the others are being collected and will be added.</p>
</section>
<section id="summary" class="panel">
  <h2>Summary table</h2>
  <div class="tablewrap"><table class="summary">
    <caption class="sr-only">All candidates at a glance</caption>
    <thead><tr><th scope="col">Option</th><th scope="col">Drive (OSRM / cross-check)</th><th scope="col">Range</th><th scope="col">Price basis</th><th scope="col" class="n3">3-night per night (first unit)</th><th scope="col" class="n4">4-night per night (first unit)</th></tr></thead>
    <tbody>{summary_rows}</tbody></table></div>
</section>
<section id="options" class="panel">
  <h2>All options</h2>
  {''.join(cards)}
</section>
<section id="rejected" class="panel">
  <h2>Rejected options and why</h2>
  <ul class="rejected">{rej}</ul>
</section>
<section id="family" class="panel">
  <h2>Family board — share your preference</h2>
  <p id="mode-note" class="notice">Checking how this board stores responses…</p>
  <noscript><p class="notice">This board needs JavaScript. Without it, text your pick to the group instead.</p></noscript>
  <form id="pref-form" class="pref">
    <div class="field"><label for="fam">Family name or nickname (shown to everyone)</label><input id="fam" name="family" maxlength="40" required autocomplete="off"></div>
    <div class="field"><label for="pick">Top pick</label><select id="pick" name="pick" required><option value="">Choose…</option>{opts}</select></div>
    <div class="field"><label for="second">Second choice (optional)</label><select id="second" name="second"><option value="">None</option>{opts}</select></div>
    <fieldset class="field"><legend>Stay length</legend>
      <label><input type="radio" name="nights" value="3" required> 3 nights (Jan 24–27)</label>
      <label><input type="radio" name="nights" value="4"> 4 nights (Jan 24–28)</label>
      <label><input type="radio" name="nights" value="either"> Either</label>
    </fieldset>
    <div class="field"><label for="note">Note for the group (optional, max 300 characters — no phone numbers or addresses please)</label><textarea id="note" name="note" maxlength="300" rows="3"></textarea></div>
    <div class="actions"><button type="submit" class="btn">Post to the board</button> <button type="button" id="copy" class="btn alt">Copy my pick for WhatsApp</button></div>
    <p id="form-msg" class="meta" role="status" aria-live="polite"></p>
  </form>
  <h3>Responses so far</h3>
  <div id="tally" class="tally" aria-live="polite"></div>
  <ul id="responses" class="responses"></ul>
</section>
<section id="method" class="panel">
  <h2>Method, access limits and what we could not verify</h2>
  <ul>
    <li><strong>Drive times:</strong> OSRM public routing from Hallandale Beach, FL (no traffic model, tends to run 10–25% slower than Google on highways). Where an independent Google Maps reading from the same origin was available on Oct 14 it is shown as a cross-check. January holiday traffic is not modelled. Options between 2 h 45 and 3 h 35 are marked borderline.</li>
    <li><strong>Exact-date quotes</strong> come only from Westgate's own engine (SynXis). It accepts adults only (ages 19+), so a 2-adult/3-child scenario could not be entered; every price is per unit. Only one itemized 3-night checkout screen was captured (prepaid Rail Car). The refundable-plan 3-night total is derived from the engine's own per-night figure and its 12.0% tax line and is labelled as such. The 4-night itemization is an independent read of the same engine at 9:30 AM ET.</li>
    <li><strong>Pending:</strong> KOA Okeechobee, Hawks Cay, Flamingo, Key Largo Cottages, Brighton and River Palm exact-date quotes — their engines require step-through forms or phone bookings; figures shown are public rates or third-party and say so.</li>
    <li><strong>Group availability</strong> was never checked — engines price one unit at a time. Nothing here implies several units are free on these dates.</li>
    <li><strong>Grill / propane / appliance rules</strong> are not published by most properties; marked unknown rather than guessed.</li>
    <li><strong>Kosher:</strong> no certification is claimed anywhere; "nearest Chabad" is a directory lookup, not a kashrut statement. Bring arrival-day essentials and water: grocery delivery to rural resorts can slip to the next morning.</li>
    <li><strong>Privacy:</strong> no reservation numbers, folios, emails, addresses or payment details are published; the Jan 2026 benchmark is a total only.</li>
  </ul>
</section>
<section id="source" class="panel">
  <h2>Source code</h2>
  <p>This site is static HTML/CSS/JS plus a tiny API for the family board. <a href="yeshiva-week-2027-source.zip">Download the full source (zip)</a>. Data lives in <code>data.json</code>; <code>build.py</code> renders the page.</p>
</section>
</main>
<footer class="foot"><p>Independent research snapshot, Oct 14 2026. Prices and policies change — re-check the linked pages before booking.</p></footer>
<script src="script.js" defer></script>
</body></html>"""
open(os.path.join(S,'index.html'),'w').write(page)
print('built', len(page))
