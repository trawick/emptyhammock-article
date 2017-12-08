# Changes and migration requirements

## Version 0.0.6

### Single Article Teaser plugin

You must now declare `ARTICLE_PLUGIN_SETTINGS['SingleArticleTeaser']` to
define flavor choices.

A migration maps the three legacy flavors `action`, `link`, and `simple` to
flavors 1-3, which should be defined in the new setting for any legacy flavors
which were used previously.

## Version 0.0.5

*Packaging fixes only*

## Version 0.0.4

*Broken due to packaging problems*

### Requirements

You must now include `tablib` and its dependencies, in support of a new
Article feature that allows events to be imported from a spreadsheet.

### Article slugs

These are now limited to 90 characters (was 100).  As these are generally
auto-generated and titles are limited to 80 characters, this isn't expected
to be a problem.
