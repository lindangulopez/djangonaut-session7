# GeoDjango track: Django, PostgreSQL and QGIS

**From mid-December 2026, after Session 7.** Written on 15 November 2026, with the help of Claude. It is a plan, so it will change.

Session 7 ends on 6 December. This track joins what I learned in it to the work I already know: GIS. Django has a geographic framework built in, [GeoDjango](https://docs.djangoproject.com/en/6.1/ref/contrib/gis/) (`django.contrib.gis`). With PostgreSQL and its PostGIS extension, a Django model can store points, lines and polygons, and QGIS can open the same table as a map layer.

## The task

Six weekend sessions of about 1.5 to 2 hours, from Saturday 19 December 2026 to Saturday 23 January 2027. By the end I can:

(i) set up a Django project on PostgreSQL with PostGIS, and say what each setting does;

(ii) write a model with a geometry field, and read the SQL its migration creates;

(iii) query by distance in the Django shell, and explain why the units matter;

(iv) open the same table in QGIS, edit a point there, and see the change in the Django admin;

(v) serve the data as GeoJSON and load it in QGIS from a URL;

(vi) publish the project as a public repository that I can explain line by line.

The example is small and real: **a register of trees in the Forest of Fontainebleau**, with a name, species, girth, date and location for each. I record a few trees myself, on public land only.

## What I start from

On my laptop (Ubuntu 24.04), checked on 15 November 2026: PostgreSQL 16.15, PostGIS 3.4.2, GDAL 3.8.4, GEOS 3.12.1, PROJ 9.4.0, QGIS 3.34.4 and Python 3.12.3 are already installed. GeoDjango needs GDAL, GEOS and PROJ, so nothing more has to be installed system-wide. The latest Django release on PyPI is 6.1.3.

## Session 1, Sat 19 Dec: a PostGIS database and a GeoDjango project

- [ ] Start PostgreSQL, which is installed but stopped: `sudo systemctl start postgresql`.
- [ ] Create a database role with my own login name, so Django can connect without a password through the local socket ("peer" authentication): `sudo -u postgres createuser --createdb linda`.
- [ ] Add PostGIS to `template1`, so every new database has it, including the test database Django makes when tests run: `sudo -u postgres psql -d template1 -c "CREATE EXTENSION postgis;"`.
- [ ] Create the database: `createdb trees`, then check: `psql -d trees -c "SELECT postgis_full_version();"`.
- [ ] New project in `~/Github/geodjango-trees`, with a virtual environment: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install "Django==6.1.3" "psycopg[binary]"`, then `django-admin startproject config .` and `python manage.py startapp trees`.
- [ ] In `config/settings.py`: add `"django.contrib.gis"` and `"trees"` to `INSTALLED_APPS`, and set the database:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "trees",
    }
}
```

With no `USER`, `PASSWORD` or `HOST`, Django connects as my login name through the local socket.

- [ ] `python manage.py check` runs with no errors.

**Output:** a note, in my own words: what PostGIS adds to PostgreSQL, and why the extension goes in `template1`.

## Session 2, Sat 26 Dec: a model with a geometry field, the admin map

- [ ] In `trees/models.py`, the model. Note the import: `models` comes from `django.contrib.gis.db`, not `django.db`.

```python
from django.contrib.gis.db import models


class Tree(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    girth_cm = models.PositiveIntegerField(null=True, blank=True)
    recorded_on = models.DateField()
    location = models.PointField(srid=4326)  # longitude, latitude (WGS 84)

    def __str__(self):
        return self.name
```

- [ ] `python manage.py makemigrations trees`, then read the SQL before applying it: `python manage.py sqlmigrate trees 0001`. Find the `geometry(POINT,4326)` column and the `GIST` index. This follows on from my Session 7 note on what `migrate` does.
- [ ] `python manage.py migrate`, then `python manage.py createsuperuser`.
- [ ] In `trees/admin.py`, register the model with the map widget:

```python
from django.contrib.gis import admin

from .models import Tree

admin.site.register(Tree, admin.GISModelAdmin)
```

- [ ] `python manage.py runserver`, open `/admin/`, and add five trees by clicking on the OpenStreetMap map.

**Output:** five trees in the database, and the `sqlmigrate` output kept in the repository's notes.

## Session 3, Sat 2 Jan: spatial queries in the shell

In `python manage.py shell`:

```python
from django.contrib.gis.db.models.functions import Distance, Transform
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from trees.models import Tree

here = Point(2.70, 48.40, srid=4326)  # x is longitude, y is latitude

# Trees within 2 km
Tree.objects.filter(location__distance_lte=(here, D(km=2)))

# All trees, nearest first, with the distance
for t in Tree.objects.annotate(d=Distance("location", here)).order_by("d"):
    print(t.name, round(t.d.m), "m")

# The same points in Lambert-93 (EPSG:2154), the official projection for mainland France, in metres
Tree.objects.annotate(l93=Transform("location", 2154)).values_list("name", "l93")
```

- [ ] Run each query and print its SQL with `print(queryset.query)`: find `ST_Distance`, `ST_DWithin` or `ST_Transform`.
- [ ] Try `location__dwithin=(here, D(km=2))`. With SRID 4326 on a geometry field, Django refuses a `D()` distance for `dwithin`, because the units of that field are degrees. Read the error, then explain the difference between `dwithin` and `distance_lte` ([GeoDjango distance lookups](https://docs.djangoproject.com/en/6.1/ref/contrib/gis/db-api/#distance-lookups)).

**Output:** a note: degrees against metres, and when I would store the data in Lambert-93 instead.

## Session 4, Sat 9 Jan: the same table in QGIS

- [ ] In QGIS, Browser panel, **PostgreSQL → New Connection**: name `trees (local)`, Host left empty (the local socket), Port 5432, Database `trees`. Test the connection. If QGIS refuses it, give the role a password (`ALTER ROLE linda PASSWORD '...'`) and use Host `localhost`.
- [ ] Open the `public.trees_tree` layer. Style the points by `species`, and label them with `name`.
- [ ] Toggle editing, move one tree, change its girth, save. Refresh the Django admin: the change is there.
- [ ] One rule: **Django's migrations own the table's structure.** I edit rows in QGIS, never columns. A new field goes in `models.py` and a migration.

**Output:** a QGIS project file (`trees.qgz`) in the repository, and a screenshot of the map.

## Session 5, Sat 16 Jan: GeoJSON out, and a test

- [ ] A view that serves every tree as GeoJSON, in `trees/views.py`:

```python
from django.core.serializers import serialize
from django.http import HttpResponse

from .models import Tree


def trees_geojson(request):
    data = serialize(
        "geojson",
        Tree.objects.all(),
        geometry_field="location",
        fields=["name", "species", "girth_cm", "recorded_on"],
    )
    return HttpResponse(data, content_type="application/geo+json")
```

Then the URL `trees.geojson` in `config/urls.py`: `path("trees.geojson", trees_geojson)`.

- [ ] In QGIS, **Layer → Add Layer → Add Vector Layer**, source type Protocol HTTP(S), URL `http://127.0.0.1:8000/trees.geojson`. The same trees appear, this time read through Django.
- [ ] A first test, in `trees/tests.py`. Two trees 7.4 km apart; only one is within 2 km:

```python
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.test import TestCase

from .models import Tree


class DistanceTests(TestCase):
    def test_only_the_near_tree_is_within_2_km(self):
        here = Point(2.70, 48.40, srid=4326)
        Tree.objects.create(name="A", species="Quercus robur",
                            recorded_on="2027-01-16", location=here)
        Tree.objects.create(name="B", species="Fagus sylvatica",
                            recorded_on="2027-01-16",
                            location=Point(2.80, 48.40, srid=4326))
        near = Tree.objects.filter(location__distance_lte=(here, D(km=2)))
        self.assertEqual([t.name for t in near], ["A"])
```

- [ ] `python manage.py test trees` passes. (Django creates `test_trees` from `template1`, which already has PostGIS since session 1.)

**Output:** the GeoJSON layer in QGIS, and a passing test.

## Session 6, Sat 23 Jan: publish it, and read one GIS ticket

- [ ] Public repository `geodjango-trees`: a README I can explain (what it does, how to run it, the six steps), a licence, a `codemeta.json`, and a `.gitignore` that keeps `.venv/` out.
- [ ] Archive it in Software Heritage and add the SWHID to the README.
- [ ] Read one open GeoDjango ticket on Django's tracker ([open tickets, component GIS](https://code.djangoproject.com/query?status=!closed&component=GIS)), with what the five sessions taught. Reading only, as with ticket #37416.

**Output:** the public repository with its SWHID, ready to show at FOSDEM (29–31 January 2027).

## If the plan breaks

- **A weekend is lost over the holidays.** Measure: sessions 3 and 5 can shrink to their output alone; the QGIS session (4) keeps its place.
- **QGIS will not connect.** Measure: the password and `localhost` route in session 4; if it still fails, export a GeoPackage with `ogr2ogr` and keep going.
- **Not ready by 23 January.** Measure: the repository goes public anyway, with what works, and the README says what is left.

## How I will know it worked

By 23 January 2027: (i) the trees app runs on PostGIS with a passing test, (ii) the same data opens in QGIS from the database and from GeoJSON, (iii) the repository is public with a SWHID. Results, not intentions.
