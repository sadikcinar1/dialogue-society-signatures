"""The staff signature app -- one page, Personal or Branch.

build() returns two variants:
  hosted  -- for a web host; includes the Outlook download button
  preview -- for a Claude artifact, which cannot start a download, so that
             button and its code are removed rather than left to fail silently
"""
import os
import re as _re


def build(VERSION, VLABEL, MARK, LOCKUP, LOCKUP_DARK, render, theme):
    K = theme
    MARK_URI = MARK
    # the same template.js the build renders with, inlined so the page can
    # rebuild the preview live as someone types. One source of truth.
    TEMPLATE = open(os.path.join(os.path.dirname(__file__), 'template.js'),
                    encoding='utf-8').read()

    APP_CSS = r'''
    .build{display:grid; grid-template-columns:300px minmax(0,1fr); gap:26px; align-items:start}
    .build>*{min-width:0}
    @media(max-width:800px){
      .build{grid-template-columns:minmax(0,1fr)}
      /* One column puts the form first and the preview under all of it, which
         means nothing you type is on screen while you type it. Pull the
         preview and its buttons above the form instead. */
      .sticky{order:-1}
    }
    .form{background:var(--surface); border:1px solid var(--line); border-radius:3px;
      padding:22px; display:flex; flex-direction:column; gap:15px}
    .field{display:flex; flex-direction:column; gap:5px}
    .field label{font-size:12px; font-weight:600; letter-spacing:.03em; color:var(--ink)}
    .field .hint{font-size:12px; color:var(--faint); line-height:1.45}
    input[type=text], input[type=email], select{
      font-family:inherit; font-size:14px; color:var(--ink); background:var(--ground);
      border:1px solid var(--line); border-radius:2px; padding:9px 11px;
      width:100%; min-width:0}
    input:focus-visible, select:focus-visible{outline:2px solid var(--blue);
      outline-offset:-1px; border-color:var(--blue)}
    .check{display:flex; align-items:flex-start; gap:9px; font-size:13.5px;
      color:var(--soft); line-height:1.45}
    .check input{margin:2px 0 0; accent-color:var(--blue); flex:none}
    .divider{height:1px; background:var(--hair); margin:2px 0}
    .sticky{position:sticky; top:22px; display:flex; flex-direction:column; gap:15px; min-width:0}
    @media(max-width:800px){.sticky{position:static}}
    .warnbox{border-left:3px solid var(--warn); background:var(--surface);
      padding:12px 16px; font-size:13.5px; color:var(--soft); display:none}
    .warnbox.on{display:block}
    .linkout{display:none; flex-direction:column; gap:7px;
      background:var(--surface); border:1px solid var(--line); border-radius:3px;
      padding:14px 16px}
    .linkout.on{display:flex}
    .linkout code{display:block; word-break:break-all; font-size:11.5px;
      color:var(--soft); line-height:1.5}
    .linkout strong{font-size:12px; letter-spacing:.03em}
    .mode{font-size:11px; font-family:'IBM Plex Mono',ui-monospace,monospace;
      color:var(--faint); display:flex; align-items:center; gap:7px}
    .mode b{font-weight:400}
    .dot{width:7px; height:7px; border-radius:50%; background:var(--ok); flex:none}
    .dot.embed{background:var(--warn)}
    .modes{display:grid; grid-template-columns:1fr 1fr; gap:0; border:1px solid var(--line);
      border-radius:2px; overflow:hidden}
    .modes label{position:relative; margin:0; cursor:pointer}
    .modes input{position:absolute; opacity:0; width:1px; height:1px}
    .modes span{display:block; text-align:center; padding:9px 8px; font-size:13.5px;
      font-weight:600; color:var(--soft); background:var(--ground);
      transition:background .14s, color .14s}
    .modes label+label span{border-left:1px solid var(--line)}
    .modes input:checked+span{background:var(--blue); color:var(--onblue)}
    .modes input:focus-visible+span{outline:2px solid var(--blue); outline-offset:-2px}
    [hidden]{display:none!important}
    .tiny{background:none; border:0; padding:0; font-size:12.5px; font-weight:500;
      color:var(--blue); text-decoration:underline; cursor:pointer; width:auto}
    .tiny:hover{filter:brightness(1.15)}
    '''


    SPEC = [
        ('Logo mark',     'Blue mark, 70&times;75, left of the text',  '#008AC4', 'Brand blue', '3.87', 'graphic'),
        ('Vertical rule', '4px left border, full height',             '#008AC4', 'Brand blue', '3.87', 'graphic'),
        ('Name',          'Bold 15px, uppercase &mdash; personal',   '#424242', 'Brand grey', '10.05', 'pass'),
        ('Branch lead',   'Bold 15px &mdash; branch signatures',     '#007AAD', 'Text blue',  '4.79', 'pass'),
        ('Job title / second line', 'Regular 11.5px',                '#6E6E6E', 'Soft grey',  '5.10', 'pass'),
        ('Organisation',  'Bold 13px, region appended',              '#007AAD', 'Text blue',  '4.79', 'pass'),
        ('Field labels',  'Bold 10px',                               '#424242', 'Brand grey', '10.05', 'pass'),
        ('Links',         'Regular 11.5px, no underline',            '#007AAD', 'Text blue',  '4.79', 'pass'),
        ('Address',       'Regular 11.5px',                          '#424242', 'Brand grey', '10.05', 'pass'),
        ('Social row',    'Bold 11px, bullet separated',             '#007AAD', 'Text blue',  '4.79', 'pass'),
        ('Charity line',  'Regular 10px, 1px border above',          '#6E6E6E', 'Soft grey',  '5.10', 'pass'),
    ]
    def _spec_row(n, d, hx, lab, cr, st):
        badge = '' if st == 'graphic' else ' <span class="pass">AA</span>'
        return ('          <tr><th scope="row">' + n + '</th><td>' + d + '</td>\n'
                '            <td class="sw"><span style="background:' + hx + '"></span>'
                '<code>' + hx + '</code><em>' + lab + '</em></td>\n'
                '            <td class="num">' + cr + ':1' + badge + '</td></tr>')

    SPEC_ROWS = chr(10).join(_spec_row(*r) for r in SPEC)

    WHICH = [
        ('Use Personal for your own mail',
         'Anything you write as yourself. A named sender is easier to reply to and easier '
         'to trust.'),
        ('Use Branch for shared inboxes',
         'Addresses answered by whoever is on duty &mdash; <code>info@</code>, a branch '
         'address, bookings, enquiries. Naming one person makes every reply look like it '
         'came from them.'),
        ('Use Branch for announcements',
         'Newsletters and mail sent by the organisation rather than by a colleague.'),
        ('Regions go on the Branch form',
         'The region is appended to the name &mdash; <em>Dialogue Society Birmingham</em> '
         '&mdash; so a branch reads as part of the whole.'),
    ]
    WHICH_CARDS = chr(10).join(
        f'''      <div class="card"><h3>{t}</h3><p style="margin:0;color:var(--soft);font-size:14.5px;">{d}</p></div>'''
        for t, d in WHICH)


    def make_body(with_download):
      DL_BTN = ('<button class="ghost" id="dl" type="button">Download for Outlook</button>'
                if with_download else '')
      OUTLOOK = ('''<div class="card"><h3>Outlook on Windows</h3><ol>
                <li>Press <strong>Download for Outlook</strong> above.</li>
                <li>Press <strong>Windows&nbsp;+&nbsp;R</strong>, type
                <code>%appdata%\\Microsoft\\Signatures</code> and press Enter.</li>
                <li>Move the downloaded file into that folder.</li>
                <li>In Outlook, open <strong>File &rarr; Options &rarr; Mail &rarr;
                Signatures</strong> and it will be listed.</li>
                <li>Set it as the default for <em>New messages</em> and
                <em>Replies/forwards</em>.</li>
          </ol></div>''' if with_download else '''<div class="card"><h3>Outlook on Windows</h3><ol>
                <li>Press <strong>Copy signature</strong> above.</li>
                <li>Open <strong>File &rarr; Options &rarr; Mail &rarr; Signatures</strong>.</li>
                <li>Press <strong>New</strong>, name it <em>Dialogue Society</em>.</li>
                <li>Click into the edit box and paste with <strong>Ctrl&nbsp;+&nbsp;V</strong>.</li>
                <li>Set it as the default for <em>New messages</em> and
                <em>Replies/forwards</em>.</li>
          </ol></div>''')
      NOSCRIPT = ('''<noscript><div class="note"><strong>JavaScript is switched off.</strong>
            This page builds your signature in your own browser, so it needs it. The
            two ready-made signatures &mdash;
            <a href="personal.html" style="color:var(--blue)">personal</a> and
            <a href="branch.html" style="color:var(--blue)">branch</a> &mdash; are
            plain pages and work either way.</div></noscript>''' if with_download else '')
      return f'''<div class="wrap">
      <header class="mast">
        {K.lockup(LOCKUP, LOCKUP_DARK)}
        <div>
          <h1>Make your email signature</h1>
          <p>Personal or branch. Fill in the details, press <strong>Copy signature</strong>,
          and paste it into Gmail, Apple Mail or Outlook. Everyone who uses this page gets
          the same colours, the same spacing and the correct logo.</p>
        </div>
      </header>

      <section>
        <div class="build">
          <form class="form" id="f" autocomplete="off">
            <div class="field">
              <label>Signature type</label>
              <div class="modes" role="radiogroup" aria-label="Signature type">
                <label><input type="radio" name="lead" value="person" checked><span>Personal</span></label>
                <label><input type="radio" name="lead" value="org"><span>Branch</span></label>
              </div>
              <span class="hint" id="modehint"></span>
            </div>
            <div class="divider"></div>
            <div id="g-person">
              <div class="field">
                <label for="i-name">Full name</label>
                <input type="text" id="i-name" placeholder="e.g. Sadik Cinar" spellcheck="false">
              </div>
              <div class="field" style="margin-top:15px">
                <label for="i-title">Job title</label>
                <input type="text" id="i-title" placeholder="e.g. Executive Director" spellcheck="false">
              </div>
            </div>
            <div class="field" id="g-strap" hidden>
              <label for="i-strap">Second line &mdash; optional</label>
              <input type="text" id="i-strap" placeholder="A motto, or leave empty" spellcheck="false">
              <span class="hint">Your motto or a short description &mdash; e.g.
              <em>Building Community Trust</em>, or <em>Enquiries and bookings</em>. Sits
              under the name in grey. About 45 characters keeps it on one line.</span>
            </div>
            <div class="field">
              <label for="i-email">Email address</label>
              <input type="email" id="i-email" placeholder="e.g. name@dialoguesociety.org" spellcheck="false">
            </div>
            <div class="field">
              <label for="i-phone">Phone or WhatsApp</label>
              <input type="text" id="i-phone" placeholder="Optional" spellcheck="false">
              <span class="hint">Adds a <strong>T / WA</strong> row.</span>
            </div>
            <div class="divider"></div>
            <div class="field">
              <label for="i-branch">Region</label>
              <input type="text" id="i-branch" placeholder="Blank for head office" spellcheck="false">
              <span class="hint">Appended to &ldquo;Dialogue Society&rdquo;. Type only the
              region.</span>
            </div>
            <div class="field">
              <label for="i-address">Office address</label>
              <input type="text" id="i-address" value="29 High Holborn, London WC1V 6AZ" spellcheck="false">
              <span class="hint">Change this and the region above if you are not at
              head office.</span>
            </div>
            <div class="divider"></div>
            <label class="check"><input type="checkbox" id="i-social" checked>
              <span>Include the social links row</span></label>
            <label class="check"><input type="checkbox" id="i-charity" checked>
              <span>Include the charity registration line<br>
              <span class="hint">Keep this on &mdash; it is a required disclosure.</span></span></label>
            <div class="divider"></div>
            <button class="tiny" id="forget" type="button">Forget my saved details</button>
          </form>

          <div class="sticky">
            {NOSCRIPT}
            <div class="stage">
              <div class="stage-cap"><span>Your signature</span><b>actual size</b></div>
              <div id="sig"></div>
            </div>
            <div class="mode" id="mode"><span class="dot" id="dot"></span><b id="modetxt">checking logo&hellip;</b></div>
            <div class="warnbox" id="warn"></div>
            <div class="actions">
              <button class="primary" id="copy" type="button">Copy signature</button>
              {DL_BTN}
              <button class="ghost" id="mylink" type="button">Copy my link</button>
              <span class="flash" id="flash" role="status" aria-live="polite"></span>
            </div>
            <div class="linkout" id="linkout">
              <strong>Your personal link</strong>
              <code id="linkurl"></code>
              <span class="hint">Bookmark it, or send it to someone so their details are
              already filled in.</span>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div class="head">
          <h2>Adding it to your email</h2>
          <p class="lede">Once per program. Press <strong>Copy signature</strong> first &mdash;
          copy the preview, not the HTML, because that is what carries the logo.</p>
        </div>
        <div class="cols">
          <div class="card"><h3>Gmail</h3><ol>
    {K.steps(K.GMAIL)}
          </ol></div>
          <div class="card"><h3>Apple Mail</h3><ol>
    {K.steps(K.APPLE)}
          </ol></div>
        </div>
        <div class="cols">
          {OUTLOOK}
          <div class="card"><h3>iPhone and iPad</h3><ol>
                <li>Open <strong>Settings &rarr; Apps &rarr; Mail &rarr; Signature</strong>.</li>
                <li>Phone signatures are plain text &mdash; no logo or blue rule is possible.</li>
                <li>Use four lines: your name, your job title, Dialogue Society, and
                <code>www.dialoguesociety.org</code>.</li>
          </ol></div>
        </div>
      </section>

      <section>
        <div class="head">
          <h2>Which one do I use?</h2>
          <p class="lede">The difference is who the mail is from, not how formal it is.</p>
        </div>
        <div class="cols">
    {WHICH_CARDS}
        </div>
      </section>

      <section>
        <div class="head">
          <h2>The house style</h2>
          <p class="lede">Every value in both forms, with its contrast against white. Brand
          blue stays on graphics only; text blue is the same hue darkened until it passes
          WCAG AA.</p>
        </div>
        <div class="tablewrap">
          <table class="spec">
            <thead><tr><th>Element</th><th>Type &mdash; Helvetica Neue</th><th>Colour</th><th>Contrast</th></tr></thead>
            <tbody>
    {SPEC_ROWS}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <div class="head"><h2>House rules</h2></div>
        <div class="tablewrap">
          <table class="spec">
            <thead><tr><th>Rule</th><th>Why</th></tr></thead>
            <tbody>
              <tr><th scope="row">Use this page, not a colleague&rsquo;s signature</th>
                <td>Editing someone else&rsquo;s copy is how the old house blue drifted to
                <code>#0797C8</code> when the brand blue is <code>#008AC4</code>.</td></tr>
              <tr><th scope="row">Write the address as your office registers it</th>
                <td>So post, the website and search results all agree.</td></tr>
              <tr><th scope="row">Type the region, not the whole name</th>
                <td>The region is appended to &ldquo;Dialogue Society&rdquo;. Typing the full
                name gives you &ldquo;Dialogue Society Dialogue Society Sheffield&rdquo;.</td></tr>
              <tr><th scope="row">Keep the charity line</th>
                <td>A registered charity must state its number on correspondence.</td></tr>
              <tr><th scope="row">Branch signatures name no one</th>
                <td>A shared inbox is answered by whoever is on duty. Putting one person on
                it makes replies look like they came from them.</td></tr>
              <tr><th scope="row">Nothing extra underneath</th>
                <td>Quotes, slogans and campaign banners sit outside the checked colour set
                and land in every reply chain you join.</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <footer>Dialogue Society &middot; 29 High Holborn, London WC1V 6AZ &middot;
      Registered Charity No. 1117039<br>
      <span style="font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;">
      Signature app {VLABEL}</span></footer>
    </div>'''

    APP_JS_BASE = TEMPLATE + K.COPY_JS + r'''
    /* ------------------------------------------------------------------ config
       The logo is embedded in each signature by default. That is deliberate: it
       removes every external dependency, so a signature can never lose its logo
       because a host lapsed or a file moved -- and Gmail and Apple Mail convert
       the embedded copy to their own hosted or attached image as you paste, so
       nothing extra travels with your mail anyway.

       Only set LOGO_URL if you would rather signatures link to a file. Use a
       permanent address on dialoguesociety.org -- never on whatever host this
       page sits on -- because the URL is baked into every signature made from
       here, and stays in mail already sent.                                     */
    var LOGO_URL = '';
    /* ----------------------------------------------------------------------- */

    (function(){
      var EMBEDDED = "''' + MARK_URI + r'''";
      var logo = EMBEDDED, raw = '', ready = false;
      var flash = mkFlash(document.getElementById('flash'));
      var sig = document.getElementById('sig'), warn = document.getElementById('warn');
      var KEYS = ['name','title','strap','branch','email','phone','address','social','charity'];
      var STORE = 'ds-signature-v1';

      function el(k){ return document.getElementById('i-'+k); }
      function val(k){ var e=el(k); return e.type==='checkbox' ? e.checked : e.value.trim(); }
      function set(k,v){ var e=el(k); if(e.type==='checkbox') e.checked=!!v; else e.value=v; }

      var radios = [].slice.call(document.querySelectorAll('input[name=lead]'));
      function lead(){
        for (var i=0;i<radios.length;i++) if (radios[i].checked) return radios[i].value;
        return 'person';
      }
      function setLead(v){
        radios.forEach(function(r){ r.checked = (r.value === (v === 'org' ? 'org' : 'person')); });
      }
      function applyMode(){
        var org = lead() === 'org';
        document.getElementById('g-person').hidden = org;
        document.getElementById('g-strap').hidden  = !org;
        document.getElementById('modehint').innerHTML = org
          ? 'For a shared branch address. No person is named \u2014 the branch leads.'
          : 'For one member of staff, with their name and job title.';
      }
      radios.forEach(function(r){
        r.addEventListener('change', function(){ applyMode(); render(); save(); });
      });

      /* ---- logo: embedded unless a permanent URL is configured -------------- */
      function resolveLogo(done){
        if (!LOGO_URL) return done('embedded');
        var probe = new Image();
        probe.onload  = function(){ logo = LOGO_URL; done('linked'); };
        probe.onerror = function(){ done('failed'); };
        probe.src = LOGO_URL;
      }

      /* ---- state ---------------------------------------------------------- */
      function save(){
        if (!ready) return;
        try {
          var d = { lead: lead() }; KEYS.forEach(function(k){ d[k] = val(k); });
          localStorage.setItem(STORE, JSON.stringify(d));
        } catch(e) {}
      }
      function load(){
        try {
          var d = JSON.parse(localStorage.getItem(STORE) || 'null');
          if (d) {
            KEYS.forEach(function(k){ if (k in d) set(k, d[k]); });
            if (d.lead) setLead(d.lead);
          }
          return !!d;
        } catch(e) { return false; }
      }
      function fromQuery(){
        var q, any = false;
        try { q = new URLSearchParams(location.search); } catch(e) { return false; }
        if (q.has('lead')) { setLead(q.get('lead')); any = true; }
        KEYS.forEach(function(k){
          if (!q.has(k)) return;
          var v = q.get(k);
          set(k, (k==='social'||k==='charity') ? v !== '0' : v);
          any = true;
        });
        return any;
      }
      function myLink(){
        var q = [];
        var org = lead() === 'org';
        if (org) q.push('lead=org');
        KEYS.forEach(function(k){
          if (org  && (k==='name' || k==='title')) return;   /* not used in this mode */
          if (!org && k==='strap') return;
          var v = val(k);
          if (k==='social'||k==='charity') { if (!v) q.push(k+'=0'); return; }
          if (v) q.push(k+'='+encodeURIComponent(v));
        });
        return location.origin + location.pathname + (q.length ? '?'+q.join('&') : '');
      }

      /* ---- render --------------------------------------------------------- */
      function render(){
        var branch = val('branch'),
            trimmed = branch.replace(/^\s*dialogue\s+society\s*/i,''),
            stripped = trimmed !== branch;
        var org = lead() === 'org';
        raw = DS.build({ lead: org ? 'org' : 'person',
                         name: val('name') || 'Your Name', title: val('title'),
                         strap: val('strap'), branch: trimmed,
                         email: val('email'), phone: val('phone'),
                         address: val('address'), socials: val('social'),
                         charity: val('charity'), logo: logo });
        sig.innerHTML = raw;
        var m = [];
        if (!org && !val('name')) m.push('Add your name.');
        if (!val('email')) m.push('Add your email address.');
        else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val('email'))) m.push('That email address looks incomplete.');
        else if (!/@dialoguesociety\.org$/i.test(val('email'))) m.push('That is not a dialoguesociety.org address.');
        if (org && !val('branch')) m.push('No region set, so this reads as the head office signature.');
        if (org && val('strap').length > 45)
          m.push('That second line is ' + val('strap').length + ' characters, so it will wrap '
                 + 'onto two lines. Around 45 keeps it on one.');
        if (!val('address')) m.push('Add your office address.');
        if (!val('charity')) m.push('The charity registration line is switched off.');
        if (stripped) m.push('Dropped &ldquo;Dialogue Society&rdquo; from the region box &mdash; it is already on that line.');
        warn.innerHTML = m.join('<br>');
        warn.className = m.length ? 'warnbox on' : 'warnbox';
      }

      /* ---- wire up -------------------------------------------------------- */
      KEYS.forEach(function(k){
        var e = el(k);
        e.addEventListener('input',  function(){ render(); save(); });
        e.addEventListener('change', function(){ render(); save(); });
      });
      document.getElementById('f').addEventListener('submit', function(e){ e.preventDefault(); });
      document.getElementById('copy').addEventListener('click', function(){ copyNode(sig, flash); });
      document.getElementById('mylink').addEventListener('click', function(){
        var u = myLink();
        document.getElementById('linkurl').textContent = u;
        document.getElementById('linkout').className = 'linkout on';
        copyText(u, function(){ flash('Your link is copied.'); });
      });
      /*<<<DL*/
      var dlBtn = document.getElementById('dl');
      if (dlBtn) dlBtn.addEventListener('click', function(){
        var name = (lead() === 'org'
                     ? ('Dialogue-Society-' + (val('branch') || 'Head-Office'))
                     : (val('name') || 'signature')).replace(/[^A-Za-z0-9]+/g,'-');
        var doc = '<!doctype html><html><head><meta charset="utf-8">'
                + '<title>' + name + '</title></head><body>' + raw + '</body></html>';
        try {
          var url = URL.createObjectURL(new Blob([doc], {type:'text/html'}));
          var a = document.createElement('a');
          a.href = url; a.download = (/^Dialogue/.test(name) ? name : 'Dialogue-Society-' + name) + '.htm';
          document.body.appendChild(a); a.click(); a.remove();
          setTimeout(function(){ URL.revokeObjectURL(url); }, 4000);
          flash('Downloaded. Move it into your Outlook Signatures folder.');
        } catch(e) { flash('Download blocked \u2014 use Copy signature instead.', 1); }
      });
      /*DL>>>*/
      document.getElementById('forget').addEventListener('click', function(){
        try { localStorage.removeItem(STORE); } catch(e) {}
        flash('Saved details cleared. They will come back if you keep typing.');
      });

      /* ---- boot ----------------------------------------------------------- */
      load();
      fromQuery();                             /* a shared link wins over saved state */
      applyMode();
      ready = true;
      render();
      resolveLogo(function(state){
        var dot = document.getElementById('dot'), txt = document.getElementById('modetxt');
        if (state === 'linked') {
          dot.className = 'dot';
          txt.textContent = 'logo linked from dialoguesociety.org';
        } else if (state === 'failed') {
          dot.className = 'dot embed';
          txt.textContent = 'LOGO_URL is set but will not load \u2014 embedded copy used instead';
        } else {
          dot.className = 'dot';
          txt.textContent = 'logo embedded \u2014 no external dependency';
        }
        render();
      });
    })();
    '''


    APP_JS_HOSTED  = APP_JS_BASE.replace('/*<<<DL*/', '').replace('/*DL>>>*/', '')
    # the artifact viewer never grants download permission, so the preview
    # ships without any download code at all rather than a dead button
    APP_JS_PREVIEW = _re.sub(r'/\*<<<DL\*/.*?/\*DL>>>\*/', '', APP_JS_BASE, flags=_re.S)
    assert 'a.download' in APP_JS_HOSTED and 'a.download' not in APP_JS_PREVIEW

    TITLE = 'Dialogue Society Signatures'
    DESC  = ('Build your Dialogue Society email signature -- personal or branch -- and '
             'paste it straight into Gmail, Apple Mail or Outlook.')

    def page(body_html, js):
        return ('<!doctype html>\n<html lang="en-GB">\n<head>\n'
                + K.head(TITLE, DESC, MARK_URI, APP_CSS)
                + '\n</head>\n<body>\n' + body_html + '\n<script>' + js + '</script>\n'
                '</body>\n</html>')

    def artifact(body_html, js):
        return ('<title>' + TITLE + '</title>\n' + K.FONTS + '\n<style>'
                + K.CSS + APP_CSS + '</style>\n' + body_html + '\n<script>' + js + '</script>')

    return (page(make_body(True), APP_JS_HOSTED),
            artifact(make_body(False), APP_JS_PREVIEW))


