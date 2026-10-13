# Tutorials

Phase 1, weeks 1 to 4. I do these before I touch a ticket. I tick each box when the code runs on my machine, and reading alone does not count.

## The Django tutorial

The polls app, in eight parts. Links go to the stable documentation.

- [ ] [Part 1](https://docs.djangoproject.com/en/stable/intro/tutorial01/): a project, an app, a first view. Requests and responses.
- [ ] [Part 2](https://docs.djangoproject.com/en/stable/intro/tutorial02/): the database, models, a first migration, the admin site.
- [ ] [Part 3](https://docs.djangoproject.com/en/stable/intro/tutorial03/): views and templates.
- [ ] [Part 4](https://docs.djangoproject.com/en/stable/intro/tutorial04/): forms and generic views.
- [ ] [Part 5](https://docs.djangoproject.com/en/stable/intro/tutorial05/): automated tests.
- [ ] [Part 6](https://docs.djangoproject.com/en/stable/intro/tutorial06/): static files.
- [ ] [Part 7](https://docs.djangoproject.com/en/stable/intro/tutorial07/): customising the admin site.
- [ ] [Part 8](https://docs.djangoproject.com/en/stable/intro/tutorial08/): third-party packages.

Part 2 and part 5 matter most for what follows: part 2 is where migrations first appear, and part 5 is how Django expects a change to be proven.

## ORM topic guides

Week 4, once the polls app works.

- [ ] [Models](https://docs.djangoproject.com/en/stable/topics/db/models/): fields, relationships, `Meta`.
- [ ] [Making queries](https://docs.djangoproject.com/en/stable/topics/db/queries/): `QuerySet`, lookups, related objects.
- [ ] [Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/): `makemigrations`, `migrate`, `sqlmigrate`, `showmigrations`, the `django_migrations` table.
- [ ] [Database transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/): `BEGIN`, `COMMIT`, `transaction.atomic`.

Output of the week: a short note, in my own words, on what `migrate` does between `BEGIN` and `COMMIT`.

## Contributing tutorial

- [x] [Writing your first contribution for Django](https://docs.djangoproject.com/en/dev/intro/contributing/): done before the session, with a practice patch.

## Where the code lives

The polls project goes in my fork of [django-local-test](https://github.com/lindangulopez/django-local-test), so that the same project can later run against a local copy of Django. See [Setup](setup.md).

If the tutorials take longer than four weeks, they keep the priority and the contribution gets smaller. See [Learning path](learning-path.md).
