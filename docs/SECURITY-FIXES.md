# Dependency security fixes — 2026-11-17

Local branch: `fix/security-dependencies`, based on master `d344461`.
No source content or public URL was changed. Nothing was committed, pushed, or deployed
while preparing these fixes. Dependabot's remote alerts will remain open until the
fixed lockfile reaches the default branch and GitHub rescans it.

## Updates

| Dependency | Previous | Fixed | Existing alerts addressed |
| --- | --- | --- | --- |
| addressable | 2.9.0 | 2.9.2 | 6 |
| loofah | 2.25.2 | 2.25.3 | 6 |
| nokogiri | 1.19.4 | 1.19.7 | 3 |
| crass | 1.0.7 | 1.0.8 | 1 |
| activesupport | 7.2.3.1 | 8.0.5.2 | 1 high |
| css_parser | 1.22.0 | 3.4.0 | 1 high |

The six updated versions no longer satisfy any of the vulnerable version ranges
in the 18 open Dependabot alerts checked through the GitHub API. All macOS/Linux
Nokogiri lockfile variants were updated; unrelated al-folio pins remain unchanged.
The updated CSS parser also brings in its SSRF filtering dependency.

Two plugin constraints required compatibility fixes:

- `al_citations` 1.0.1 is sourced from immutable upstream commit
  `ef8ab02fbd4f1383d5126616be02afd985f3b355`. That commit changes only gemspec
  bounds, permitting ActiveSupport 8 and modern Bundler. It has not been released
  to RubyGems. ActiveSupport is constrained to patched 8.0.x in this site.
- `jekyll-3rd-party-libraries` 0.0.1 is explicitly sourced from
  `gems/jekyll-3rd-party-libraries`. Its upstream runtime files are unchanged;
  the local gemspec permits patched CSS Parser 3.x instead of requiring <2.
  The upstream MIT license and runtime SHA-256 inventory are included. This
  also satisfies the existing al_img_tools dependency without disabling features.
  See that directory's README for maintenance and removal guidance.

These exceptions keep the v1.2 runtime and existing features rather than updating
the whole theme. They are dependency source/metadata changes, not theme overrides.
The local gem and tests are excluded from the generated site.

## Validation

- Production build: passed.
- Ruby advisory database audit: **no vulnerabilities found**, with no ignored
  advisories. Database commit `cad74bbe85c643bb9456450f357d6288c9ded2f8`,
  containing 1,378 advisories at verification time.
- All 18 GitHub alert ranges independently checked against installed gem versions:
  **0 still affected**.
- Before/after production output comparison: **375 files in each build**, none
  added or removed. All HTML, CSS, JS, images, PDFs, and other assets are
  byte-for-byte identical. The only changed file is `feed.xml`, whose `<updated>`
  build timestamp changed; its other content is identical.
- Site verifier: passed, covering **185 historical paths**, **118 HTML files**,
  **68 publications**, **4 selected papers**, and **0 broken local links**.
- Compatibility tests: **4 tests, 8 assertions, 0 failures/errors**. Exercise
  Scholar and InspireHEP rendering with stubbed responses under ActiveSupport 8,
  the font rewrite API under CSS Parser 3, and file-URI rejection by default.
- Upgrade audit: 0 blocking/non-blocking findings. Override audit: no overrides.
- Updated-dependency preview: **130 HTTP checks passed**, including major pages,
  profile photo, every historical news page, and all PDF paths.
- `git diff --check`: passed.

Browser access was unavailable, so interactive browser QA could not be repeated.
The complete output comparison establishes that the served production page and
asset bytes are unchanged. The remaining build warning is the dependency's
ActiveSupport `to_time` deprecation about future Rails 8.1 timezone behavior.
GitHub-hosted Linux CI and Dependabot alert closure must be verified after an
owner-authorized push/merge; neither was performed locally.

## Repeat checks

With Ruby 3.3 and dependencies installed:

```sh
bin/security-check
bundle exec ruby test/security_dependencies_test.rb
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 migration/verify.py
bundle exec al-folio upgrade audit --no-fail
bundle exec al-folio upgrade overrides audit
```

`bin/security-check` updates the Ruby advisory database under ignored
`.local/security/`; it requires network access. CI now runs this audit and the
compatibility tests before building or publishing. Future known vulnerabilities
fail the workflow instead of being silently ignored.

Local evidence and the pre-change build are under ignored `.local/security/`;
historical migration reports were left intact.

## Preview

The fixed-dependency preview is running at <http://127.0.0.1:4001/>. The earlier
server on port 4000 was preserved. Restart the new preview from the repository root:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" # Apple Silicon Homebrew
bundle exec jekyll serve --host 127.0.0.1 --port 4001 \
  --destination .local/security/preview --no-watch
```