def readme(VERSION):
        return ('DIALOGUE SOCIETY - STAFF EMAIL SIGNATURE APP\n=============================================\nVersion {V}\n\nThree pages -- the signature maker plus a finished personal and branch\nsignature -- with no backend, no database and no build step. They run on any\nstatic web host.\n\n   index.html      the signature maker\n   personal.html   a finished personal signature\n   branch.html     a finished branch signature\n   ds-mark.png     the logo, if you ever want to link it instead of embedding\n\nThey link to each other by relative name, so keep them in the same folder.\n\n\nCHECKING WHICH VERSION IS LIVE  -  READ THIS FIRST\n--------------------------------------------------\nThe bottom of the page shows a version, e.g. "Signature app {V}".\n\nAfter deploying, open your address and look at it. If it does not say {V},\nthen either an older file was uploaded or your browser is showing a cached\ncopy. Reload with Cmd+Shift+R (Ctrl+Shift+R on Windows).\n\nQuick way to tell by eye:\n   {V} - the logo sits to the LEFT of the text.   <- correct\n   v5   - the logo sits ABOVE the text.            <- wrong file deployed\n\nDownloaded zips all used to share one filename, so it was easy to upload an\nolder one by mistake. They are numbered now. Check the number matches.\n\n\nDEPLOYING TO CLOUDFLARE PAGES\n-----------------------------\n1. dash.cloudflare.com -> Workers & Pages -> your project -> Create deployment.\n2. Upload the zip as it is, or drag in all of the files. index.html must end\n   up at the TOP level, not inside a folder, or the app lands at a subpath\n   and the links between the three pages break.\n3. Deploy, then open the address and check the version in the footer.\n4. Cloudflare keeps the previous deployment, so you can roll back from the\n   Deployments tab if anything looks wrong.\n\nFirst time: Workers & Pages -> Create -> Pages -> Upload assets, name the\nproject (e.g. dialogue-signatures), upload, Deploy. You get\nhttps://dialogue-signatures.pages.dev\n\nNetlify Drop (app.netlify.com/drop) works the same way - the archive root\nbecomes the site root.\n\n\nDEPLOYING TO GITHUB PAGES\n-------------------------\nThe repository already carries a built copy of these files in docs/, so there\nis nothing to upload. In the repository, open Settings -> Pages, set Source to\n"Deploy from a branch", pick the main branch and the /docs folder, and Save.\n\nTo publish a change: edit the source, run\n\n    python3 build.py\n\nwhich rewrites docs/, then commit and push. Pages redeploys on its own.\n\n\nUSING YOUR OWN DOMAIN\n---------------------\nAll of these support a custom domain, so signatures.dialoguesociety.org can\npoint at it later without changing the address staff have bookmarked.\n\n\nABOUT THE LOGO\n--------------\nThe logo is embedded inside each signature by default. That is deliberate: a\nsignature then has no external dependency and cannot lose its logo because a\nhost lapsed or a file moved. Gmail re-hosts the image on its own servers as\nstaff paste, and Apple Mail attaches it, so nothing extra travels with mail.\n\nTo link it instead, upload ds-mark.png somewhere permanent on\ndialoguesociety.org, then open index.html, find\n\n    var LOGO_URL = \'\';\n\nand put the address between the quotes. Use an address on dialoguesociety.org,\nnever on the host serving this page - the URL is written into every signature\nmade here and stays in mail already sent. The status line under the preview\nsays which mode is active and warns if a configured URL will not load.\n\n\nWHAT STAFF DO\n-------------\nOpen the address, choose Personal or Branch, fill in their details, press Copy\nsignature, and follow the instructions on the page for Gmail, Apple Mail,\nOutlook or iPhone. Nothing is sent anywhere - the page works entirely in their\nbrowser and what they type is saved only on their own machine.\n\n\nHOUSE STYLE\n-----------\nBrand blue    #008AC4   logo and the vertical rule only\nText blue     #007AAD   links, organisation line, branch lead line\nBrand grey    #424242   name, contact values, address\nSoft grey     #6E6E6E   job title, second line, charity line\nTypeface      Helvetica Neue, falling back to Helvetica then Arial\n\nThe blue in the older signatures was #0797C8. It does not match the logo and\nfails the WCAG AA contrast standard for body text. Do not reintroduce it.\n'.replace('{V}', VERSION))
