# Local security compatibility copy

This is the runtime of `jekyll-3rd-party-libraries` 0.0.1, copied verbatim from
its RubyGems package. Copyright and license are preserved in `LICENSE`.
`UPSTREAM.json` records each upstream runtime file's SHA-256 checksum.

Upstream requires `css_parser < 2.0`, but GHSA-9pmc-p236-855h is fixed only in
`css_parser >= 3.0.0`. The local gemspec allows `>= 3.0, < 4.0`; the site's Ruby
requirement is 3.3. No runtime library code has been changed. Keep the original
gem version so the al_img_tools 1.0.3 dependency remains satisfied. Bundler's
explicit path source distinguishes this local copy from the registry package.

The production site keeps `third_party_libraries.download: false`; URL template
expansion remains active. The patched CSS parser API is also checked by the
security regression tests. Do not replace this copy with the registry gem until
an upstream release permits patched css_parser. Review and remove the path source
when that release is available.

Upstream: <https://github.com/george-gca/jekyll-3rd-party-libraries>
Advisory: <https://github.com/advisories/GHSA-9pmc-p236-855h>
