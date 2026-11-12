"""What does ForeignObject really do with on_delete, and are the system
checks documented in pull request #21173 right?

Guide: https://lindangulopez.github.io/djangonaut-session7/reading-list/guide-21173/

Run it from a folder that holds this file and an empty package ``app/``
(``app/__init__.py`` and ``app/models.py``), with Django 6.1 or later
installed:

    python foreignobject_check.py

The script uses an in-memory SQLite database. Each test builds its own
parent and child models, so one failing relation cannot break another.
Written with the help of Claude (Anthropic), 12 November 2026.
"""

import django
from django.conf import settings

settings.configure(
    INSTALLED_APPS=["app"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
)
django.setup()

from django.db import connection, models  # noqa: E402

counter = 0


def model(name, meta=None, **fields):
    """Create a model class on the fly in the app ``app``."""
    global counter
    counter += 1
    attrs = {"__module__": "app.models", **fields}
    attrs["Meta"] = type("Meta", (), {"app_label": "app", **(meta or {})})
    return type(f"{name}{counter}", (models.Model,), attrs)


def check_ids(*model_classes):
    """System-check error ids for these models (fields and Meta).

    ``databases`` matters: without it, Django skips the checks on
    ``Meta.indexes`` and ``Meta.constraints``, as ``manage.py check`` does
    unless you pass ``--database``.
    """
    return sorted({e.id for m in model_classes for e in m.check(databases=["default"])})


def make_parent():
    return model("Parent", meta={"unique_together": [("a", "b")]},
                 a=models.IntegerField(), b=models.IntegerField())


ON_DELETE = {
    "CASCADE": models.CASCADE,
    "PROTECT": models.PROTECT,
    "RESTRICT": models.RESTRICT,
    "SET_NULL": models.SET_NULL,
    "SET_DEFAULT": models.SET_DEFAULT,
    "SET(0)": models.SET(0),
    "DO_NOTHING": models.DO_NOTHING,
    "DB_CASCADE": models.DB_CASCADE,
    "DB_SET_NULL": models.DB_SET_NULL,
    "DB_SET_DEFAULT": models.DB_SET_DEFAULT,
}


def test_on_delete(label, on_delete):
    """Delete a parent that has one child linked by a ForeignObject."""
    parent = make_parent()
    child = model(
        "Child",
        pa=models.IntegerField(null=True, default=0),
        pb=models.IntegerField(null=True, default=0),
        p=models.ForeignObject(parent, on_delete=on_delete, from_fields=("pa", "pb"),
                               to_fields=("a", "b"), related_name="+"),
    )
    with connection.schema_editor() as editor:
        editor.create_model(parent)
        editor.create_model(child)
    row = parent.objects.create(a=1, b=2)
    child.objects.create(pa=1, pb=2)
    try:
        row.delete()
        kid = child.objects.first()
        result = "child deleted" if kid is None else f"child kept, (pa, pb) = ({kid.pa}, {kid.pb})"
    except Exception as exc:  # noqa: BLE001, we want to see every failure
        result = f"{type(exc).__name__}: {str(exc)[:70]}"
    print(f"  {label:<15} {result}")


def test_checks_on_delete():
    """SET_NULL on fields that cannot be null: ForeignKey vs ForeignObject."""
    parent = make_parent()
    fk_child = model("FKChild", p=models.ForeignKey(parent, on_delete=models.SET_NULL,
                                                    related_name="+"))
    fo_child = model(
        "FOChild",
        pa=models.IntegerField(), pb=models.IntegerField(),
        p=models.ForeignObject(parent, on_delete=models.SET_NULL, from_fields=("pa", "pb"),
                               to_fields=("a", "b"), related_name="+"),
    )
    print(f"  ForeignKey, SET_NULL, not nullable:    {check_ids(fk_child)}")
    print(f"  ForeignObject, SET_NULL, not nullable: {check_ids(fo_child)}")


def test_e049():
    """Is models.E049 about the ForeignObject or about the fields in from_fields?"""
    parent = make_parent()
    fo = dict(
        pa=models.IntegerField(), pb=models.IntegerField(),
        p=models.ForeignObject(parent, on_delete=models.CASCADE, from_fields=("pa", "pb"),
                               to_fields=("a", "b"), related_name="+"),
    )
    on_fo = model("IdxFO", meta={"indexes": [models.Index(fields=["p"], name="idx_fo")]}, **fo)
    fo2 = dict(fo, p=models.ForeignObject(parent, on_delete=models.CASCADE,
                                          from_fields=("pa", "pb"), to_fields=("a", "b"),
                                          related_name="+"))
    on_cols = model("IdxCols", meta={"indexes": [models.Index(fields=["pa", "pb"], name="idx_cols")]},
                    **fo2)
    fo3 = dict(fo, p=models.ForeignObject(parent, on_delete=models.CASCADE,
                                          from_fields=("pa", "pb"), to_fields=("a", "b"),
                                          related_name="+"))
    in_ut = model("UtFO", meta={"unique_together": [("p", "pa")]}, **fo3)
    print(f"  index on the ForeignObject itself:   {check_ids(on_fo)}")
    print(f"  unique_together with the ForeignObject: {check_ids(in_ut)}")
    print(f"  index on the fields in from_fields:  {check_ids(on_cols)}")


def test_to_fields():
    """Which error codes does to_fields raise, and when?"""
    def child(parent):
        return model(
            "TFChild",
            pa=models.IntegerField(), pb=models.IntegerField(),
            p=models.ForeignObject(parent, on_delete=models.CASCADE, from_fields=("pa", "pb"),
                                   to_fields=("a", "b"), related_name="+"),
        )

    no_unique = model("NoUnique", a=models.IntegerField(), b=models.IntegerField())
    print(f"  target without a uniqueness constraint:  {check_ids(child(no_unique))}")

    missing = model("Missing", a=models.IntegerField())
    print(f"  name in to_fields missing on target:     {check_ids(child(missing))}")

    conditional = model(
        "Conditional",
        meta={"constraints": [models.UniqueConstraint(fields=["a", "b"], name="uniq_cond",
                                                      condition=models.Q(a__gt=0))]},
        a=models.IntegerField(), b=models.IntegerField(),
    )
    print(f"  UniqueConstraint with a condition:       {check_ids(child(conditional))}")

    plain = model(
        "Plain",
        meta={"constraints": [models.UniqueConstraint(fields=["a", "b"], name="uniq_plain")]},
        a=models.IntegerField(), b=models.IntegerField(),
    )
    print(f"  UniqueConstraint without a condition:    {check_ids(child(plain))}")


print(f"Django {django.get_version()}, {connection.vendor}\n")
print("1. Deleting the parent, for each on_delete option")
for label, option in ON_DELETE.items():
    test_on_delete(label, option)
print("\n2. System checks for on_delete")
test_checks_on_delete()
print("\n3. models.E049 (from_fields)")
test_e049()
print("\n4. to_fields checks")
test_to_fields()
