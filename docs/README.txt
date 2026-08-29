DIALOGUE SOCIETY - STAFF EMAIL SIGNATURE APP
=============================================
Version v10

Three pages -- the signature maker plus a finished personal and branch
signature -- with no backend, no database and no build step. They run on any
static web host.

   index.html      the signature maker
   personal.html   a finished personal signature
   branch.html     a finished branch signature
   ds-mark.png     the logo, if you ever want to link it instead of embedding

They link to each other by relative name, so keep them in the same folder.


CHECKING WHICH VERSION IS LIVE  -  READ THIS FIRST
--------------------------------------------------
The bottom of the page shows a version, e.g. "Signature app v10".

After deploying, open your address and look at it. If it does not say v10,
then either an older file was uploaded or your browser is showing a cached
copy. Reload with Cmd+Shift+R (Ctrl+Shift+R on Windows).

Quick way to tell by eye:
   v10 - the logo sits to the LEFT of the text.   <- correct
   v5   - the logo sits ABOVE the text.            <- wrong file deployed

Downloaded zips all used to share one filename, so it was easy to upload an
older one by mistake. They are numbered now. Check the number matches.


DEPLOYING TO CLOUDFLARE PAGES
-----------------------------
1. dash.cloudflare.com -> Workers & Pages -> your project -> Create deployment.
2. Upload the zip as it is, or drag in all of the files. index.html must end
   up at the TOP level, not inside a folder, or the app lands at a subpath
   and the links between the three pages break.
3. Deploy, then open the address and check the version in the footer.
4. Cloudflare keeps the previous deployment, so you can roll back from the
   Deployments tab if anything looks wrong.

First time: Workers & Pages -> Create -> Pages -> Upload assets, name the
project (e.g. dialogue-signatures), upload, Deploy. You get
https://dialogue-signatures.pages.dev

Netlify Drop (app.netlify.com/drop) works the same way - the archive root
becomes the site root.


DEPLOYING TO GITHUB PAGES
-------------------------
The repository already carries a built copy of these files in docs/, so there
is nothing to upload. In the repository, open Settings -> Pages, set Source to
"Deploy from a branch", pick the main branch and the /docs folder, and Save.

To publish a change: edit the source, run

    python3 build.py

which rewrites docs/, then commit and push. Pages redeploys on its own.


USING YOUR OWN DOMAIN
---------------------
All of these support a custom domain, so signatures.dialoguesociety.org can
point at it later without changing the address staff have bookmarked.


ABOUT THE LOGO
--------------
The logo is embedded inside each signature by default. That is deliberate: a
signature then has no external dependency and cannot lose its logo because a
host lapsed or a file moved. Gmail re-hosts the image on its own servers as
staff paste, and Apple Mail attaches it, so nothing extra travels with mail.

To link it instead, upload ds-mark.png somewhere permanent on
dialoguesociety.org, then open index.html, find

    var LOGO_URL = '';

and put the address between the quotes. Use an address on dialoguesociety.org,
never on the host serving this page - the URL is written into every signature
made here and stays in mail already sent. The status line under the preview
says which mode is active and warns if a configured URL will not load.


WHAT STAFF DO
-------------
Open the address, choose Personal or Branch, fill in their details, press Copy
signature, and follow the instructions on the page for Gmail, Apple Mail,
Outlook or iPhone. Nothing is sent anywhere - the page works entirely in their
browser and what they type is saved only on their own machine.


HOUSE STYLE
-----------
Brand blue    #008AC4   logo and the vertical rule only
Text blue     #007AAD   links, organisation line, branch lead line
Brand grey    #424242   name, contact values, address
Soft grey     #6E6E6E   job title, second line, charity line
Typeface      Helvetica Neue, falling back to Helvetica then Arial

The blue in the older signatures was #0797C8. It does not match the logo and
fails the WCAG AA contrast standard for body text. Do not reintroduce it.
