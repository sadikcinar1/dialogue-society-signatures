"""Shared look and behaviour for every page in this project.

Nothing here touches the signature markup itself -- that lives in
src/template.js and must stay independent of how these pages look.
"""

CSS = r'''
:root{
  --ground:#F5F7F9; --surface:#FFFFFF; --sunken:#EBEFF3;
  --ink:#242A30; --soft:#565F67; --faint:#7C868E;
  --line:#DCE1E6; --hair:#E9EDF1;
  --blue:#007AAD; --brand:#008AC4; --onblue:#FFFFFF;
  --paper:#FFFFFF; --lift:16px 34px 64px -34px rgba(24,40,52,.28);
  --warn:#A75B0C; --ok:#1B7A4B;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#12181D; --surface:#1A2228; --sunken:#151D23;
    --ink:#E6EBEF; --soft:#A7B2BA; --faint:#7F8B93;
    --line:#2A343B; --hair:#212A31;
    --blue:#4FBDE4; --brand:#3FB2DC; --onblue:#06242F;
    --paper:#FFFFFF; --lift:16px 34px 64px -34px rgba(0,0,0,.66);
    --warn:#E0A254; --ok:#5FC08C;
  }
}
:root[data-theme="dark"]{
  --ground:#12181D; --surface:#1A2228; --sunken:#151D23;
  --ink:#E6EBEF; --soft:#A7B2BA; --faint:#7F8B93;
  --line:#2A343B; --hair:#212A31;
  --blue:#4FBDE4; --brand:#3FB2DC; --onblue:#06242F;
  --paper:#FFFFFF; --lift:16px 34px 64px -34px rgba(0,0,0,.66);
  --warn:#E0A254; --ok:#5FC08C;
}
*{box-sizing:border-box}
html{color-scheme:light dark}
body{margin:0; background:var(--ground); color:var(--ink);
  font-family:'IBM Plex Sans','Helvetica Neue',Helvetica,Arial,sans-serif;
  font-size:15.5px; line-height:1.62; -webkit-font-smoothing:antialiased}
.wrap{max-width:920px; margin:0 auto; padding:56px 26px 92px;
  display:flex; flex-direction:column; gap:44px}
@media(max-width:640px){.wrap{padding:30px 17px 60px; gap:34px}}

.mast{display:flex; gap:22px; align-items:flex-start;
  padding-bottom:26px; border-bottom:1px solid var(--line)}
/* 118 x 38.3 is the file's own 354 x 115 at a third. Pinning height to 39px
   stretched the wordmark by ~2%; aspect-ratio holds it and still reserves the
   box before the image lands. */
.mast .logo{width:118px; height:auto; aspect-ratio:354/115; flex:none; margin-top:9px;
  display:block}
h1{font-family:Newsreader,Georgia,'Times New Roman',serif; font-weight:500;
  font-size:38px; line-height:1.09; letter-spacing:-.014em; margin:0 0 8px;
  text-wrap:balance}
@media(max-width:640px){h1{font-size:28px} .mast{gap:16px} .mast .logo{width:92px}}
.mast p{margin:0; color:var(--soft); max-width:56ch}


section{display:flex; flex-direction:column; gap:17px}
h2{font-family:Newsreader,Georgia,'Times New Roman',serif; font-weight:500;
  font-size:25px; letter-spacing:-.01em; margin:0; text-wrap:balance}
.head{display:flex; flex-direction:column; gap:5px}
.lede{margin:0; color:var(--soft); max-width:66ch}
.eyebrow{font-size:11px; font-weight:600; letter-spacing:.15em;
  text-transform:uppercase; color:var(--blue); margin:0}

.stage{background:var(--paper); border:1px solid var(--line); border-radius:3px;
  box-shadow:var(--lift); padding:30px; overflow-x:auto; min-width:0}
@media(max-width:640px){
  .stage{padding:18px 15px}
  /* The signature is 378px wide and a phone is not, so .stage scrolls. Without
     a cue the row just looks cut off. The fading edge is painted with
     background-attachment:local, so it travels with the content and clears
     itself once you have reached the end. */
  .stage{background:
    linear-gradient(to left, var(--paper), rgba(255,255,255,0)) right/36px 100% no-repeat local,
    radial-gradient(farthest-side at 100% 50%, rgba(36,42,48,.17), rgba(36,42,48,0))
      right/13px 100% no-repeat scroll,
    var(--paper)}
}
/* hold the preview at the signature's true width; .stage scrolls when narrower.
   This sits on the wrapper, never on the table, so the copied markup stays clean. */
#sig{min-width:390px}
.stage-cap{display:flex; justify-content:space-between; align-items:baseline;
  gap:14px; margin-bottom:16px; padding-bottom:11px;
  border-bottom:1px dashed #E4E9ED; font-size:10.5px; font-weight:600;
  letter-spacing:.13em; text-transform:uppercase; color:#8B959C}
.stage-cap b{font-weight:400; letter-spacing:.02em; text-transform:none;
  font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:11px; white-space:nowrap}

.actions{display:flex; flex-wrap:wrap; gap:13px; align-items:center}
button{font-family:inherit; font-size:14.5px; font-weight:600; cursor:pointer;
  border-radius:2px; padding:11px 21px; border:1px solid transparent;
  transition:background .15s, border-color .15s, color .15s}
button:focus-visible{outline:2px solid var(--blue); outline-offset:2px}
.primary{background:var(--blue); color:var(--onblue)}
.primary:hover{filter:brightness(1.12)}
.ghost{background:transparent; color:var(--ink); border-color:var(--line)}
.ghost:hover{border-color:var(--blue); color:var(--blue)}
.flash{font-size:14px; font-weight:600; color:var(--blue); opacity:0;
  transition:opacity .18s}
.flash.on{opacity:1}
.flash.warn{color:var(--warn)}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}

.cols{display:grid; grid-template-columns:1fr 1fr; gap:21px}
.cols>*{min-width:0}
@media(max-width:730px){.cols{grid-template-columns:1fr}}
.card{background:var(--surface); border:1px solid var(--line);
  border-radius:3px; padding:23px}
.card h3{margin:0 0 14px; font-size:16.5px; font-weight:600;
  display:flex; align-items:center; gap:10px}
.card h3::before{content:''; width:7px; height:7px; border-radius:50%;
  background:var(--brand); flex:none}
ol{margin:0; padding:0; list-style:none; counter-reset:s;
  display:flex; flex-direction:column; gap:10px}
ol li{counter-increment:s; position:relative; padding-left:32px;
  font-size:14.5px; line-height:1.54; color:var(--soft)}
ol li::before{content:counter(s); position:absolute; left:0; top:1px;
  width:22px; height:22px; border-radius:50%; background:var(--sunken);
  color:var(--ink); font-size:11.5px; font-weight:600; line-height:22px;
  text-align:center; font-variant-numeric:tabular-nums}
strong{color:var(--ink); font-weight:600}

.note{border-left:3px solid var(--brand); background:var(--surface);
  padding:15px 19px; font-size:14.5px; color:var(--soft)}
.note strong{color:var(--ink)}

.tablewrap{overflow-x:auto; border:1px solid var(--line); border-radius:3px;
  background:var(--surface)}
table.spec{border-collapse:collapse; width:100%; min-width:640px; font-size:13.5px}
table.spec th, table.spec td{text-align:left; padding:11px 16px;
  border-bottom:1px solid var(--hair); vertical-align:middle}
table.spec tbody tr:last-child th, table.spec tbody tr:last-child td{border-bottom:0}
table.spec thead th{font-size:10.5px; letter-spacing:.13em; text-transform:uppercase;
  color:var(--faint); font-weight:600; background:var(--sunken)}
table.spec th[scope=row]{font-weight:600; color:var(--ink); white-space:nowrap}
table.spec td{color:var(--soft)}
table.spec td.num{font-variant-numeric:tabular-nums;
  font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:12.5px}
.pass{color:var(--ok); font-weight:600}
.sw{white-space:nowrap}
.sw span{display:inline-block; width:12px; height:12px; border-radius:2px;
  margin-right:9px; vertical-align:-1px; border:1px solid rgba(120,132,142,.45)}
.sw code{font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:12px; color:var(--ink)}
.sw em{color:var(--faint); font-style:normal; font-size:12px; margin-left:7px}

details{border:1px solid var(--line); border-radius:3px; background:var(--surface)}
summary{cursor:pointer; padding:14px 19px; font-weight:600; font-size:14.5px;
  list-style:none; display:flex; justify-content:space-between; align-items:center; gap:12px}
summary::-webkit-details-marker{display:none}
summary em{font-style:normal; font-weight:400; font-size:12px; color:var(--faint);
  font-family:'IBM Plex Mono',ui-monospace,monospace}
summary::after{content:'+'; color:var(--blue); font-weight:600; font-size:17px; line-height:1}
details[open] summary::after{content:'\2212'}
summary:focus-visible{outline:2px solid var(--blue); outline-offset:-2px}
.codebody{padding:0 19px 19px; display:flex; flex-direction:column; gap:13px;
  align-items:flex-start}
pre{margin:0; width:100%; background:var(--sunken); border:1px solid var(--hair);
  border-radius:2px; padding:15px; overflow:auto; max-height:320px;
  font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:11.5px;
  line-height:1.62; color:var(--ink)}
code{font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:.92em;
  overflow-wrap:anywhere}   /* long paths like %appdata%\Microsoft\Signatures */
ol li{min-width:0}
footer{border-top:1px solid var(--line); padding-top:21px; font-size:13px;
  color:var(--faint)}

'''

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Newsreader:opsz,wght@6..72,400;6..72,500'
         '&family=IBM+Plex+Sans:wght@400;600'
         '&family=IBM+Plex+Mono:wght@400&display=swap">')

