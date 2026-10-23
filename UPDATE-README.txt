DAWITDSEYOUM.COM — SELF-UPDATE ENGINE
=====================================

WHAT THIS IS
------------
Two folders that turn your GitHub repository into a self-updating website:

  source/                          the site's workshop: code, data, and the
                                   Bluesky sync robot
  .github/workflows/self-sync.yml  the daily robot (a GitHub Action)

Once installed, the site updates ITSELF:

  you post on Bluesky  ->  the robot downloads the new photographs, writes
  the captions into the walls, rebuilds the site, and pushes it to this
  repository  ->  Cloudflare redeploys automatically.

You never touch GitHub, Cloudflare, or the site again. Posting on Bluesky
IS updating the website.


HOW TO INSTALL (one time, about 5 minutes, using GitHub Desktop)
----------------------------------------------------------------
1. Install GitHub Desktop (desktop.github.com), sign in, then open
   File -> Clone Repository -> dawitdseyoum-website.
   Choose a folder you can find again (e.g. Documents).

2. Unzip this package (dawitdseyoum-selfsync-upgrade.zip).
   You get: a folder "source", a folder ".github", and this readme.

3. Drag BOTH folders into the repository folder on your computer
   (the one called "dawitdseyoum-website").
   - Windows: ".github" starts with a dot — that is correct, keep it.
   - If you see two small files called ".gitignore" and ".assetsignore",
     drag those in as well.
   - If asked about merging folders, choose yes/merge.

4. In GitHub Desktop you will see ~140 new files listed.
   In the summary box (bottom left) write:  add self-update engine
   Click "Commit to main", then click "Push origin".

5. Enable Actions (one click): on github.com open your repo ->
   the "Actions" tab -> if you see a button
   "I understand my workflows, go ahead and enable them" -> click it.


TEST THE ROBOT (2 minutes, do this once)
----------------------------------------
1. On github.com -> your repo -> "Actions" tab.
2. Left sidebar: "Self-sync from Bluesky".
3. Right side: "Run workflow" -> the green "Run workflow" button.
4. Wait ~3 minutes until the run turns green (a tick).
5. Done. A new commit appeared in the repo, and Cloudflare redeploys the
   site automatically (check Workers & Pages -> your project ->
   Deployments — you should see a deployment for that commit).
   The website will look unchanged — that is correct: nothing new was
   posted yet, so there was nothing to add.

If the Actions run is green but Cloudflare does NOT show a new deployment,
tell me in the chat — connecting the repo's auto-deploy is a 2-click fix.


FROM NOW ON — YOUR ENTIRE WORKFLOW
----------------------------------
1. Post photographs on Bluesky, with your captions, like you already do.
   (Bluesky is the pipeline source — the captions live there. Photos
   posted only on Instagram/Flickr will not flow in automatically.)
2. Within 24 hours the robot adds them to dawitdseyoum.com —
   same walls, same captions, same layout. The collection simply grows.
3. Impatient? Actions -> "Self-sync from Bluesky" -> "Run workflow" —
   3 minutes and your new work is live.
4. Field Notes essays: send those to me in the chat. They are curated by
   hand, not by the robot.

Housekeeping (optional):
- The empty repos "Dwebsite" and "dawitdseyoum-webiste" can be deleted:
  repo -> Settings -> scroll to Danger Zone -> Delete this repository.
- Add your site (dawitdseyoum.com) to your Bluesky/Instagram/Pixelfed/
  Flickr bios — good for people AND for Google.
