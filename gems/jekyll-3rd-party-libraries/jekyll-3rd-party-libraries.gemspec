# frozen_string_literal: true
require_relative 'lib/jekyll-3rd-party-libraries/version'

Gem::Specification.new do |spec|
  spec.name = 'jekyll-3rd-party-libraries'
  spec.version = Jekyll::ThirdPartyLibraries::VERSION
  spec.authors = ['George Corrêa de Araújo']
  spec.summary = 'Third-party library URL expansion and optional downloads for Jekyll'
  spec.homepage = 'https://github.com/george-gca/jekyll-3rd-party-libraries'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.3'
  spec.files = Dir['lib/**/*', 'LICENSE', 'README.md', 'UPSTREAM.json']
  spec.require_paths = ['lib']
  spec.add_dependency 'jekyll', '>= 3.6', '< 5.0'
  # Security compatibility patch: upstream's < 2.0 prevents installing the fix.
  spec.add_dependency 'css_parser', '>= 3.0', '< 4.0'
  spec.add_dependency 'nokogiri', '>= 1.8', '< 2.0'
end
