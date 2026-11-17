Migrate Leopoldo Teixeira's academic website to the al-folio v1.2 gem-based runtime,
keeping the production root URL, academic page/news permalinks, and every direct PDF
path. Preserve all bibliography, news, PDFs, and images; move social configuration
and homepage settings to the v1 contract and adapt coauthor lookup keys. Remove
starter articles and Einstein content, keeping compatibility pages at old URLs.

The workflow builds PRs without publishing. Only master push/manual events publish
production output to the root of gh-pages, with an explicit .nojekyll marker.

Validation: production Jekyll build, upgrade/override audits, generated route and
local link checks, all 68 bibliography entries and 4 selected publications,
byte comparison of content assets, and local preview HTTP checks. Browser visual
QA could not run because the browser access host was unavailable. The owner
reviewed and approved the local preview before this PR was opened. See migration/REVIEW.md and migration/CUTOVER.md for evidence,
URL changes, known limitations, cutover, and rollback commands.
