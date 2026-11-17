# Post-review cutover

These are instructions for the owner after reviewing the local preview and diff.
No push, PR, merge, deployment, or settings change was performed during migration.

## Review and publish the source

Run from the website checkout. Include all migration files, especially the lockfile,
compatibility pages, and verification scripts. The migration is deliberately uncommitted.

```sh
git switch upgrade/al-folio-v1.2
git diff --stat
git diff
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle install
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 migration/verify.py
git add -A
git commit -m "Migrate academic website to al-folio v1.2"
git push -u origin upgrade/al-folio-v1.2
gh pr create --base master --head upgrade/al-folio-v1.2 \
  --title "Migrate academic website to al-folio v1.2" \
  --body-file migration/PR-BODY.md
```

Record the PR number printed by `gh pr create` as `PR_NUMBER`:

```sh
PR_NUMBER=123 # replace with the actual number
gh pr checks "$PR_NUMBER" --watch
gh pr view "$PR_NUMBER" --web
```

Review the `Deploy site / build` result and the `site` artifact. There must be
no publishing job for the PR. Check any repository-specific required checks.
When satisfied, create a merge commit so the source rollback remains simple:

```sh
gh pr merge "$PR_NUMBER" --merge
git switch master
git pull --ff-only origin master
git rev-parse HEAD # record this merge SHA for rollback
```

## Verify build and Pages separately

The merge triggers `Deploy site`. Confirm **both build and publish** succeed:

```sh
gh run list --workflow deploy.yml --branch master --limit 5
# Set RUN_ID to the matching master run ID, then:
gh run watch RUN_ID --exit-status
git fetch origin gh-pages:refs/remotes/origin/gh-pages
git show -s --format=fuller origin/gh-pages
git ls-tree origin/gh-pages .nojekyll index.html
```

Then check the separate GitHub-managed `pages build and deployment` run at
<https://github.com/leopoldomt/leopoldomt.github.io/actions>. Its SHA should
match the **new gh-pages commit**, not the master merge SHA. Inspect its deployment
result, and verify the settings still show `gh-pages`, `/(root)`:

```sh
gh api repos/leopoldomt/leopoldomt.github.io/pages \
  --jq '{status,build_type,source,html_url}'
curl -I https://leopoldomt.github.io/
curl -I https://leopoldomt.github.io/publications/
curl -I https://leopoldomt.github.io/news/2026-09-03-sast-award/
curl -I https://leopoldomt.github.io/assets/pdf/2026-ist.pdf
```

Open the site in a fresh browser session; inspect photo, news, selected papers,
publications, PDF buttons, author links, mobile navigation, search, and dark mode.
A successful publishing action alone does not prove Pages has served the new site.
GitHub/CDN caching can delay visible changes; compare the rendered HTML and asset
URLs with the uploaded artifact. If no Pages build starts after publication,
request a branch Pages rebuild (after review only):

```sh
gh api --method POST repos/leopoldomt/leopoldomt.github.io/pages/builds
```

A production rebuild without a source commit is available with:

```sh
gh workflow run deploy.yml --ref master
```

A manual run selecting any other branch builds only. A branch push alone does
not run this workflow unless it is master; opening/updating a PR targeting master
runs build only. PRs have read-only token permissions. Manual runs on the upgrade
branch cannot publish. Publish uses explicit `branch: gh-pages`, `target-folder: .`,
`folder: _site`, and cleans stale output, retaining gh-pages Git history.

## Roll back the source

First stop/cancel any in-flight deployment runs so they cannot overwrite rollback.
Create and review a source rollback PR; do not reset or force-push master:

```sh
git switch master
git pull --ff-only origin master
git switch -c rollback/al-folio-v1.2
git revert -m 1 MERGE_SHA # replace with the migration merge SHA recorded above
git push -u origin rollback/al-folio-v1.2
gh pr create --base master --head rollback/al-folio-v1.2 \
  --title "Roll back al-folio v1.2 migration" \
  --body "Restore the source before the al-folio v1.2 migration."
```

Review and merge the rollback PR. If the upgrade was squash-merged instead, use
`git revert SQUASH_SHA` (no `-m`). Wait for its deployment to finish, or cancel it
if restoring the exact published snapshot below. The pre-upgrade source baseline
is `dc6897223ef1f37fdef3cd5085f53c5f28d6035f`. Rebuilding that old source can fail
because its dependency set was unpinned; restoring the published tree is independent
of rebuilding it.

## Restore the exact known-good published tree

Do this **after** the source rollback deployment has finished/cancelled. Otherwise
a later source deployment may overwrite the restored site. This creates a new
commit containing the old tree; it does not rewrite branch history.
Run from the main checkout, using a fresh, unused worktree path:

```sh
git fetch origin gh-pages:refs/remotes/origin/gh-pages
git worktree add -b rollback/published-v1.2 /tmp/leopoldo-pages-rollback origin/gh-pages
git -C /tmp/leopoldo-pages-rollback restore \
  --source=fcf047e4c69cbe2eb4514bebf4c99720de24460e --staged --worktree -- .
git -C /tmp/leopoldo-pages-rollback diff --cached --stat
git -C /tmp/leopoldo-pages-rollback commit -m "Restore last known-good published site"
git -C /tmp/leopoldo-pages-rollback diff --exit-code \
  fcf047e4c69cbe2eb4514bebf4c99720de24460e HEAD -- .
git -C /tmp/leopoldo-pages-rollback push origin HEAD:gh-pages
```

If Git reports nothing to commit, the published tree already matches the snapshot.
If the push rejects because gh-pages advanced, fetch and repeat restoration from
its new tip in a fresh rollback branch; never force-push. Verify the separate Pages
deployment and live URLs again. Request a Pages rebuild with the POST command above
if needed. This snapshot is verified by its deploy commit message and successful
Pages run, recorded in `baseline.json`.