COPY_JS = r'''
function mkFlash(el){
  return function(msg,warn){
    el.textContent=msg; el.className='flash on'+(warn?' warn':'');
    clearTimeout(el._t); el._t=setTimeout(function(){el.className='flash';},4600);
  };
}
/* Hand the clipboard a complete HTML document, not a selection fragment.

   Apple Mail turns the data-URI logo into a cid: attachment as it pastes, and
   an attachment cannot sit inside a table cell -- so Mail cuts the markup at
   the image and re-opens the document from there. Against a fragment that seam
   lands mid-table: the logo cell is emptied to <tr></td></tr>, the image is
   hoisted out above everything else, and the table is re-emitted carrying only
   the text cell. That is the logo-above-the-text bug, and it is nothing to do
   with the narrow-pane reflow below -- it happens at any pane width.

   document.execCommand('copy') is what produces that fragment, and Safari
   prefixes it with a stray <head><meta charset>. A <head> is invalid inside a
   fragment, and it is exactly where Mail re-opened the document. A well-formed
   <head></head><body> document gives it no such seam and the <img> stays in its
   cell -- which is why the same signature pasted correctly before and split
   afterwards. Writing the document ourselves also keeps the page's computed
   styles -- IBM Plex Sans, caret-color, box-sizing on every node -- from being
   baked into the signature, which is what selection copying does.

   execCommand stays as the fallback for browsers with no ClipboardItem.        */
function sigDocument(html){
  return '<!DOCTYPE html><html><head><meta charset="utf-8"></head>' +
         '<body dir="auto">' + html + '</body></html>';
}
function copyNode(node,flash){
  function done(){ flash('Copied. Now paste it into your mail client.'); }
  function manual(){ flash('Select the signature above and press \u2318C.',1); }
  function legacy(){
    var sel=window.getSelection(), r=document.createRange(), ok=false;
    sel.removeAllRanges(); r.selectNodeContents(node); sel.addRange(r);
    try{ ok=document.execCommand('copy'); }catch(e){ ok=false; }
    sel.removeAllRanges();
    ok?done():manual();
  }
  if(navigator.clipboard && window.ClipboardItem){
    try{
      navigator.clipboard.write([new ClipboardItem({
        'text/html': new Blob([sigDocument(node.innerHTML)],{type:'text/html'}),
        'text/plain': new Blob([node.innerText],{type:'text/plain'})
      })]).then(done, legacy);
      return;
    }catch(e){}
  }
  legacy();
}
function copyText(t,flash){
  function ok(){ flash('HTML source copied.'); }
  function legacy(){
    var ta=document.createElement('textarea'); ta.value=t;
    ta.style.position='fixed'; ta.style.top='-1000px'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    var d=false; try{ d=document.execCommand('copy'); }catch(e){}
    document.body.removeChild(ta);
    d?ok():flash('Select the code and press \u2318C.',1);
  }
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(t).then(ok, legacy);
  } else legacy();
}
'''


