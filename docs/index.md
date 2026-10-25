# Djangonaut Space, Session 7

**Linda Angulo Lopez, 13 October 2026**

I am a Djangonaut in [Djangonaut Space](https://djangonaut.space/), Session 7, from 12 October to 6 December 2026. It is an eight-week group mentoring programme for people who want to contribute to [Django](https://www.djangoproject.com/). My team's project is **Accessibility / Django**, and I give it about 4 hours a weekend: since 23 October, weekends are the only time I really have for it.

This site shows what I plan to do, week by week. It is a plan, so it will change.

## Where I start from

I grew up on the Wild Coast in South Africa and trained as a botanist. I am a Full Stack GIS Developer, with more than 25 years of work across Europe and Africa in environmental governance, landscape ecology and research infrastructures, including national ecological restoration programmes in South Africa.

I now focus on the digital commons. Since September 2025 I have been a Partnerships Specialist at Software Heritage, where I work with universities, research organisations and Open Source Program Offices (OSPOs). In parallel, I take part in the Rewilding Academic Talent Program at Rewilding Portugal, with GIS and ecological connectivity analyses for landscape restoration.

Django is new to me. I use Python every day, and my Django experience so far is the contributing tutorial and one practice patch.

## What I want from the eight weeks

(i) To read Django's internals with some comfort, starting with the ORM.

(ii) To make one real contribution: a reproduction, a review, a test, or a fix.

(iii) To learn how a large open source community reviews work and welcomes new contributors.

## Three phases, tutorials first

| Phase | When | What |
| --- | --- | --- |
| **1. Tutorials** | Weekends, 24 Oct to 22 Nov | The official Django tutorial, parts 1 to 8, then four ORM topic guides. See [Tutorials](tutorials.md). |
| **2. Follow** | From week 1, alongside | I read ORM tickets and pull requests as they move, without commenting. See [ORM watchlist](orm-watchlist.md). |
| **3. Contribute** | Weekends, 28 Nov to 6 Dec | Follow-up on my pull request, then a blog post. |

The plan was to contribute only after phase 1, but issue #2904 was assigned to me in week 1 and went first. The weekend-by-weekend table is on [Learning path](learning-path.md).

## Two tracks for the contribution

**ORM.** Ticket [#37416](https://code.djangoproject.com/ticket/37416), "Migrations are not recorded atomically". The aim is a reproduction, a review and a regression test, in that order. See [ORM track](orm-track.md).

**Accessibility.** Small tickets in the Django admin and the accessibility audit of Django's ticket tracker. This is my team's project. See [Accessibility track](accessibility-track.md).

The choice between the two is open with my Navigator. Both stay on this site until it is made.

## Status

- 25 October 2026: [ticket #36510](https://code.djangoproject.com/ticket/36510) (admin pagination heading) is now owned by another Djangonaut. I stepped back and offered to review their pull request and test it with a screen reader. See [Accessibility track](accessibility-track.md#update-25-october-2026-ticket-36510-handed-over-i-will-review-it).
- 24 October 2026: first review on [pull request #2924](https://github.com/django/djangoproject.com/pull/2924). Kanishk asked me to remove the AI co-author line from the commit message. Done the same day: commit amended and force-pushed, code unchanged, waiting for a new review. See [Accessibility track](accessibility-track.md#update-24-october-2026-first-review).
- 23 October 2026: [pull request #2924](https://github.com/django/djangoproject.com/pull/2924) opened for #2904, with a test that failed before the fix and passes after it. See [Accessibility track](accessibility-track.md#update-23-october-2026-fixed-on-a-branch-pull-request-next). Learning path reset to weekends only, tutorials from 24 October. See [Learning path](learning-path.md).
- 15 October 2026: first accessibility issue assigned to me, [djangoproject.com #2904](https://github.com/django/djangoproject.com/issues/2904), the contact form's e-mail field. See [Accessibility track](accessibility-track.md).
- 13 October 2026: week 1. Plan published. Tutorial part 1 not started.

How do you learn a codebase of this size: from the tutorial outwards, or from one bug inwards?
