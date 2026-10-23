# Tutorials

Phase 1, on weekends from 24 October to 22 November (reset on 23 October: I can only really work on weekends). The plan was to do these before touching a ticket; #2904 came first. I tick each box when the code runs on my machine, and reading alone does not count.

## The Django tutorial

The polls app, in eight parts. Links go to the stable documentation.

- [ ] [Part 1](https://docs.djangoproject.com/en/stable/intro/tutorial01/) (weekend of 24–25 Oct): a project, an app, a first view. Requests and responses.
- [ ] [Part 2](https://docs.djangoproject.com/en/stable/intro/tutorial02/) (weekend of 24–25 Oct): the database, models, a first migration, the admin site.
- [ ] [Part 3](https://docs.djangoproject.com/en/stable/intro/tutorial03/) (weekend of 31 Oct–1 Nov): views and templates.
- [ ] [Part 4](https://docs.djangoproject.com/en/stable/intro/tutorial04/) (weekend of 7–8 Nov): forms and generic views.
- [ ] [Part 5](https://docs.djangoproject.com/en/stable/intro/tutorial05/) (weekend of 7–8 Nov): automated tests.
- [ ] [Part 6](https://docs.djangoproject.com/en/stable/intro/tutorial06/) (weekend of 14–15 Nov): static files.
- [ ] [Part 7](https://docs.djangoproject.com/en/stable/intro/tutorial07/) (weekend of 14–15 Nov): customising the admin site.
- [ ] [Part 8](https://docs.djangoproject.com/en/stable/intro/tutorial08/) (weekend of 14–15 Nov): third-party packages.

Part 2 and part 5 matter most for what follows: part 2 is where migrations first appear, and part 5 is how Django expects a change to be proven.

## ORM topic guides

Weekend of 21–22 November, once the polls app works. Database transactions if there is time.

- [ ] [Models](https://docs.djangoproject.com/en/stable/topics/db/models/): fields, relationships, `Meta`.
- [ ] [Making queries](https://docs.djangoproject.com/en/stable/topics/db/queries/): `QuerySet`, lookups, related objects.
- [ ] [Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/): `makemigrations`, `migrate`, `sqlmigrate`, `showmigrations`, the `django_migrations` table.
- [ ] [Database transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/): `BEGIN`, `COMMIT`, `transaction.atomic`.

Output of the week: a short note, in my own words, on what `migrate` does between `BEGIN` and `COMMIT`.

## Contributing tutorial

- [x] [Writing your first contribution for Django](https://docs.djangoproject.com/en/dev/intro/contributing/): done before the session, with a practice patch.

## Where the code lives

The polls project goes in my fork of [django-local-test](https://github.com/lindangulopez/django-local-test), so that the same project can later run against a local copy of Django. See [Setup](setup.md).

If the tutorials take longer than four weekends, they keep the priority and the contribution gets smaller. See [Learning path](learning-path.md).
