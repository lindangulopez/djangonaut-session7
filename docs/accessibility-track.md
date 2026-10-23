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

**Pull request opened, 23 October 2026: [#2924](https://github.com/django/djangoproject.com/pull/2924).** Next: answer the review comments. Every step, with my answers: [Guide: issue #2904, step by step](reading-list/guide-2904.md).

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

### Tutorial: listen to pull request #2924 with Orca, on Ubuntu with Firefox

[Pull request #2924](https://github.com/django/djangoproject.com/pull/2924) changes two fields on the [contact form](https://www.djangoproject.com/contact/foundation/): E-mail becomes an e-mail input, and both fields get `autocomplete`. This tutorial listens to the form twice, before and after the change, with the Orca screen reader. It takes about 15 minutes.

You need nothing new. Orca and Firefox both come with Ubuntu 24.04. Don't download Firefox from firefox.com: a second copy would sit next to Ubuntu's and would not update itself. Use Firefox and not Chrome: Chrome only talks to Orca if you start it in a special way, and even then not as well.

#### The keys

A shortcut written **A+B** means: hold down A, press B, let go of both.

| Written | Which key |
| --- | --- |
| **Super** | The key with the Windows logo, bottom left, between Ctrl and Alt. |
| **Alt** | Next to the space bar, on the left. |
| **Tab** | On the left, above Caps Lock, often with two arrows. |
| **Shift+Tab** | Hold Shift, press Tab: go back one step. |
| **Ctrl** | Bottom left corner. On its own, it makes Orca stop talking. |
| **Orca key** | **Insert** on a full keyboard, **Caps Lock** on a laptop layout. |

So **Super+Alt+S** means: hold the Windows key and Alt together, press S, let go. It turns Orca on, and the same keys turn it off.

If the shortcut does nothing, use the menu: **Settings → Accessibility → Seeing → Screen Reader**, on or off.

#### Step 1: make Orca speak English (once)

Orca speaks the language of the computer. Mine is in French, and the contact form is in English, so I switched Orca's voice to English.

(i) Turn Orca on (**Super+Alt+S**).

(ii) Press **Orca key+Space**. The Orca Preferences window opens.

(iii) Go to the **Voice** tab and choose an **English** voice or language.

(iv) Click **Apply**, then **OK**. Orca keeps this setting. The rest of the computer stays in French.

#### Step 2: listen to the form before the change

The live site does not have the fix yet: the pull request was still open on 23 October 2026.

(i) With Orca on, open Firefox and go to <https://www.djangoproject.com/contact/foundation/>. Orca starts reading the page. Press **Ctrl** to make it stop.

(ii) Click once on some plain text above the form. Now your key presses go to the page, not to the address bar.

(iii) Press **Tab** once, and listen. Each press moves to the next link, button or field, and Orca says what it is. The menu links come first, so keep pressing **Tab**, one press at a time.

(iv) When you hear **"Name"**, stop. Write down exactly what Orca says, for example *"Name, entry, required"*.

(v) Press **Tab** once more, to E-mail. Write that down too.

(vi) Type a few letters in each field. Does Firefox offer to fill it in? Does Orca read the suggestion?

To hear a field again, press **Orca key+Enter**. If you went too far, **Shift+Tab** goes back one field.

#### Step 3: listen to the form after the change

The change is on my branch, `contact-email-input-autocomplete`, in my copy of the site.

(i) In a terminal, start the site:

```bash
cd ~/Github/djangoproject.com
git switch contact-email-input-autocomplete
docker compose up
```

(ii) In Firefox, go to <http://www.djangoproject.localhost:8000/contact/foundation/>.

(iii) Do Step 2 again, from (ii) to (vi), and write down what Orca says now.

(iv) When you are done, press **Ctrl+C** in the terminal to stop the site.

#### Step 4: turn Orca off

Press **Super+Alt+S**, or **Settings → Accessibility → Seeing → Screen Reader**, off.

#### What to expect

Before the change, Name and E-mail probably sound the same. After it, E-mail may sound a little different, or not at all. `autocomplete` is usually not read aloud: it helps autofill, not speech. So hearing no difference does not mean the fix does nothing. That is why I also check the inputs in the browser's developer tools (**F12**), and the keyboard on my phone.

#### If something goes wrong

| Problem | What to do |
| --- | --- |
| Orca talks too much | Press **Ctrl**. |
| Orca is silent | Check the sound is not muted, and the right output is chosen in **Settings → Sound**. |
| Orca speaks French | Do Step 1. |
| Typing does not go into a field | Click in the field with the mouse. |
| Arrow keys move a reading cursor, not the text cursor | Press **Orca key+A**. |
| The local page does not open | Check that `docker compose up` is still running in the terminal. |

#### What I heard

| Field | Before (live site, 23 October 2026) | After (my branch) |
| --- | --- | --- |
| Name | "Name : entry required." then "invalid entry." | Not done |
| E-mail | "E-mail : entry required." then "invalid entry." | Not done |

Before the change, the two fields sound the same: a label, "entry", "required". Nothing tells me the second one wants an e-mail address. Orca also says "invalid entry" for both, only because they are still empty and required. That is not what the pull request changes.

To get these words as text, not from memory, I started Orca from a terminal with a log file, and kept only the lines with `SPEECH OUTPUT`:

```bash
LANG=en_US.UTF-8 LANGUAGE=en_US:en orca --replace --debug-file ~/orca-before.txt
grep "SPEECH OUTPUT" ~/orca-before.txt
```

To stop Orca, press **Ctrl+C** in that terminal window, not in Firefox.

(iii) The [Accessibility Insights](https://accessibilityinsights.io/downloads/) browser plugin, to check a page before and after a patch. Installed on 15 October 2026, as a Microsoft Edge extension. I learned it from [Introduction to Accessibility Insights for Web](https://www.youtube.com/watch?v=XVvBJoEe4Is), the tool's own video.

Which of these would you give to someone who has finished the tutorial and nothing more?
