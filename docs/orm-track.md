# ORM track: ticket #37416

[Ticket #37416](https://code.djangoproject.com/ticket/37416), "Migrations are not recorded atomically", was opened on 11 October 2026 in the component "Database layer (models, ORM)". On that day it was Unreviewed, with no owner and no patch. I have not checked its state since.

## What the bug is

- A migration applies its operations in a transaction. Django then writes a row in the `django_migrations` table to record that the migration was applied.
- When the migration has deferred SQL, for example a `CreateModel` with a foreign key, the row is written **after** the transaction has committed. A crash between the two steps leaves an applied migration that Django will try to run again.
- Where: `MigrationExecutor.apply_migration` in `django/db/migrations/executor.py`. `record_migration()` is called inside the `schema_editor` block only when `schema_editor.deferred_sql` is empty.
- History: ticket [#29721](https://code.djangoproject.com/ticket/29721) made the recording atomic. The fix of [#32374](https://code.djangoproject.com/ticket/32374) moved it out again for migrations with deferred SQL, so that a migration is not marked as applied when its deferred SQL fails.
- Two existing tests are the way in, both in `tests/migrations/test_executor.py`: `test_migrations_applied_and_recorded_atomically` and `test_migrations_not_applied_on_deferred_sql_failure`.

!!! note "Read, not reproduced"
    I read this code path on Django's main branch on 11 October 2026, with the help of Claude. I have not run it. The reproduction was planned for week 5; since 23 October, with weekends only, this track is reading and the reproduction is on hold.

## What I aim to contribute

The reporter has proposed two designs and asked which one is preferred, so the fix is probably not mine to write. The ticket may also be closed or changed at triage. My aim is a visible, useful contribution by 6 December, in this order of likelihood:

1. An independent reproduction posted on the ticket, on PostgreSQL and on SQLite.
2. A review of the reporter's pull request, tested locally on more than one database.
3. A regression test, offered to the reporter, or submitted as my own pull request if the reporter agrees.
4. Stretch: the fix itself, only if the ticket is accepted, nobody has claimed it and the reporter says go ahead.

Items 1 to 3 are contributions Django recognises, and each one teaches me the migrations code.

## What I need to learn first

(i) How migrations work from the outside: [Tutorials](tutorials.md), part 2 and the Migrations guide.

(ii) What "atomic" means for a migration, and why MySQL cannot roll back schema changes.

(iii) How a regression test is written so that it fails before the fix and passes after.

Is a reproduction from a newcomer useful on an Unreviewed ticket, or should it wait until the ticket is accepted?
