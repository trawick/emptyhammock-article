# emptyhammock_article

## Overview

This package implements some of my idiosyncratic ideas for how some classes of
users can effectively create content for their web site and use a combination of
Django CMS plugins and other site features to make that content accessible to
users of their site.  It is not intended to be the only way content would be
created for a site, and it should not be construed as an appropriate solution
for a large class of developers and client scenarios.

At its core, the package provides a multi-purpose `Article` class, a view
for articles, and Django CMS plugins which allow the content editor to
place particular articles or article teasers on a CMS page.  Additional
CMS plugins are provided to create article feeds.  As examples, you could
place an article feed on a CMS page that displays links to sets of articles
like the following:

* recently updated articles
* upcoming (future) events

The article feeds can optionally be limited by particular article tags,
and they are always limited by time range and number of items.

Articles can be marked invisible either manually or automatically by a
scheduled task.

## Planned development in the near term

Currently articles are editable only in the Django admin.  Most content
editors need a wizard-like approach to adding articles, along with autocomplete
and other UI aids to prevent frustration.

## Integrating this in your Django/Django CMS project

* Install the latest version from Github by adding something like
  `git+git://github.com/trawick/emptyhammock_article.git@0.0.1` to your
  pip requirements file.  **Please check the current release.**
* Install dependencies, not currently called out in `setup.py`:
  * `tablib==0.12.1`, `django-taggit==0.22.1`, `django-cms==3.4.5`,
    `djangocms-text-ckeditor==3.5.1`, `django-filer==1.3.0` (and
    their dependencies)
* Add 'articles' to `INSTALLED_APPS`.
* Add `url(r'^articles/', include('articles.urls', namespace='articles')),` to
  your base `urls.py`'s `urlpatterns`.
* Copy the `sample_templates` tree to your project (presumably to a different
  directory name) and update your settings so that they are found.  You'll need
  to customize the templates for your application, but you may want to
  experiment with them as is until you actively use features that require a
  particular template.
* Optional: Call `articles.utils.expire_articles()` from a scheduled task in
  order to mark expired articles as invisible.

## Specifying an Article search configuration

### Example Postgres setup

The following commands create a full text search configuration that ignores
accents:

```
$ sudo -u postgres psql my_project_db
psql (9.5.10, server 9.4.8)
Type "help" for help.

my_project_db=# create extension if not exists unaccent;
CREATE EXTENSION
my_project_db=# create text search configuration english_unaccent(copy=english);
CREATE TEXT SEARCH CONFIGURATION
my_project_db=# alter text search configuration english_unaccent alter mapping for hword, hword_part, word with unaccent, english_stem;
ALTER TEXT SEARCH CONFIGURATION
my_project_db=#
```

### Django settings

This configures Article search to use the configuration created in the example
above:

```
ARTICLE_SEARCH_SETTINGS = {
    'config': 'english_unaccent',
}
```

## Support

This package exists to support my own commercial activities.  Just maybe it can
provide other developers with a helpful hint, or even more.  Feel free to open
Github issues for suggestions or suspected problems, but please don't expect me
to volunteer any time to respond or otherwise address them directly.  Think of
Github issues for this project as a way to document something you'd like me to
be aware of when fixing problems or implementing future requirements.
