# Setup

## Repositories

| Repository | What it is for |
| --- | --- |
| [lindangulopez/django](https://github.com/lindangulopez/django) | My fork of Django. One branch per ticket. |
| [lindangulopez/django-local-test](https://github.com/lindangulopez/django-local-test) | My fork of a small starter project for running code against a local copy of Django. Notes per ticket in `notes/`, one `ticket-*` branch per reproduction, a `boilerplate` branch to start from. |
| [lindangulopez/code.djangoproject.com](https://github.com/lindangulopez/code.djangoproject.com) | My fork of the configuration of Django's ticket tracker, for the accessibility audit. |

## Later, if there is time: PostgreSQL with statement logging

None of this has been run yet. The commands are the plan, and I will correct them here once they work.

(i) Bring the Django clone up to date with upstream main, on a new branch.

(ii) Start PostgreSQL in Docker with every statement logged:

```bash
docker run --name pg-django -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres \
  -c log_statement=all
docker logs -f pg-django
```

(iii) Point the polls project at it and run `python manage.py migrate`. The log should show each `BEGIN`, `CREATE TABLE`, `COMMIT` and the `INSERT INTO django_migrations`.

## Later, if there is time: the executor tests

Run the two existing tests for the migration executor, from the `tests/` directory of the Django clone:

```bash
./runtests.py migrations.test_executor
```

By default this runs on SQLite. Running it on PostgreSQL needs a settings file, described in the [unit tests guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/#using-another-settings-module).
