# Guide: run djangoproject.com locally

How I run the code of [www.djangoproject.com](https://www.djangoproject.com/) on my laptop, with the docs and dashboard sites, from the [`README.rst`](https://github.com/django/djangoproject.com/blob/main/README.rst) of [django/djangoproject.com](https://github.com/django/djangoproject.com). Written on 24 October 2026, on Ubuntu 24.04 with Docker 29 and Docker Compose 2.40, while working on [issue #2904](guide-2904.md). I wrote it with Claude's help.

As part of my [accessibility track](../accessibility-track.md), I also created [issue #2929](https://github.com/django/djangoproject.com/issues/2929) on the same repository. It proposes adding a `CONTRIBUTING.md` and a `codemeta.json`, and optionally an `AUTHORS` file and a `CITATION.cff`. The repository has no contributor guide yet, so a new contributor starts from the README, as this guide does.

The README gives two ways: (i) a Python 3.12 virtual environment with a local PostgreSQL, or (ii) **docker compose**. I use docker compose: it starts PostgreSQL for you, and the container already has `gettext` and the build tools.

## Step 0: fork, clone, branch

```bash
gh repo fork django/djangoproject.com --clone
cd djangoproject.com
git remote -v        # origin = my fork, upstream = django/djangoproject.com
```

To run the site as it is today, use an up-to-date `main`. To test a fix, stay on its branch.

```bash
git fetch upstream
git switch main && git merge --ff-only upstream/main
```

## Step 1: build and start

```bash
docker compose build
docker compose up
```

Keep this terminal open. On start, the entrypoint (`docker-entrypoint.dev.sh`) runs the migrations, compiles the SCSS and collects the static files. A second container, `db`, runs PostgreSQL 17.

## Step 2: load the local data

In a second terminal:

```bash
docker compose run --rm web make reset-local-db
```

!!! warning "This empties the local database"

    `reset-local-db` starts with `manage flush`, then loads the site hostnames (`dev_sites`), the doc releases (`doc_releases`) and the dashboard metrics. Its last step, `update_metrics`, calls external APIs, so it needs a network connection and takes a minute or two.

## Step 3: create an admin account

`reset-local-db` does not create one.

```bash
docker compose run --rm web python -m manage createsuperuser
```

## Step 4: open the sites

| Site | Local URL |
| --- | --- |
| www | <http://www.djangoproject.localhost:8000/> |
| dashboard | <http://dashboard.djangoproject.localhost:8000/> |
| admin | <http://www.djangoproject.localhost:8000/admin/> |
| docs | <http://docs.djangoproject.localhost:8000/>, only after step 5 |
| contact form, the page of [issue #2904](guide-2904.md) | <http://www.djangoproject.localhost:8000/contact/foundation/> |

To check whether the site is already up, from the repository:

```bash
docker compose ps          # web should be Up, with 0.0.0.0:8000->8000/tcp
ss -ltnp | grep :8000      # something is listening on the host port
```

### Subdomain routing, or why `localhost:8000` does not work

All three sites are one Django process on one port. `http://localhost:8000/` gives a 400 page, `DisallowedHost at /`, not the home page. That is not a broken install: this project routes on the **hostname**, not on the path.

Two settings do it:

- `ALLOWED_HOSTS` in `djangoproject/settings/dev.py` lists the four names Django will answer to: `djangoproject.localhost` and its `www`, `docs` and `dashboard` subdomains. `localhost` is not one of them, so Django refuses the request before any view runs. (Django's usual "`localhost` works in `DEBUG`" shortcut only applies when `ALLOWED_HOSTS` is empty, and here it is not.)
- [`django-hosts`](https://django-hosts.readthedocs.io/) then chooses the URLconf from the subdomain, in `djangoproject/hosts.py`:

```python
host_patterns = [
    host(r"www", settings.ROOT_URLCONF, name="www"),          # djangoproject.urls.www
    host(r"docs", "djangoproject.urls.docs", name="docs"),
    host(r"dashboard", "dashboard.urls", name="dashboard"),
]
```

`PARENT_HOST` (`djangoproject.localhost:8000` in dev, `djangoproject.com` in production) is the part stripped off before matching, and `DEFAULT_HOST = "www"` is the fallback, which is why the bare `http://djangoproject.localhost:8000/` also gives the www site. So the same code serves three sites, and a `{% host_url %}` link can point from one to another in both dev and production without hardcoding a domain.

The names resolve without any configuration on most systems: `.localhost` is reserved for the local machine ([RFC 6761](https://www.rfc-editor.org/rfc/rfc6761#section-6.3)), and resolvers and browsers send any `*.localhost` name to 127.0.0.1. If yours does not, add the line to `/etc/hosts`:

```text
127.0.0.1 www.djangoproject.localhost docs.djangoproject.localhost dashboard.djangoproject.localhost
```

To see the routing from the command line, send the hostname by hand, the port included, because `PARENT_HOST` carries it:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: www.djangoproject.localhost:8000" http://127.0.0.1:8000/   # 200
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: localhost:8000"                   http://127.0.0.1:8000/   # 400
```

## Step 5: build the docs, one version only

The docs site does not ship with the docs. Until you build them, <http://docs.djangoproject.localhost:8000/en/6.1/> gives a 404 like this one:

```text
Page not found (404)
data/djangodocs/en/6.1/_built/json
Raised by: docs.views.document
```

The path in the error is the folder the page reads from. It does not exist yet.

The README says `python -m manage update_docs`, which builds **every** version in every language and takes a long time. The command takes a version and a language, so build only the default one:

```bash
docker compose exec web python -m manage update_docs 6.1 --language en
```

This clones Django's docs and runs Sphinx several times (JSON, HTML, gettext), which took a few minutes for me. The `_built/` folder only appears at the very end, so the page keeps giving the same 404 while the build runs. When it ends with `build succeeded`, reload the page.

!!! note "Two things that look like errors and are not"

    (i) `--link-dest arg does not exist` on the last line: the build copies the new files next to the previous build, and on a first build there is no previous one. The command still exits with code 0.

    (ii) Other versions and languages, `/en/dev/` or `/fr/6.1/`, still give a 404. Build them the same way when you need them, for example `update_docs dev --language en`.

To find which versions are loaded, look at the `DocumentRelease` objects in the admin, or:

```bash
docker compose exec web python -m manage shell -c \
  "from docs.models import DocumentRelease as D; print(list(D.objects.values_list('lang', 'release__version', 'is_default')))"
```

## Step 6: run the tests

```bash
docker compose run --rm web python -m manage test
```

## Step 7: stop

```bash
docker compose down       # keeps the database volume
docker compose down -v    # deletes it too
```

## If you use the virtual environment instead

Three things the README does not say, which I hit on my laptop:

(i) `make compilemessages` needs `msgfmt`. On Ubuntu, `gettext-runtime` alone is not enough: `sudo apt install gettext`.

(ii) The README installs with `pip install -r requirements/dev.txt`, but the repository also has a `pyproject.toml` and a `uv.lock`, so `uv sync` works too.

(iii) PostgreSQL has to be running, with the two databases and users of `secrets.json` (`djangoproject` and `code.djangoproject`). A compose `db` container left running uses port 5432 inside Docker, not on the host, so it does not conflict.

Which of these should go back into the README as a pull request?
