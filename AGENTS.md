# Maintaining Leopoldo Teixeira's academic website

This repository contains the Jekyll source for <https://leopoldomt.github.io/>.
It uses the al-folio v1.2 starter and a pinned, gem-based runtime. This is a
personal academic site; upstream starter-development instructions do not apply
automatically. Follow the user's task scope and preserve unrelated work.

## Before making changes

- Check the current branch, working tree, and applicable nested instructions.
  Preserve existing edits. Do not assume the current checkout is up to date with
  GitHub or that an earlier PR is still open.
- Work on a task branch when changing source on `master`. Do not reset or
  force-push shared branches.
- Keep work local unless the user authorizes committing, pushing, opening a PR,
  merging, or deploying. Approval for one action does not authorize the others.
- Consult `README.md` for setup and `migration/REVIEW.md` for migration history.
  Migration reports describe a historical snapshot, not necessarily current state.

## Content map

| Content | Location |
| --- | --- |
| Biography, profile image settings, homepage announcements | `_pages/about.md` |
| Publications page | `_pages/publications.md` |
| Service, students, and teaching | `_pages/service.md`, `_pages/students.md`, `_pages/teaching.md` |
| Other public pages and compatibility routes | `_pages/` |
| News entries | `_news/`; full archive wrapper: `news.html` |
| BibTeX entries and selected publications | `_bibliography/papers.bib` |
| Social identities | `_data/socials.yml` |
| Coauthor links and venue metadata | `_data/coauthors.yml`, `_data/venues.yml` |
| Repository list | `_data/repositories.yml` |
| Profile photo | `assets/img/lmt.jpg` |
| Papers and other downloadable PDFs | `assets/pdf/` |
| Site settings and plugin activation | `_config.yml` |
| Dependencies and reproducible versions | `Gemfile`, `Gemfile.lock` |
| CI build and publication | `.github/workflows/deploy.yml` |

Keep academic facts grounded in supplied content; do not invent appointments,
awards, student details, or publication metadata. Do not introduce starter sample
content or Einstein profile data. Edit social accounts in the data file rather
than restoring legacy top-level configuration keys.

News files use YAML front matter and date-prefixed filenames. Keep existing
filenames: they form part of `/news/:path/`. Homepage announcements are configured
in the about page's front matter. In BibTeX, `selected = {true}` selects homepage
papers; local PDF values are filenames relative to `assets/pdf/`. Coauthor lookup
keys use lowercase, accent-free surnames as produced by the runtime's
`remove_accents` filter; preserve first-name variants and destination URLs.

## URL and content contracts

- Keep `url: https://leopoldomt.github.io` and `baseurl: ''` in production.
- Preserve public page permalinks, news routes, publication keys/anchors, and
  direct PDF paths. Add a compatibility route if a requested change moves a page.
- Keep existing PDFs and images unless the task explicitly calls for their removal
  or replacement. A filename change can break external links.
- Retain `_pages/legacy-*.html` compatibility pages. They preserve old public
  routes while retiring starter content; they are not active demo articles.
- `migration/published-paths.txt` records the pre-migration published inventory.
  Do not remove entries merely to make verification pass. Distinguish deliberate
  runtime/tooling removals from broken public content URLs.

## Runtime and dependency changes

The theme is `al_folio_core`. Installed gems supply layouts, includes, styles,
JavaScript, and Liquid helpers; there are no intentional local runtime overrides
in the migrated baseline. Avoid copying old theme directories back into this site.

For a customization, prefer content, front matter, configuration, or an existing
plugin option. A necessary site-local override is allowed, but keep it small,
document why it exists, and review it with the upgrade override audit. Follow the
audit's diff/accept workflow and track `.al-folio-overrides.yml` when applicable.

Add or remove plugins in **both** `Gemfile` and `_config.yml`. Preserve explicit
al-folio gem pins and commit lockfile changes with dependency changes. Keep Linux
CI platforms supported. Use the requested upstream release as a read-only reference;
do not silently replace release pins with upstream `main` or update dependencies
unrelated to the task. Core CSS is prebuilt; the current CI does not run PurgeCSS.

## Local setup and verification

Use Ruby 3.3, Bundler, Node for JavaScript minification, ImageMagick, and Python 3
for the verification script. On Apple Silicon macOS, system Ruby 2.6 is too old:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle config set --local path vendor/bundle
bundle install
```

Install dependencies when missing or changed. Launch the preview with:

```sh
bin/preview
```

The preview runs at <http://127.0.0.1:4000/> with live reload and writes to
`_site_preview/`. Restart it after configuration changes. Check for an existing
server before launching another; preserve a preview the user is actively reviewing.

For site content, runtime, configuration, or dependency changes, run:

```sh
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 migration/verify.py
```

For runtime/dependency changes, also run:

```sh
bundle exec al-folio upgrade audit --no-fail
bundle exec al-folio upgrade overrides audit
```

Inspect the audit findings: `--no-fail` does not make a successful exit proof of
zero findings. Verification checks historical HTML/PDF paths, local HTML links,
bibliography entries, selected papers, and key homepage content. When changing
those features intentionally, adapt semantic checks without weakening URL coverage.

Inspect affected pages in a browser when available, especially the homepage photo,
news, publications, PDF buttons, mobile navigation, search, and dark mode. Report
browser or external-service checks that could not run. Documentation-only changes
need a diff/consistency check rather than a full site rebuild. Keep generated output,
dependencies, and caches out of commits; do not overwrite historical migration
evidence with routine build output. `AGENTS.md` is already excluded from the site.

## Deployment and rollback

- `master` contains source; `gh-pages` contains generated output. Do not manually
  edit generated output for normal site changes.
- PRs targeting `master` build and verify only. A skipped publish job on a PR is
  expected. Only a push or manual workflow run on `master` may publish.
- Publication writes `_site/` to the root of `gh-pages`, includes `.nojekyll`, and
  cleans stale output. Keep the read-only build token and publishing job's scoped
  write permission. Do not let a PR or another branch publish.
- Pages uses deployment from `gh-pages`, `/(root)`. Do not change repository
  settings or switch deployment mechanisms without explicit authorization.
- After an authorized merge, verify the source build/publish run, the separate
  Pages deployment, and the live URLs. These are distinct checks.
- See `migration/CUTOVER.md` for cutover and source/published rollback procedures.
  Its recorded good commits belong to the v1.2 migration; identify the appropriate
  current recovery point before rolling back a later change. Prefer revert/new
  restoration commits over rewriting history.

When handing off, summarize changes, checks and warnings, any URL effects, and
remaining review items. Include the preview URL and restart command when relevant.
