# ORM watchlist

Phase 2, from week 1, alongside the weekend tutorials. I follow these tickets and pull requests to see how ORM work moves through triage and review. I read, I do not comment yet.

## Live queries

These open on Django's tracker and on GitHub, and are always current.

- ORM tickets, unreviewed: [Database layer, Unreviewed](https://code.djangoproject.com/query?status=!closed&component=Database+layer+(models%2C+ORM)&stage=Unreviewed&order=id&desc=1)
- ORM tickets, accepted: [Database layer, Accepted](https://code.djangoproject.com/query?status=!closed&component=Database+layer+(models%2C+ORM)&stage=Accepted&order=changetime&desc=1)
- ORM tickets with a patch waiting for review: [Database layer, has patch](https://code.djangoproject.com/query?status=!closed&component=Database+layer+(models%2C+ORM)&has_patch=1&needs_better_patch=0&needs_tests=0&needs_docs=0&order=changetime&desc=1)
- Migrations tickets, open: [Migrations](https://code.djangoproject.com/query?status=!closed&component=Migrations&order=changetime&desc=1)
- Django pull requests, most recently updated: [django/django](https://github.com/django/django/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc)

## Tickets I follow

Kept by hand. Django's tracker cannot be read automatically, so the stage is the one I saw on the date given. A blank cell means I have not checked.

| Ticket | Summary | Component | Stage | Why I follow it | Checked |
| --- | --- | --- | --- | --- | --- |
| [#37416](https://code.djangoproject.com/ticket/37416) | Migrations are not recorded atomically | Database layer (models, ORM) | Unreviewed | My [ORM track](orm-track.md) | 11 Oct |
| [#37407](https://code.djangoproject.com/ticket/37407) | `UUIDTextMixin.process_rhs()` mutates the lookup's rhs in place | Database layer (models, ORM) | Unreviewed, assigned | How a lookup is compiled to SQL | 11 Oct |
| [#37371](https://code.djangoproject.com/ticket/37371) | Inconsistent behaviour of `--keepdb` with the SQLite backend | Testing framework | Unreviewed, assigned | Test databases, which I need for the reproduction | 11 Oct |
| [#37415](https://code.djangoproject.com/ticket/37415) | Error in the documentation of `connection.execute_wrapper` | Documentation | Unreviewed | A small documentation ticket on the database layer | 11 Oct |
| [#37365](https://code.djangoproject.com/ticket/37365) | `models.E007` and a quoted `db_column` |  |  | System checks on models, see pull request #22015 |  |
| [#34122](https://code.djangoproject.com/ticket/34122) | Reference documentation for `ForeignObject` |  |  | Relations without a foreign key constraint, see pull request #21173 |  |
| [#29721](https://code.djangoproject.com/ticket/29721) | Migrations are not applied atomically |  | Closed, fixed | History of #37416 | 11 Oct |
| [#32374](https://code.djangoproject.com/ticket/32374) | Migrations marked applied when deferred SQL fails |  | Closed, fixed | History of #37416 | 11 Oct |

## Pull requests I follow

States read on GitHub on 13 October 2026.

| Pull request | What | State | Last updated |
| --- | --- | --- | --- |
| [#21173](https://github.com/django/django/pull/21173) | Reference docs for `ForeignObject` (ticket #34122) | Open | 11 Oct 2026 |
| [#22015](https://github.com/django/django/pull/22015) | `models.E007` duplicate column detection with a quoted `db_column` (ticket #37365) | Open | 23 Sept 2026 |
| [#20367](https://github.com/django/django/pull/20367) | Windowing example in the expressions docs | Open | 7 April 2026 |

## How I follow

(i) On the tracker: I add myself to Cc on the ticket, and I get an email at each change.

(ii) On GitHub: I subscribe to the pull request.

(iii) Once a week I open the queries above and move one ticket in or out of the table.

Which ORM ticket taught you the most by watching it?
