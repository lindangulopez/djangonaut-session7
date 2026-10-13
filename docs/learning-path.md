# Learning path

Eight weeks, about 4 hours each. Every week ends on one output. The week names are the programme's own.

| Week | Phase | What I do | Output |
| --- | --- | --- | --- |
| **1, 12 Oct**, Blast off! | Tutorials | Tutorial parts 1 and 2: project, models, admin. Light week. | Polls project running locally |
| **2, 19 Oct**, Leaving the atmosphere! | Tutorials | Parts 3 to 5: views, forms, tests. | Polls app with passing tests |
| **3, 26 Oct**, Into orbit! | Tutorials | Parts 6 to 8: static files, admin, third-party packages. Django clone brought up to date, PostgreSQL in Docker with statement logging. | Polls project in `django-local-test`, migrating on PostgreSQL |
| **4, 2 Nov**, Avoiding asteroids! | Tutorials | Topic guides: Models, Making queries, Migrations, Database transactions. Light week. | Note: what `migrate` does, in my own words |
| **5, 9 Nov**, Traveling amongst the stars! | Contribute | Reproduce ticket #37416 on PostgreSQL and SQLite. Read `apply_migration` and the two existing tests. | Statement logs, and a note on the call sequence |
| **6, 16 Nov**, Talking to extraterrestrials | Contribute | Write a failing regression test. | A test that fails on main, on a branch of my fork |
| **7, 23 Nov**, Collecting samples! | Contribute | Review the reporter's pull request on two databases, or offer the test. | One review, or a draft pull request |
| **8, 30 Nov**, Returning home | Wrap up | Follow-up on review comments. Blog post. | Blog post published |

Weeks 5 to 7 are written for the [ORM track](orm-track.md). If the [accessibility track](accessibility-track.md) is chosen, the same three weeks become: (i) reproduce one admin ticket with a screen reader, (ii) review its pull request, (iii) take the patch over if its author agrees.

Alongside, from week 1: the [ORM watchlist](orm-watchlist.md), read once a week.

## If the plan breaks

- **The tutorials take longer than four weeks.** Measure: they keep the priority. The contribution shrinks to the reproduction and one review.
- **Ticket #37416 is closed as invalid or wontfix.** Measure: the reading of weeks 4 and 5 still stands, it is the same code. The contribution moves to the accessibility track.
- **The reporter's pull request is merged before I have reproduced anything.** Measure: I review it after the fact for my own notes, then take the accessibility track.
- **I am asked to stay on accessibility.** Measure: the accessibility track becomes the plan, and #37416 stays as reading.

## How I will know it worked

By 6 December: (i) the polls app runs with its tests, (ii) one contribution is visible on a Django ticket or pull request, (iii) one blog post is published. Results, not intentions.
