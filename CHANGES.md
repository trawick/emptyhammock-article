# Changes and migration requirements

## Version 0.0.22

* The search view now orders even empty querysets in order to avoid
  `UnorderedObjectListWarning` in that case (e.g., loading the search page
  with no prior search).

## Version 0.0.21

* The article feed CMS plugin now supports inclusion of "Album" articles.

## Version 0.0.20

* Reset the expiration time for an event `Article` if it is currently less
  than the start time.

## Version 0.0.19

* `Article` search now searches the `subtitle` field too.

## Version 0.0.18

* `Article` admin now provides duplicate, hide, and show actions.
* Site visibility is displayed in the admin list view.

## Version 0.0.17

* `Article.creator_key` is now viewable and editable in admin.

## Version 0.0.16

### Repository name

The repository name was changed from `emptyhammock_article` to
`emptyhammock-article`.

### `new_event` management command

This brings two new dependencies:

* `django-click` (and its dependencies)
* `emptyhammock-time` (`git+git://github.com/trawick/emptyhammock-time.git@0.0.2`)

## Version 0.0.15

### Detail view URL

This is now `<prefix>/view/<slug/` instead of simply `<prefix>/<slug>/`.
No redirects are provided.

### Article search configuration

A Postgres search configuration can be specified.  This is covered in the
README.

## Version 0.0.14

Article search is now implemented.  The search view is referred to as
`articles:search`; the template is `articles/article_search_results.html`.
It only works with Postgres, and `django.contrib.postgres` must be added
to `INSTALLED_APPS`.

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
