# Reading list

## Django documentation, in reading order

1. [The Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/), parts 1 to 8. Checklist on [Tutorials](tutorials.md).
2. [Models](https://docs.djangoproject.com/en/stable/topics/db/models/) and [Making queries](https://docs.djangoproject.com/en/stable/topics/db/queries/).
3. [Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/).
4. [Database transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/).
5. [Unit tests](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/): how to run Django's own test suite.
6. [Triaging tickets](https://docs.djangoproject.com/en/dev/internals/contributing/triaging-tickets/): what the stages and flags on a ticket mean.

## The ORM, from the inside

- ["Demystifying the Django ORM"](https://www.youtube.com/watch?v=IakfTkQIuFw), Simon Charette's talk to Djangonaut Space Session 3 (2024, 44 minutes), with [slides](http://charettes.name/djangonauts2024/). How a QuerySet becomes SQL and comes back as model instances, in four phases: resolving, compilation, execution, construction. His tip from the questions: use `git blame` on a line to walk back to its pull request and ticket.

## Accessibility tools

- [An Orca screen reader tutorial](https://diff.wikimedia.org/2020/07/02/an-orca-screen-reader-tutorial/) (Wikimedia, 2020): installing and using Orca, the screen reader on Linux, as a sighted developer.
- [Accessibility Insights for Web](https://accessibilityinsights.io/docs/web/overview/): the browser extension I use to check a page before and after a change, in Microsoft Edge. Watched: [Introduction to Accessibility Insights for Web](https://www.youtube.com/watch?v=XVvBJoEe4Is) (Accessibility Insights channel), a walk through the extension.

## Reviewing pull requests

- [Getting started with Django PR reviews](https://gist.github.com/ontowhee/a86b146541f849e98ff77c447e69c823), a gist with a method I intend to follow.

## The programme's learning material, by week

From the Djangonaut Space workbook. I do not plan to read all of it.

**Week 1**

- [Becoming a Django Fellow](https://djangochat.com/episodes/becoming-a-django-fellow-natalia-bidart) (1 hour)
- [Your web framework needs you](https://www.youtube.com/watch?v=1BFjg9XtptM) (15 minutes)
- [Intro to sprints at Django](https://www.youtube.com/watch?v=MgpMh2aXzWM) (45 minutes)

**Week 2, documentation**

- [Diátaxis](https://diataxis.fr/), the documentation framework Django uses
- [Read the Docs documentation guide](https://docs-guide.readthedocs.io/en/latest/writing/)
- [Google's technical writing resources](https://developers.google.com/tech-writing/resources)
- [Docs or it didn't happen!](https://www.youtube.com/watch?v=gwVxNHO9Lh0) (45 minutes)

**Week 3, working together**

- [When to pair program and when to go solo](https://nikoheikkila.fi/blog/when-to-pair-program-and-when-to-go-solo/)
- [Mob programming: a whole team approach](https://youtu.be/SHOVVnRB4h0) (55 minutes)

**Week 4, blogging**

- [Just write](https://www.sarasoueidan.com/desk/just-write/)
- [Blogging articles by Juha-Matti Santala](https://hamatti.org/blog/blogging/)

**Week 5, testing and debugging**

- [Testing at Django](https://www.youtube.com/watch?v=EHyKzPQFXzo) (1 hour)
- [Debugging at Django](https://www.youtube.com/watch?v=5fheDDj3oHY) (1 hour)
- [Profiling in Python](https://realpython.com/python-profiling/)

**Week 6, community and review**

- [Ned Batchelder's PyCon 2023 keynote on community](https://www.youtube.com/watch?v=n5QaOADqSyY&t=177s) (45 minutes)
- [How to be an open source gardener](https://steveklabnik.com/writing/how-to-be-an-open-source-gardener)
- [Guidelines for a healthy code review culture](https://www.mediawiki.org/wiki/Guidelines_for_a_healthy_code_review_culture)

**Week 7, accessibility**

- [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)
- [Django accessibility for everyone](https://www.youtube.com/watch?v=bflB8xZmSNw) (30 minutes)
- [Setting up a screen reader testing environment](https://www.sarasoueidan.com/blog/testing-environment-setup/)

**Week 8, giving back**

- [Django Software Foundation's future](https://wsvincent.com/dsf-board-future/)
- [Coworking with a friend to write more](https://jacobian.org/2021/mar/9/coworking-to-write-more/)

## AI tools

A [survey of the AI policies of 108 open source projects](https://bzg.fr/floss-ai-policies/) codes Django as conditional, with disclosure required ([Django's entry](https://bzg.fr/floss-ai-policies/django.html)). I have not yet read Django's own text, and I will before my first comment or pull request.

My rule for this session: I say in each contribution what an AI tool was used for. This site was written with the help of Claude.
