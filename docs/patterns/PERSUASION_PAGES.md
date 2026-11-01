# Persuasion pages - the fleet pattern

A persuasion page is the one public page whose job is to make a stranger care. Every other
page in the app assumes the visitor already cares and has a task. That split decides almost
everything about webapp structure: one page may scroll and show off, all the rest must stay
dense and get out of the way.

Words used here, spelled out once. A persuasion page is sometimes called a landing page or
a marketing page; this pattern keeps the word persuasion because landing says nothing about
the job. Tool pages are the working pages behind it: consoles, dashboards, pickers, settings,
logs. The leporello is the long folding print, and by extension any page that keeps unfolding
as you scroll. The fat footer is the multi-column link block at the very bottom of a
persuasion page. Bring Your Own Key means the visitor pastes their own cloud key.

## When a persuasion page is required

An app earns a persuasion page when a stranger can install it and get value in the first
week. Speech, search, image and video tools, e-book and media libraries, the robot stack,
the drawing-to-simulation chain, the office chain: all of these qualify. Inner plumbing
never gets one. Federation hubs, observability, secrets stores, monitoring, backup engines
get a good README file and a clean dashboard, and that is the whole public surface.

The test is simple. If you can finish the sentence "install this and by Friday you will...",
the app needs a persuasion page. If the sentence ends with "...be able to see what the other
apps are doing", it does not.

## The section order

Every fleet persuasion page follows the same order, so learning one teaches all. The
sections below are listed in order, and each one earns its place by answering the next
question a skeptical visitor asks.

First comes the hero. It answers "what is this and is it for me" in under ten seconds:
one eyebrow line with the honest facts (free, local, no account), one headline with a
single promise, one paragraph naming the apps it plugs into, and at most three buttons
(open the working page, get the installer, see the code). Getsandratools adds an orbit
stage beside the headline on wide screens: one central anchor with five small group marks
circling it slowly. That is decoration, and it must behave like decoration: pause on hover
or keyboard focus, still for visitors who prefer reduced motion, hidden on narrow screens.
A hero may have one such flourish, never two.

Second comes the proof strip. Four numbers, no adjectives: tool count, stable count,
installer count, extension count, or the per-app equivalents (voices, providers, models,
recipes). Numbers are checkable, adjectives are not. If a number would embarrass you,
fix the thing it counts instead of hiding the strip.

Third comes the choice. The five group cards on the hub, or the equivalent short list on
a single app (for example: transcribe, clone a voice, talk live). Each card carries a
count and links to the working page that does the thing. This is also where the sidebar
order is mirrored, so the persuasion page and the app navigation can never disagree about
what exists.

Fourth comes how it works, in exactly three steps. Pick, install, ask is the hub version;
every app finds its own three verbs. Three steps fit in memory. Four do not.

Fifth comes the ready proof. Up to six real items with installers or extensions and their
sizes and dates, not screenshots of buttons that do nothing. This section is why the fake
rule exists: a persuasion page that shows dead buttons poisons every page behind it.

Sixth comes the open-source panel. License name, link to the code, and the sentence that
makes the business model honest: the tools are free, cloud use is optional, keys are yours.
If there is a paid convenience layer later, it is named here in one line, never as a
pop-up.

Seventh and last comes the fat footer. Columns of small links in the same order as the
rest of the page (groups or features, then community, then get, then legal), plus a bottom
bar with copyright, imprint, privacy note, and status. The footer is also the sitemap for
search engines, so every working page worth finding is linked from it exactly once.

## What stays out

No login wall before the proof. No pricing table before the open-source panel. No pop-up
of any kind. No autoplaying video with sound. No second flourish in the hero competing
with the first. No marketing links inside the app navigation; resources and support belong
in the footer or a help page, never as sidebar items that look like tools. And no dead
controls anywhere on the page: a button that does nothing on the persuasion page teaches
the visitor that the tool pages lie too.

## The two levels

The hub persuades for the fleet, each major app persuades for itself. The hub headline
promises breadth (many tools, runs on your machine, no account). The app headline promises
one outcome (speak and it moves, search that shows its receipts, drawings that become
simulations). Both use the same grammar, the same section order, the same footer shape,
so the visitor feels one fleet, not fifty websites.

Plumbing apps opt out of both levels and appear on the hub only as rows in the picker and
the downloads tables, which is honest: they are found through need, not through browsing.

## Motion, access, and small screens

Motion is allowed one flourish per persuasion page, one timing token for the whole page,
and a still version for everyone who asks for reduced motion. Hovering or focusing the
flourish pauses it. Decorative motion is hidden from screen readers whenever the same
links exist elsewhere on the page, which they always do, because the cards repeat them.

At 800 pixels wide the page stacks to one column with no sideways scrolling. Tables scroll
inside their cards. The orbit or equivalent hides. The fat footer stacks its columns.
These are checked by hand on every persuasion page before it ships, because the overflow
bugs always cluster exactly here.

## Shipping checklist for a new persuasion page

Read this as a walkthrough, not a form. Open the page with an empty address and confirm
the hero answers the what-and-for-me question in ten seconds. Count the buttons and
confirm there are at most three. Read the proof strip and spot-check one number against
its source. Click every card and confirm it lands on a working page. Count the how-it-works
steps and confirm there are three. Click every proof button and confirm each one does what
it says. Read the open-source panel and confirm the license link opens. Scroll to the fat
footer and confirm every working page is linked exactly once. Shrink to 800 pixels and
confirm nothing scrolls sideways. Turn on reduced motion and confirm the flourish stops.
Do all of that, and the page may ship.
