/* Dialogue Society email signature -- single source of truth.
   Outlook-hardened: table cells only, bgcolor for the rule, mso-line-height-rule
   on every line box, explicit width/height on images, no letter-spacing reliance.

   Palette
     #008AC4  brand blue    graphics only (rule, logo) -- 3.87:1
     #007AAD  text blue     links and branch line      -- 4.79:1  AA
     #424242  brand grey    name, values, address      -- 10.05:1 AA
     #6E6E6E  soft grey     job title, charity line    -- 5.10:1  AA
     #DCDCDC  hairline
*/
var DS = (function () {
  var BLUE = '#008AC4', TXTBLUE = '#007AAD',
      GREY = '#424242', SOFT = '#6E6E6E', HAIR = '#DCDCDC',
      FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";

  var SOCIALS = [
    ['LinkedIn',  'https://www.linkedin.com/company/21820638'],
    ['Instagram', 'https://www.instagram.com/dialoguesociety'],
    ['Facebook',  'https://www.facebook.com/DialogueSociety'],
    ['X',         'https://x.com/DialogueSociety'],
    ['YouTube',   'https://www.youtube.com/@DialogueSociety']
  ];

  var LH = 'mso-line-height-rule:exactly;';

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function row(label, value, top) {
    return '<tr>' +
      '<td style="padding:' + top + 'px 11px 0 0;font-family:' + FONT +
        ';font-size:10px;font-weight:700;color:' + GREY + ';line-height:15px;' + LH +
        'white-space:nowrap;vertical-align:top;">' + label + '</td>' +
      '<td style="padding:' + top + 'px 0 0 0;font-family:' + FONT +
        ';font-size:11.5px;color:' + GREY + ';line-height:15px;' + LH +
        'vertical-align:top;">' + value + '</td></tr>';
  }

  function link(href, text, weight) {
    return '<a href="' + esc(href) + '" style="color:' + TXTBLUE +
      ';text-decoration:none;' + (weight ? 'font-weight:700;' : '') + '">' +
      esc(text) + '</a>';
  }

  /* d = {lead, name, title, branch, strap, email, phone, address, logo,
          socials:bool, charity:bool}

     lead:'org' is a branch signature -- no person, so the organisation becomes
     the top line at the size the name would have taken. Anything else is a
     personal signature: name leads, organisation sits under it.                */
  function build(d) {
    var lines = [], pad;
    var org = 'Dialogue Society' + (d.branch ? ' ' + d.branch : '');

    if (d.lead === 'org') {
      lines.push('<tr><td style="padding:0;font-family:' + FONT +
        ';font-size:15px;font-weight:700;color:' + TXTBLUE + ';line-height:20px;' + LH +
        '">' + esc(org) + '</td></tr>');
      if (d.strap) lines.push('<tr><td style="padding:3px 0 0 0;font-family:' + FONT +
        ';font-size:11.5px;color:' + SOFT + ';line-height:15px;' + LH + '">' +
        esc(d.strap) + '</td></tr>');
    } else {
      lines.push('<tr><td style="padding:0;font-family:' + FONT +
        ';font-size:15px;font-weight:700;color:' + GREY + ';line-height:19px;' + LH +
        'text-transform:uppercase;">' + esc(d.name) + '</td></tr>');
      if (d.title) lines.push('<tr><td style="padding:3px 0 0 0;font-family:' + FONT +
        ';font-size:11.5px;color:' + SOFT + ';line-height:15px;' + LH + '">' +
        esc(d.title) + '</td></tr>');
      lines.push('<tr><td style="padding:10px 0 0 0;font-family:' + FONT +
        ';font-size:13px;font-weight:700;color:' + TXTBLUE + ';line-height:17px;' + LH + '">' +
        esc(org) + '</td></tr>');
    }

    /* contact block */
    var fields = '', first = true;
    if (d.phone) { fields += row('T&nbsp;/&nbsp;WA', esc(d.phone), 0); first = false; }
    if (d.email) { fields += row('E', link('mailto:' + d.email, d.email), first ? 0 : 4); first = false; }
    fields += row('W', link('https://www.dialoguesociety.org', 'www.dialoguesociety.org'), first ? 0 : 4);
    pad = (d.lead === 'org') ? 12 : 11;
    lines.push('<tr><td style="padding:' + pad + 'px 0 0 0;">' +
      '<table cellpadding="0" cellspacing="0" border="0" role="presentation" ' +
      'style="border-collapse:collapse;border-spacing:0;">' + fields + '</table></td></tr>');

    if (d.address) lines.push('<tr><td style="padding:11px 0 0 0;font-family:' + FONT +
      ';font-size:11.5px;color:' + GREY + ';line-height:15px;' + LH + '">' +
      esc(d.address) + '</td></tr>');

    if (d.socials) {
      var sep = '<span style="color:#9A9A9A;font-weight:400;">&nbsp;&#8201;&#8226;&#8201;&nbsp;</span>';
      var s = SOCIALS.map(function (x) { return link(x[1], x[0], true); }).join(sep);
      lines.push('<tr><td style="padding:12px 0 0 0;font-family:' + FONT +
        ';font-size:11px;line-height:15px;' + LH + '">' + s + '</td></tr>');
    }

    if (d.charity) {
      /* The divider is a border on this cell, not a thin cell filled with colour.
         A filled cell has to hold a &nbsp; to keep its height, and if a client
         strips the 1px font-size -- as Apple Mail does -- that space inflates to
         the inherited size and the hairline renders as a thick grey bar. A border
         has no content, so nothing can inflate it.                                */
      if (lines.length) {
        var last = lines.length - 1;
        lines[last] = lines[last]
          .replace(/padding:(\d+)px 0 0 0;/, 'padding:$1px 0 12px 0;')
          .replace(/style="padding:0;/, 'style="padding:0 0 12px 0;');
      }
      lines.push('<tr><td style="border-top:1px solid ' + HAIR +
        ';padding:9px 0 0 0;font-family:' + FONT +
        ';font-size:10px;color:' + SOFT + ';line-height:14px;' + LH + '">' +
        'Registered Charity No. 1117039</td></tr>');
    }

    var img = '<img src="' + d.logo + '" width="70" height="75" alt="Dialogue Society" ' +
      'style="display:block;width:70px;height:75px;max-width:70px;border:0;outline:none;' +
      'text-decoration:none;font-family:' + FONT + ';font-size:12px;font-weight:700;color:' +
      GREY + ';">';

    if (d.layout !== 'stacked') {
      /* Side by side -- the default. Logo left, blue rule, text right.

         Two cells, not three: the rule is a left border on the text cell rather
         than a cell of its own. That matters because Apple Mail strips widths and
         font sizes but leaves borders alone, so the old 4px filled cell could be
         squeezed to nothing while a border cannot. Fewer cells in the row also
         means less for a narrow signature pane to push around.                    */
      return '' +
'<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="378" style="border-collapse:collapse;border-spacing:0;width:378px;min-width:378px;">\n' +
'  <tr>\n' +
'    <td width="70" valign="middle" style="width:70px;min-width:70px;padding:0 22px 0 0;vertical-align:middle;">' + img + '</td>\n' +
'    <td width="264" valign="middle" style="width:264px;min-width:264px;border-left:4px solid ' + BLUE +
      ';padding:0 0 0 18px;vertical-align:middle;">\n' +
'      <table cellpadding="0" cellspacing="0" border="0" role="presentation" width="264" style="border-collapse:collapse;border-spacing:0;width:264px;">' +
        lines.join('') +
'</table>\n' +
'    </td>\n' +
'  </tr>\n' +
'</table>';
    }

    /* Stacked -- available with layout:'stacked'.
       One column, one cell, nothing that can wrap however narrow the pane.        */
    return '' +
'<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="286" style="border-collapse:collapse;border-spacing:0;width:286px;">\n' +
'  <tr>\n' +
'    <td style="border-left:4px solid ' + BLUE + ';padding:0 0 0 18px;vertical-align:top;">\n' +
'      <table cellpadding="0" cellspacing="0" border="0" role="presentation" width="264" style="border-collapse:collapse;border-spacing:0;width:264px;">' +
'<tr><td style="padding:0 0 14px 0;font-size:0;line-height:0;' + LH + '">' + img + '</td></tr>' +
        lines.join('') +
'</table>\n' +
'    </td>\n' +
'  </tr>\n' +
'</table>';
  }

  return { build: build, colours: { BLUE: BLUE, TXTBLUE: TXTBLUE, GREY: GREY, SOFT: SOFT, HAIR: HAIR } };
})();

if (typeof module !== 'undefined') module.exports = DS;
