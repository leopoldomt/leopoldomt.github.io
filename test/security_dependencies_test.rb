# frozen_string_literal: true
require 'minitest/autorun'
require 'minitest/mock'
require 'jekyll'
require 'al_citations'
require 'css_parser'
require 'stringio'

# Cover APIs changed by the security upgrades that are not exercised by the
# current bibliography or by third_party_libraries.download: false.
class SecurityDependenciesTest < Minitest::Test
  def setup
    Jekyll::GoogleScholarCitationsTag::Citations.clear
    Jekyll::InspireHEPCitationsTag::Citations.clear
  end

  def test_scholar_tag_still_parses_and_formats_counts_with_active_support_8
    html = '<meta name="description" content="Cited by 1,234">'
    template = Liquid::Template.parse('{% google_scholar_citations scholar article %}')
    URI.stub(:open, ->(*) { StringIO.new(html) }) do
      assert_equal '1.2K', template.render!('scholar' => 'fixture', 'article' => 'fixture')
    end
  end

  def test_inspirehep_tag_still_formats_counts_with_active_support_8
    payload = { 'hits' => { 'hits' => [{ 'metadata' => { 'citation_count' => 1532 } }] } }
    template = Liquid::Template.parse('{% inspirehep_citations record %}')
    Net::HTTP.stub(:get, ->(*) { payload.to_json }) do
      assert_equal '1.5K', template.render!('record' => 'fixture')
    end
  end

  def test_css_parser_retains_the_font_rewrite_api_used_by_the_library_loader
    parser = CssParser::Parser.new
    parser.load_string!("@font-face { font-family: Fixture; src: url('fixture.woff2') format('woff2'); }")
    count = 0
    parser.each_rule_set do |rule|
      assert_includes rule['src'], 'fixture.woff2'
      rule['src'] = 'url(/assets/libs/fixture/fonts/fixture.woff2)'
      count += 1
    end
    assert_equal 1, count
    assert_includes parser.to_s, 'url(/assets/libs/fixture/fonts/fixture.woff2)'
  end

  def test_css_parser_rejects_file_uris_by_default
    parser = CssParser::Parser.new(io_exceptions: true)
    assert_raises(CssParser::RemoteFileError) do
      parser.load_uri!('file:///this-file-must-not-be-read.css')
    end
  end
end
