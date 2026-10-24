# Guide: issue #2904, step by step

How I fixed [djangoproject.com issue #2904](https://github.com/django/djangoproject.com/issues/2904): on the Django Software Foundation's [contact form](https://www.djangoproject.com/contact/foundation/), the E-mail field rendered as `type="text"`, and neither Name nor E-mail had `autocomplete`. The fix is [pull request #2924](https://github.com/django/djangoproject.com/pull/2924).

The steps and questions were written as a learning guide on 15 October 2026, the day the issue was assigned to me. The answers and notes were added as I worked through it, on 23 October 2026. I wrote the code with Claude's help, as the pull request's AI Assistance Disclosure says. Background and the short version: [Accessibility track](../accessibility-track.md).

## Step 0: understand the problem before touching code

- [x] Open <https://www.djangoproject.com/contact/foundation/> on your phone. Tap the E-mail field. Which keyboard appears?
- [x] On your laptop, open the same page with devtools (F12) and inspect the Name and E-mail inputs. Write down the exact attributes each one has.
- [x] Run **Accessibility Insights for Web** (Ctrl+Shift+K) → FastPass on the page. Does it flag anything about these fields? (It may not: automated tools often miss this one. That is a lesson in itself.) I only saw a lot of colour contrast issues.
- [x] Optional, 15 min: turn on **Orca**, Tab into the form, and listen to how each field is announced. How: [Tutorial: listen to pull request #2924 with Orca](../accessibility-track.md#tutorial-listen-to-pull-request-2924-with-orca-on-ubuntu-with-firefox).
- [x] Read WCAG 2.2 **SC 1.3.5 Identify Input Purpose** (<https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html>) and find the list of input-purpose tokens it points to. Which tokens match "Name" and "E-mail"?

Question to answer in your own words: why does `type` matter for a phone user, and why does `autocomplete` matter for someone for whom typing is slow or painful? These are two different problems.

**Answer:** why they are two different problems:

- `type` makes typing easier.
- `autocomplete` removes the typing.
- A field can have one without the other. Pull request #2924 adds both: `EmailInput` for the type and the `autocomplete` attributes.
- Neither shows up when you listen with Orca. In my test, both fields sounded the same: "entry required". The benefit is in the keyboard and in autofill, not in what a screen reader says. That's why I checked on my phone and in devtools as well.

## Step 1: fork and clone

- [x] Fork the repository with the `gh` CLI and clone your fork into your home folder (look up `gh repo fork --help`: there is a flag that clones in the same command).
- [x] Check your remotes with `git remote -v`. You should see your fork and the upstream repository. Which is which?
- [x] Create a branch for the issue. Look at the branch names of recent merged pull requests (`gh pr list -R django/djangoproject.com --state merged`) and choose a short, descriptive name in the same spirit. Mine: `contact-email-input-autocomplete`.

Hint: never work on `main` of your fork. One branch per issue.

## Step 2: run the site locally

The `README.rst` gives two ways: a virtual environment (Python 3.12 + PostgreSQL), or **docker compose**. Docker is the shorter road.

- [x] Read the "Run with docker compose" section of `README.rst` and follow it: build, start, load the local data.
- [x] Open the local site and find the foundation contact page. Which URL? (Hint: look in `contact/urls.py`, and at the hostnames the README gives.) Answer: <http://www.djangoproject.localhost:8000/contact/foundation/>.
- [x] Inspect the inputs again, locally. You should see exactly what you saw on the live site. If you do, you have **reproduced** the bug. That is the first real milestone.

If docker gives you trouble, write down the exact error and stop there: setup problems are normal and good questions for the team.

## Step 3: read the code

- [x] Open `contact/forms.py` and find `BaseContactForm`. Look at the four fields.
- [x] Question: the e-mail field is a `forms.EmailField`. Which widget does Django give an `EmailField` **by default**? Find it in the Django docs: "Form fields" → `EmailField` → "Default widget". Then look at which widget this form passes instead.

    **Answer:** the default widget is **`EmailInput`** ([Form fields → `EmailField`](https://docs.djangoproject.com/en/6.1/ref/forms/fields/#emailfield), Django 6.1), which renders `<input type="email">`. The form passes **`TextInput`** instead: `widget=forms.TextInput(attrs={"class": "required"})`, which renders `<input type="text">`. Passing a widget replaces the default, so the field still validates like an e-mail field but is drawn as a plain text box. That is the bug in #2904. The fix in #2924 passes `forms.EmailInput(attrs={"class": "required", "autocomplete": "email"})`.

- [x] Question: what does a widget's `attrs` dict do? (Django docs: "Widgets" → "Styling widget instances".)

    **Answer:** `attrs` is a dictionary of extra HTML attributes: Django adds each key and value to the tag when it renders the widget ([Widgets → `Widget.attrs`](https://docs.djangoproject.com/en/6.1/ref/forms/widgets/#django.forms.Widget.attrs), Django 6.1). It changes only how the field is drawn, not how the data is validated. Example: `forms.TextInput(attrs={"size": 10, "title": "Your name"})` renders `<input title="Your name" type="text" name="name" value="A name" size="10">`. `True`/`False` values become HTML boolean attributes (`{"required": True}` gives `required`). You can set it when creating the widget, or later with `field.widget.attrs.update({...})` (for model form fields, through `self.fields[...]`). In #2904 the form used `attrs={"class": "required"}`; the fix in #2924 keeps that class and adds `"autocomplete": "email"` / `"autocomplete": "name"` in the same dict.

- [x] Use `git blame` on the e-mail field line (or the "Blame" view on GitHub) and follow it back to the commit that introduced it. Was the `TextInput` a deliberate choice or an accident of history? (This is Simon Charette's tip from the ORM talk: blame, then walk back to the pull request.)

    **Answer: an accident of history.** Blame is on the *file* page, not the commit page: open `contact/forms.py` on GitHub and click **Blame**; "blame prior to this change" goes one step further back. The E-mail line, walked back:

    | Date | Commit | What happened to the E-mail line |
    | --- | --- | --- |
    | 16 Nov 2014 | [07a8182](https://github.com/django/djangoproject.com/commit/07a818210624e4f475f959463da9fb20d8e11fa0), PR #166 "Redesign 2014" | E-mail is a `CharField`; `TextInput` is passed only to add a class and a placeholder. Right widget for a `CharField`. |
    | 5 Jan 2016 | [b3f5d57](https://github.com/django/djangoproject.com/commit/b3f5d57e176dbfae7510cbdea8363eb802ccc17b), PR #610 "Added email validation to contact form." | `CharField` becomes `EmailField` for validation, but the `TextInput` widget is left as it was. **The bug starts here.** |
    | 6 May 2025 | [95ed0d5](https://github.com/django/djangoproject.com/commit/95ed0d5623b29a9bd65c0ef072c39584fb2388dd), PR #2050 "Use labels instead of placeholders on contact form" | Placeholder removed, labels added, `TextInput` kept. (The commit I found first.) |

    `TextInput` made sense in 2014, for a `CharField`. The 2016 commit changed one word, `CharField` → `EmailField`, and the explicit `TextInput` kept overriding the default `EmailInput`. Nobody chose `type="text"` for an e-mail field on purpose. Lesson: the first commit blame shows is often not the origin; keep walking back.

    I posted this history as [a comment on pull request #2924](https://github.com/django/djangoproject.com/pull/2924#issuecomment-6370103273), for the reviewers. Not on issue #107, which the 2014 commit mentions: that one is "Styling for contact templates", opened and closed on 16 November 2014.

- [ ] Look at the other forms in the same file. Are there other fields that would benefit from the same treatment? Note them, but **keep the pull request to what the issue asks**. A small, focused pull request gets reviewed faster.

## Step 4: write a failing test first

- [x] Open `contact/tests.py`. Find the `ContactFormTests` class. Read `setUp` and `test_invalid_email`: they show you the URL and how a test talks to the page.

    **Tips:** on the fix branch, `ContactFormTests` is at line 27, `setUp` at 28 (sets `self.url`, run before each test), `test_invalid_email` at 32 (submits a bad address with `self.client.post(...)`), and the new `test_name_and_email_inputs` at 47 (loads the page with `self.client.get(...)`). Compare the two: POST sends the form, GET just loads the page. For the file before the fix, see <https://github.com/django/djangoproject.com/blob/main/contact/tests.py>.

- [x] Write a new test method that loads the contact page (a GET, not a POST) and checks the rendered HTML of the two inputs.

    **Note:** this is the **test** in pull request #2924, not the fix. The pull request changes two files:

    | File | Lines | What it does |
    | --- | --- | --- |
    | `contact/forms.py` | 2 changed | **The fix**: `TextInput` → `EmailInput` for E-mail, `autocomplete` on both fields. |
    | `contact/tests.py` | 13 added | **The test**: proves the fix works and stops anyone breaking it again. |

    The test, `test_name_and_email_inputs`:

    ```python
    def test_name_and_email_inputs(self):
        form = self.client.get(self.url).context["form"]
        self.assertInHTML(
            '<input type="text" name="name" class="required" autocomplete="name" '
            'required id="id_name">',
            str(form["name"]),
        )
        self.assertInHTML(
            '<input type="email" name="email" class="required" autocomplete="email" '
            'maxlength="320" required id="id_email">',
            str(form["email"]),
        )
    ```

    "Loads the contact page (a GET)" is `self.client.get(self.url)`; "checks the rendered HTML of the two inputs" is the two `assertInHTML` calls. Before the fix it failed (the page drew `type="text"`, no `autocomplete`); after the 2-line change in `forms.py` it passes. That is why the test comes first.

- Hints, if you need them, one at a time:
    1. The existing tests use `self.client`. What does `self.client.get(self.url)` return?
    2. Django's `TestCase` has an assertion that checks a response contains a piece of text or HTML. Search the Django testing docs for "assertContains".
    3. Alternatively, you can test the form directly, without a request: instantiate the form and render one bound field to a string. Which is simpler to read? Which is closer to what a user sees?
- [ ] Run only your test: `python -m manage test contact` (inside docker: prefix with `docker compose run --rm web`). It must **fail**. If it passes before you changed anything, the test is not testing the right thing.

## Step 5: make the change

- [x] Change the form so the two fields render as the issue asks. Keep the existing `class` attribute.

    **What was done:** two lines in `contact/forms.py`, class `BaseContactForm`, on the branch `contact-email-input-autocomplete`:

    ```diff
         email = forms.EmailField(
    -        widget=forms.TextInput(attrs={"class": "required"}),
    +        widget=forms.EmailInput(attrs={"class": "required", "autocomplete": "email"}),
             label=_("E-mail"),
         )
         name = forms.CharField(
    -        widget=forms.TextInput(attrs={"class": "required"}),
    +        widget=forms.TextInput(attrs={"class": "required", "autocomplete": "name"}),
             label=_("Name"),
         )
    ```

    - **E-mail:** the widget changes from `TextInput` to `EmailInput`, so the page draws `<input type="email">` and phones show the e-mail keyboard. `"autocomplete": "email"` tells the browser it can fill in the saved address.
    - **Name:** the widget stays `TextInput` (a name is ordinary text, so `type="text"` is right). Only `"autocomplete": "name"` is added.
    - **The class is kept:** `"class": "required"` stays in both `attrs` dicts, so the page's styling does not change. The new attribute is just one more key in the same dict.
    - **One change, three forms:** the two sponsorship forms inherit these fields from `BaseContactForm`, so they are fixed too.
    - Nothing else changes: the labels, the validation (`EmailField` already checked the address) and the other fields stay as they were.

- [x] Run your test again: it must pass now. Then run the whole `contact` app's tests.

    **Done:** from the repository folder, on the fix branch:

    ```bash
    # only the new test
    docker compose run --rm web python -m manage test contact.tests.ContactFormTests.test_name_and_email_inputs
    # the whole contact app
    docker compose run --rm web python -m manage test contact
    ```

    Result of the whole `contact` app:

    ```text
    Ran 15 tests in 0.556s

    OK
    Destroying test database for alias 'default'...
    ```

    All 15 pass, the new test included. `OK` = everything passed; `FAILED (failures=…)` = a test ran but the page did not match; `FAILED (errors=…)` = a test crashed. "Destroying test database" is normal: Django builds a throwaway database for the tests and deletes it at the end.

- [x] Reload the local page, inspect the inputs, run FastPass, and (optional) listen with Orca again. **Skipped:** neither FastPass nor Orca shows this kind of change (see Step 0: FastPass only flagged colour contrast, Orca read both fields as "entry required"). The test covers the rendered inputs.
- [x] Run the project's linters: the repository uses **pre-commit** (see `.pre-commit-config.yaml`). Install it once, then run it on the files you changed.

    **Done:** installed once with `uv tool install pre-commit`, then, from the repository folder:

    ```bash
    SKIP=prettier,checkmake pre-commit run --files contact/forms.py contact/tests.py
    ```

    All checks **passed** (black, flake8, ruff check, ruff format, pyupgrade, django-upgrade, whitespace and end-of-file checks) and no file was changed. "Skipped (no files to check)" is normal: those hooks are for other file types.

    Why `SKIP`: the first plain run crashed while installing **prettier** (`npm error code EALLOWGIT`: "Fetching non-root packages of type "git" have been disabled"). pre-commit installs every tool in the config, even ones that don't apply. Prettier is for CSS and JavaScript, checkmake for the Makefile, so skipping them is fine for Python changes. A local setup problem, not a code problem.

    If a fixer hook (black, ruff format, trailing-whitespace) changes a file after the pull request is open: `git add` the files, `git commit --amend --no-edit`, `git push --force-with-lease`. Optional: `pre-commit install` runs the checks on every commit.

## Step 6: commit, push, open the pull request yourself

Done: [pull request #2924](https://github.com/django/djangoproject.com/pull/2924), opened on 23 October 2026.

!!! note "First review, 24 October 2026: change the commit message"

    The reviewer asked me to remove the AI agent from the commit's co-authors (the `Co-Authored-By:` line). Django has no rule on it yet, so it is simpler to leave it out; the AI use stays disclosed in the pull request description. To change only the message of the last commit, and push it again:

    ```bash
    git fetch origin                      # so Git knows what the branch on the fork looks like
    git commit --amend                    # edit the message, delete the Co-Authored-By line
    git push --force-with-lease origin contact-email-input-autocomplete
    ```

    `--force-with-lease` overwrites the branch only if nobody else pushed to it since your last fetch. Without the `git fetch`, it refuses with **"stale info"**: it has nothing to compare against. Check that the code did not change: `git diff <old commit> HEAD` prints nothing.

- Read the commit titles of recent human-written merged pull requests (not the dependabot ones). Imperative or past tense? Do they reference the issue number? Copy the style.
- Commit, push your branch **to your fork**, and open the pull request against `django/djangoproject.com` `main` (`gh pr create --help`, or the GitHub button).
- The pull request template has a **required AI Assistance Disclosure**: tick exactly one box. If you used an AI tool, tick the second box and say what it was used for.
- In the description: link the issue (look up the GitHub keyword that closes an issue when the pull request is merged), say what you changed, how you tested it, and the WCAG criterion.

## Step 7: check yourself

Before you open the pull request, can you answer these without looking?

1. What is the difference between a form **field** and a **widget** in Django?
2. Why did the page render `type="text"` even though the field was an `EmailField`?
3. What does the `autocomplete` attribute let a browser do, and which WCAG criterion asks for it, at which level?
4. Why write the test before the fix?
5. Why not fix every form on the site in the same pull request?

### My answers

(i) **Field and widget.** The field holds the rules: it cleans and validates the data on the server. The widget is the HTML the browser receives. An `EmailField` checks that the address is valid; its widget decides whether the page draws `<input type="email">` or `<input type="text">`. Two separate jobs, and you can change one without the other.

(ii) **Why `type="text"`.** Because the form passed `widget=forms.TextInput(...)`, and an explicit widget overrides the field's default `EmailInput`. The history explains it. In 2014 the field was a `CharField`, so `TextInput` was the right widget. In 2016 it became an `EmailField` for validation, one word changed, and the old `TextInput` stayed. Nobody chose it; it was left behind.

(iii) **`autocomplete`.** It tells the browser what the field is for (`name`, `email`), so it can fill in the saved value in one tap. For someone for whom typing is slow or painful, that removes the typing. WCAG 2.2 asks for it in success criterion 1.3.5, Identify Input Purpose, level AA.

(iv) **Test first.** A test that fails before the fix proves it tests the bug. Mine failed and printed the real input, `type="text"` with no `autocomplete`; after the two-line change it passed. If it had passed before the fix, it would have been testing the wrong thing. It also stays in the suite. In 2016 a one-word change created the bug and no test noticed; now a change like that would fail.

(v) **One issue, one pull request.** A small pull request is quicker to review and easier to revert. Issue #2904 is about two fields on one form. The change in `BaseContactForm` already fixes the two sponsorship forms, which inherit it; anything beyond that is a different issue, with its own discussion. Other fields that could get the same treatment go in a note, not in this pull request.

Which of these could you explain to the next Djangonaut without the notes?

## Where to get help

- Your Djangonaut Space team channel and weekly check-in.
- **DSF Office Hours**, every Wednesday, on the Djangonaut Space Discord: explicitly for work on djangoproject.com.
- The [Django accessibility team](https://www.djangoproject.com/foundation/teams/#accessibility-team), for accessibility questions.

## My notes

- **Orca on the live contact form**, before the fix, Firefox on Ubuntu 24.04: Name says "Name : entry required." then "invalid entry."; E-mail says "E-mail : entry required." then "invalid entry.". The two fields sound the same: nothing says the second one wants an e-mail address. "invalid entry" is only because the required fields are empty. I skipped the "after" test. Lessons: Orca speaks the system language (French, for me) unless told otherwise; Firefox works with Orca out of the box, Chrome needs `--force-renderer-accessibility`.
- **Reading:** [Working with forms](https://docs.djangoproject.com/en/6.1/topics/forms/) (Django 6.1 docs), the topic guide on HTML forms, GET and POST, building a `Form` with its view and template, bound and unbound forms, fields, widgets and `cleaned_data`, and rendering forms in templates. The part behind #2904: a **field** validates the data, a **widget** is its HTML, and passing another widget overrides the field's default.
