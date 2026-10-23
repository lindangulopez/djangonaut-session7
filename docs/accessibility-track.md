# Accessibility track

Accessibility is my team's project in this session. These are the tickets and pull requests I looked at. Pull request states were read on GitHub on 13 October 2026. I have not verified the ticket fields on Django's tracker.

## Working on now

**[djangoproject.com issue #2904](https://github.com/django/djangoproject.com/issues/2904)**: on the Django Software Foundation's [contact form](https://www.djangoproject.com/contact/foundation/), the E-mail field renders as a plain text input, so a phone shows the ordinary keyboard instead of the e-mail one, and neither Name nor E-mail tells the browser what it is for, so autofill is unreliable. That second point is [WCAG 2.2 success criterion 1.3.5, Identify Input Purpose](https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html), level AA.

State on 15 October 2026: assigned to me. The plan: fix it, step by step, to learn: reproduce it on a local copy of the site, write a test that fails, make the change, check the page again with a screen reader and Accessibility Insights, then open a pull request. No pull request yet.

It is a small change to the website, not to Django itself, and it uses what tutorial parts 4 (forms) and 5 (tests) teach.

### Update, 23 October 2026: fixed on a branch, pull request next

**A false "fixed".** On my phone the form already answered "Enter a valid email address.", so the bug looked solved. It was not. That message is Django's server-side check, which `forms.EmailField` runs *after* you submit. The issue is about the input *before* you submit: which keyboard the phone shows, and whether autofill knows what the field is for. To test it, tap the field and look at the keyboard. Don't submit.

**Where the bug was.** In `contact/forms.py`, class `BaseContactForm`, each field passed its own widget:

```python
email = forms.EmailField(
    widget=forms.TextInput(attrs={"class": "required"}),  # line 28
    ...
name = forms.CharField(
    widget=forms.TextInput(attrs={"class": "required"}),  # line 32
```

An `EmailField` renders as `<input type="email">` by default, but an explicit `TextInput` widget overrides that. The field is what validates; the widget is what gets drawn. The two sponsorship forms inherit these fields, so one change fixes all three forms.

**The fix.**

```python
email = forms.EmailField(
    widget=forms.EmailInput(attrs={"class": "required", "autocomplete": "email"}),
    label=_("E-mail"),
)
name = forms.CharField(
    widget=forms.TextInput(attrs={"class": "required", "autocomplete": "name"}),
    label=_("Name"),
)
```

**The test first.** I added a test to `ContactFormTests` that loads the page and checks the rendered `<input>` of both fields with `assertInHTML`. Before the fix it failed and printed the real input, `<input type="text" name="name" class="required" required id="id_name">`, with no `autocomplete`. After the fix, all 15 tests in the `contact` app pass (`docker compose run --rm web python -m manage test contact`). The Python pre-commit hooks (black, flake8, ruff) pass too.

How: I cloned my fork (a shallow clone with `--depth 50`, because the full history is large), created the branch `contact-email-input-autocomplete` from `upstream/main`, and ran everything in Docker. I wrote the code with Claude's help, so I will tick that box in the pull request's AI Assistance Disclosure.

**Pull request opened, 23 October 2026: [#2924](https://github.com/django/djangoproject.com/pull/2924).** Next: answer the review comments.

## Tickets I could take over

| Ticket | What | Pull request | State on 13 Oct |
| --- | --- | --- | --- |
| [#36510](https://code.djangoproject.com/ticket/36510) | Redundant model name in the admin pagination heading | [#20513](https://github.com/django/django/pull/20513) | Open, 7 lines |
| [#36509](https://code.djangoproject.com/ticket/36509) | Missing label on input fields in admin tables | [#19655](https://github.com/django/django/pull/19655) | Open, last updated July 2026 |

Taking over means asking the author first.

## Pull requests to review, not to take

| Ticket | What | Pull request | State on 13 Oct |
| --- | --- | --- | --- |
| [#36630](https://code.djangoproject.com/ticket/36630) | Admin navigation sidebar as accessible list markup | [#21562](https://github.com/django/django/pull/21562) | Open |
| [#36582](https://code.djangoproject.com/ticket/36582) | `required` attribute on mandatory fields in admin inline forms | [#19970](https://github.com/django/django/pull/19970) | Open |

## Without any Django code

The accessibility review of Django's ticket tracker, [code.djangoproject.com issue #250](https://github.com/django/code.djangoproject.com/issues/250), open on 13 October. One page of the audit is a contribution on its own.

## Skills to build

(i) [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/): enough to name the criterion a ticket is about.

(ii) A screen reader test environment on my own machine, following [Setting up a screen reader testing environment](https://www.sarasoueidan.com/blog/testing-environment-setup/). On Linux this means [Orca](https://diff.wikimedia.org/2020/07/02/an-orca-screen-reader-tutorial/).

(iii) The [Accessibility Insights](https://accessibilityinsights.io/downloads/) browser plugin, to check a page before and after a patch. Installed on 15 October 2026, as a Microsoft Edge extension. I learned it from [Introduction to Accessibility Insights for Web](https://www.youtube.com/watch?v=XVvBJoEe4Is), the tool's own video.

Which of these would you give to someone who has finished the tutorial and nothing more?
