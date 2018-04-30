# emptyhammock-article

## Overview

This package implements an idea for how some classes of
users can effectively create content for their web site and use a combination of
Django CMS plugins and other site features to make that content accessible to
users of their site.  It is not intended to be the only way content would be
created for a site, and it should not be construed as an appropriate solution
for everyone.

At its core, the package provides a multi-purpose `Article` class, a view
for articles, and Django CMS plugins which allow the content editor to
place particular articles or article teasers on a CMS page.  Additional
CMS plugins are provided to create article feeds.  For example, you could
place an article feed on a CMS page that displays links to sets of articles
like the following:

* recently updated articles
* upcoming (future) events

The article feeds can optionally be limited by particular article tags
and they are always limited by maximum number of items and maximum event
start time.

Articles can be marked invisible either manually or automatically by a
scheduled task.  Support is provided for marking past events as invisible.

## Planned development in the near term

Currently articles are editable only in the Django admin.  Most content
editors need a wizard-like approach to adding articles, along with autocomplete
and other UI aids to prevent frustration.

## Integrating this in your Django/Django CMS project

* Install the latest version from Github by adding something like
  `git+git://github.com/trawick/emptyhammock-article.git@0.0.1` to your
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

Full-text search can be enabled for the `Article` model, as described in this section.

### Example Postgres setup

A Postgres search configuration will be useful in some circumstances, such as when
searching should ignore accents.  The following commands create a full text search
configuration that ignores accents:

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

This configures Article search to use the search configuration created in the example
above:

```
ARTICLE_SEARCH_SETTINGS = {
    'config': 'english_unaccent',
}
```

## Support

Please open Github issues for suggestions or suspected problems.  Even if I am
unable to respond in a timely basis, the information may quickly become valuable
to others, and I will eventually find time to respond to the issue.
