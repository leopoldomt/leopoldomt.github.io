# Local migration review

All work is local on `upgrade/al-folio-v1.2`, based on master, with no migration
commit yet. Nothing was pushed, no PR was opened, and no Pages settings changed.
The running preview is <http://127.0.0.1:4000/>; restart with `bin/preview` from
the repository root. Its output is `_site_preview`, separate from `_site`.

## Verified starting point

- Both website and read-only sibling v1.2 worktrees were clean before migration.
- Origin: `git@github.com:leopoldomt/leopoldomt.github.io.git`.
- Fetch succeeded. The clone fetches only master by default, so gh-pages was
  explicitly fetched into `origin/gh-pages` without changing the fetch refspec.
- Local master and fetched origin/master both identify Jekyll source at
  `dc6897223ef1f37fdef3cd5085f53c5f28d6035f` (the supplied SHA).
- Sibling `../al-folio-v1.2` is detached at the v1.2 tag; HEAD and peeled tag
  both equal `b95d6d61a1b0663529094b1b5f4fbe8aa41f8a04`.
- Published gh-pages tip and last verified good output:
  `fcf047e4c69cbe2eb4514bebf4c99720de24460e`. Its commit message identifies
  `dc68972…` as its source. The supplied SHA is **not** the output commit.
- [Source deploy succeeded](https://github.com/leopoldomt/leopoldomt.github.io/actions/runs/43036303280),
  then [Pages deployment succeeded](https://github.com/leopoldomt/leopoldomt.github.io/actions/runs/43036468087)
  for `fcf047e…`. Read-only Pages API confirms `legacy`, `gh-pages`, `/`, built.
- The live homepage returned 200 and was compared with the gh-pages snapshot.
  See `live-comparison.json` for the byte comparison result.

Exact identifiers and content checks are in `baseline.json`. The sibling checkout
was used only for reads and remains unchanged. Existing website Git history and
master remain intact; the upgrade branch has the migration worktree changes.

## What changed

- Use v1.2's Gemfile, gem pins, core theme and plugin wiring. Track the lockfile
  with macOS and Linux platforms. Ruby 3.3 was installed with Homebrew because
  system Ruby 2.6 cannot run this version.
- Remove old `_includes`, `_layouts`, `_sass`, `_plugins`, CSS/JS/font runtime
  copies. The pinned gems now provide these. There are **no local gem overrides**.
- Transfer identity, site URL, root baseurl, layout settings, bibliography options,
  publication badges, comment identifier, and feature preferences. Keep analytics
  off, as before; the obsolete UA analytics ID is not activated in v1.
- Move social identities to `_data/socials.yml`; rename Twitter's setting to
  `x_username` and correct the YouTube ID to avoid a duplicated URL prefix.
  Normalize coauthor keys for v1's lowercase/accent-free lookup, retaining URLs
  and all existing first-name variants.
- Adapt homepage `subtitle`, profile `more_info`, and page-level announcements;
  retain the biography, photo, office, five recent news entries, and selected papers.
  The full news archive includes all 56 entries, including their old date-prefixed URLs.
- All 68 BibTeX entries, all 56 news files, all 66 PDFs, and all 24 images are
  byte-for-byte identical to the source baseline. All PDF filenames and page/news
  permalinks remain valid. Service, student, and teaching content is retained
  (unused commented demo markup was removed from service).
- Remove starter posts/projects and Einstein profile/CV/resume content. The existing
  `/cv/` now contains only verified education/career facts from the biography and a
  Lattes link; `/people/` points to students/group, `/projects/` points to research
  repositories, and `/repositories/` retains the actual repository list as links.
  Unreferenced static legacy images/media and `example_pdf.pdf` remain to preserve
  direct asset links; no demo posts or Einstein identity is displayed.
- Disable starter RSS imports, unused blog pagination and book archives. Remove
  the notebook plugin from both Gemfile/config because no site pages use notebooks;
  this avoids converting a bundled demo notebook during every build.
- Add `bin/preview`, a repeatable verification script, evidence, and cutover guidance.

## URLs and content differences

No academic page, news, or PDF URL changed. All old HTML routes are still generated,
including the accidentally exposed `/_pages/dropdown/` and demo notebook HTML.
Former starter blog article/archive URLs serve a short compatibility page and
redirect to `/blog/`; that page points to the real news archive. The old exposed
`/_pages/about_einstein.md` now serves a compatibility notice with a home link;
its `.md` content type may cause the browser to display that notice as text.
HTML compatibility routes use theme-provided meta refresh redirects, not
server-side HTTP 301s. `retired-sample-urls.txt` lists
the old blog and Einstein paths; the additional compatibility paths are
`/_pages/dropdown/` → `/publications/` and `/assets/jupyter/blog.ipynb.html` → `/blog/`.

Old Bootstrap/MDB/font files and some obsolete JS endpoints have been retired in
favor of v1 gem assets/CDNs. The fake `/assets/json/resume.json` and accidentally
published repository tooling/readme/report files are no longer published.
`verification.json` records **every** old file missing from the new output;
these are intentional runtime/tooling/demo removals, not unreported page/PDF changes.
New canonical production URLs remain under `https://leopoldomt.github.io/`.

## Verification and remaining attention

- Production `JEKYLL_ENV=production bundle exec jekyll build --trace`: passed.
- `python3 migration/verify.py`: passed, all historical HTML/PDF paths and exposed
  Einstein path, all 68 publications and 4 selected papers, and all local links
  including responsive image sources. Full counts/results: `verification.json`.
- Upgrade audit: 0 blocking, 0 non-blocking findings. Override audit: no overrides.
  Saved in `upgrade-audit.txt` and `overrides-audit.txt`.
- Development Jekyll preview: running with live reload, HTTP 200. HEAD checks for
  homepage, publications, news, service, students, teaching, photo, all historical
  news pages and every PDF are recorded in `http-checks.json`.
- Live site checks: homepage, publications, award news, and an actual paper PDF
  returned 200. Published-tree comparison is the complete historical path inventory;
  no crawl of external sites was performed.
- Relevant remaining build warning: ActiveSupport's `to_time` timezone behavior
  will change in Rails 8. This originates in a pinned dependency; it does not fail
  the build. Notebook conversion, missing pagination, and Bootstrap warnings were
  resolved rather than suppressed. Sass emits no warnings on the final build.
- Browser access host was unavailable, so **visual/browser interaction QA remains
  for owner review**: desktop/mobile layout, profile crop, dark mode, search,
  publication reveal controls and external icon/CDN loading. Static HTML and local
  asset existence were verified; these do not establish interactive behavior.
- The existing Discord value is a username rather than the numeric user ID its
  profile URL needs; it was preserved, but the owner should supply a valid numeric
  ID or remove that social entry. Other external account links were transferred;
  account validity and third-party badge responses were not comprehensively tested.
- Docker helpers are based on v1.2 and Ruby 3.3; Docker was not built/tested. The
  verified local route is native Ruby/Jekyll. GitHub Actions cannot be executed on
  GitHub until the owner pushes the PR; Linux CI/Pages verification is still required.

## Deployment changes

The old workflow and v1.2 starter both accept master/main push and PR events plus
manual dispatch, and both deploy on any non-PR event. Their deployment action leaves
branch/root behavior implicit; in particular, a manual run on another branch can
publish. The migrated workflow:

- Builds PRs targeting master, pushes to master, and all manual dispatches.
- Publishes **only** push/manual runs whose ref is `refs/heads/master`.
- Gives build a read-only token; only publish has contents-write permission.
- Uses explicit gh-pages root, cleans stale files, and includes `.nojekyll`.
- Uses Ruby 3.3 and the committed lockfile; installs ImageMagick, builds production,
  runs path/link checks, and publishes the same artifact that passed verification.
- Removes upstream template-sync and Docker-image publication workflows.
- Omits starter Python/Jupyter, npm demo/visual-test dependencies, and PurgeCSS:
  no site pages need notebook conversion and v1's core ships prebuilt/minified CSS.
  This avoids an extra post-build purge altering verified Tailwind runtime styles.
- Uses no push path filter so a dependency/workflow/source change cannot accidentally
  skip the production build. Concurrency serializes runs for the same source ref.

No Pages settings change is needed. Follow [CUTOVER.md](CUTOVER.md) for exact
push, PR, merge, independent build/Pages checks, and source/published rollback steps.
