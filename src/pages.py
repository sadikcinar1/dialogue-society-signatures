"""The two finished signature pages -- no form to fill in.

  personal.html  a named member of staff
  branch.html    the organisation, for shared inboxes

Both render their signature through src/template.js like everything else, so
they can never drift from what the app produces.
"""


def build(VERSION, VLABEL, MARK, LOCKUP, LOCKUP_DARK, render, theme):
    K = theme
    import html as _html

    SIG_PERSONAL = render(
        lead='person', name='Sadik Cinar', title='Executive Director', branch='',
        email='scinar@dialoguesociety.org', phone='',
        address='29 High Holborn, London WC1V 6AZ',
        socials=True, charity=True, logo=MARK)

    SIG_BRANCH = render(
        lead='org', branch='', strap='Building Community Trust',
        email='info@dialoguesociety.org', phone='',
        address='29 High Holborn, London WC1V 6AZ',
        socials=True, charity=True, logo=MARK)

    SIG_REGION = render(
        lead='org', branch='Birmingham', strap='',
        email='birmingham@dialoguesociety.org', phone='0121 000 0000',
        address='55 Colmore Row, Birmingham B3 2AA',
        socials=True, charity=True, logo=MARK)

    HOSTED = 'https://www.dialoguesociety.org/wp-content/uploads/ds-mark.png'

    OUTLOOK = [
        'Press <strong>Copy signature</strong> above.',
        'In Outlook, open <strong>File &rarr; Options &rarr; Mail &rarr; Signatures</strong>.',
        'Press <strong>New</strong> and name it <em>Dialogue Society</em>.',
        'Click into the edit box and paste with <strong>Ctrl&nbsp;+&nbsp;V</strong>.',
        'Set it as the default for new messages and for replies.',
    ]
    IPHONE = [
        'Open <strong>Settings &rarr; Apps &rarr; Mail &rarr; Signature</strong>.',
        'Phone signatures are plain text, so no logo or blue rule is possible.',
        'Use three lines: your name or Dialogue Society, your role or motto, and '
        '<code>www.dialoguesociety.org</code>.',
    ]

    def page(title, lede, sig, desc, extra=''):
        src_hosted = sig.replace(MARK, HOSTED)
        return f'''<!doctype html>
<html lang="en-GB">
<head>
{K.head(title, desc, MARK)}
</head>
<body>
<div class="wrap">
  <header class="mast">
    {K.lockup(LOCKUP, LOCKUP_DARK)}
    <div>
      <h1>{title}</h1>
      <p>{lede}</p>
    </div>
  </header>

  <section>
    <p class="eyebrow">Ready to copy</p>
    <div class="stage">
      <div class="stage-cap"><span>Preview at actual size</span><b>{VLABEL}</b></div>
      <div id="sig">{sig}</div>
    </div>
    <div class="actions">
      <button class="primary" id="copy" type="button">Copy signature</button>
      <span class="flash" id="flash" role="status" aria-live="polite"></span>
    </div>
    <p class="note"><strong>Copy the preview, not the code.</strong> Copying the
    rendered signature is what carries the logo across: Gmail re-hosts the image on
    its own servers as you paste, and Apple Mail embeds it.</p>
    <p class="note"><strong>These are not your details.</strong> This page is fixed.
    For your own name, title, region or address, use the
    <a href="index.html" style="color:var(--blue)">signature maker</a>.</p>
  </section>
{extra}
  <section>
    <div class="head">
      <h2>Setting it up</h2>
      <p class="lede">Once per mail client.</p>
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
      <div class="card"><h3>Outlook on Windows</h3><ol>
{K.steps(OUTLOOK)}
      </ol></div>
      <div class="card"><h3>iPhone and iPad</h3><ol>
{K.steps(IPHONE)}
      </ol></div>
    </div>
  </section>

  <section>
    <div class="head">
      <h2>The HTML, if you need it</h2>
      <p class="lede">This version links the logo instead of embedding it, for a
      mail-server template. Upload <code>ds-mark.png</code> somewhere permanent on
      dialoguesociety.org and swap the <code>src</code> for that address.</p>
    </div>
    <details>
      <summary>Signature HTML <em>hosted logo</em></summary>
      <div class="codebody">
        <pre><code id="srccode">{_html.escape(src_hosted)}</code></pre>
        <button class="ghost" id="srcbtn" type="button">Copy HTML source</button>
      </div>
    </details>
  </section>

  <footer>Dialogue Society &middot; 29 High Holborn, London WC1V 6AZ &middot;
  Registered Charity No. 1117039<br>
  <span style="font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;">
  Signature {VLABEL}</span></footer>
</div>
<script>{K.COPY_JS}
(function(){{
  var flash = mkFlash(document.getElementById('flash'));
  document.getElementById('copy').addEventListener('click', function(){{
    copyNode(document.getElementById('sig'), flash);
  }});
  var b = document.getElementById('srcbtn');
  if (b) b.addEventListener('click', function(){{
    copyText(document.getElementById('srccode').textContent, flash);
  }});
}})();
</script>
</body>
</html>'''

    region_extra = f'''
  <section>
    <div class="head">
      <h2>A regional branch</h2>
      <p class="lede">Type the region into the app and it is appended to the name.
      Birmingham below as an example &mdash; the phone number is a placeholder.</p>
    </div>
    <div class="stage">
      <div class="stage-cap"><span>Example &mdash; not for use</span><b>placeholder details</b></div>
      <div style="min-width:390px">{SIG_REGION}</div>
    </div>
  </section>
'''

    return {
        'personal.html': page(
            'Sadik Cinar &mdash; email signature',
            'Your personal signature. Copy it and paste it into your mail client.',
            SIG_PERSONAL,
            'A finished Dialogue Society personal email signature, ready to copy into '
            'Gmail, Apple Mail or Outlook.'),
        'branch.html': page(
            'The branch signature',
            'For mail sent as the organisation rather than as a person. No one is '
            'named, so the organisation leads.',
            SIG_BRANCH,
            'The Dialogue Society branch email signature, for shared inboxes, '
            'newsletters and regional branches.',
            region_extra),
    }