GMAIL = [
    'Press <strong>Copy signature</strong> above.',
    'In Gmail, open the gear icon &rarr; <strong>See all settings</strong>.',
    'On the <strong>General</strong> tab, scroll to <strong>Signature</strong> and press '
    '<strong>Create new</strong>.',
    'Click into the editing box and paste with <strong>&#8984;V</strong>.',
    'Under <strong>Signature defaults</strong>, select it for new emails and for '
    'replies&#8202;/&#8202;forwards.',
    'Press <strong>Save Changes</strong> at the bottom of the page.',
]
APPLE = [
    'Press <strong>Copy signature</strong> above.',
    'In Mail, open <strong>Mail &rarr; Settings &rarr; Signatures</strong>.',
    'Select your account, press <strong>+</strong>, and name it <em>Dialogue Society</em>.',
    'Untick <strong>Always match my default message font</strong>. Skip this and Mail '
    'strips the styling out.',
    'Drag the Settings window wider if it is narrow &mdash; the signature pane grows '
    'with it, and a pane narrower than the signature squeezes the text column until '
    'the social row wraps.',
    'Click into the right-hand pane and paste with <strong>&#8984;V</strong>.',
    'If the logo lands above the text instead of beside it, undo with '
    '<strong>&#8984;Z</strong>, click into the pane again and paste once more. Mail '
    'occasionally converts the logo to an attachment as it pastes, and an attachment '
    'cannot stay inside the layout.',
    'Set <strong>Choose Signature</strong> to it so it is added automatically.',
]
def lockup(light, dark):
    """The masthead lockup, swapping to a light wordmark on a dark page.

    The wordmark is black. On the dark palette it drops to roughly 1.5:1
    against the page and is effectively unreadable, so a second file carries
    the same lockup with the letters lifted to --ink.
    """
    return ('<picture>'
            '<source srcset="%s" media="(prefers-color-scheme: dark)">'
            '<img class="logo" src="%s" alt="Dialogue Society" width="354" height="115">'
            '</picture>') % (dark, light)


def head(title, description, icon, extra_css=''):
    """Everything between <head> and </head>, shared by all three pages."""
    return ('<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            # The site is public -- GitHub Pages has no access control on a free
            # plan -- but it is for staff, and personal.html carries a name, a job
            # title and a work address. Keep it out of search results.
            #
            # This meta is what does the work. robots.txt sits at the archive root
            # for a deploy that owns its domain, but a crawler only reads
            # robots.txt at the domain root, and this is a project page under
            # sadikcinar1.github.io/<repo>/ -- so on Pages the file is ignored and
            # the meta is the whole mechanism.
            '<meta name="robots" content="noindex, nofollow">\n'
            '<title>' + title + '</title>\n'
            '<meta name="description" content="' + description + '">\n'
            '<meta name="theme-color" content="#008AC4">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="' + title + '">\n'
            '<meta property="og:description" content="' + description + '">\n'
            '<link rel="icon" href="' + icon + '">\n'
            + FONTS + '\n<style>' + CSS + extra_css + '</style>')


def steps(items):
    """Render a list of instruction strings as <li> rows."""
    return '\n'.join('            <li>%s</li>' % s for s in items)
