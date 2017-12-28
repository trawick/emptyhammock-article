# Changes and migration requirements

## Version 0.0.14

Article search is now implemented.  The search view is referred to as
`articles:search`; the template is `articles/article_search_results.html`.

## Version 0.0.11

You must now include `django-autocomplete-lite` and its dependencies, in
support of autocompletion for article plugins.

## Version 0.0.7

### Article plugin

You must now declare `ARTICLE_PLUGIN_SETTINGS['Article']` to
define flavor choices.

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
