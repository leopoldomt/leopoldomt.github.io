# Leopoldo Teixeira's academic website

Jekyll source for <https://leopoldomt.github.io/>, migrated to the al-folio
v1.2 starter with pinned gem runtime dependencies.

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" # macOS Homebrew; otherwise use Ruby 3.3
bundle config set --local path vendor/bundle
bundle install
bin/preview
```

Preview: <http://127.0.0.1:4000/>. Stop with Ctrl-C. The preview writes to
`_site_preview`, separate from production output. Restart after configuration
changes. Dependencies include Ruby 3.3, Node (for the JS minifier), and ImageMagick.

```sh
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 migration/verify.py
bundle exec al-folio upgrade audit --no-fail
bundle exec al-folio upgrade overrides audit
```

Edit `_pages/about.md`, `_pages/{service,students,teaching}.md`, `_news/`,
`_bibliography/papers.bib`, `_data/{socials,coauthors,venues}.yml`, and `assets/`
for site content. Keep `url: https://leopoldomt.github.io` and `baseurl: ''`.
The gem owns runtime layouts, styles, scripts, and Liquid helpers. There are
no local runtime overrides. Add future plugins to **both** Gemfile and
`_config.yml`, then review the lockfile changes.

See [migration review and verification](migration/REVIEW.md) and
[post-review cutover and rollback](migration/CUTOVER.md). No deployment is
needed to review locally. Only master push/manual runs can publish; PRs build only.
