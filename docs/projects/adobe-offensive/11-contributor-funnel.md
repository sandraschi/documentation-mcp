# 11 - Contributor Funnel: Why PhotoCraft Is Catnip for High-Ability Devs

Date: 2026-10-10. Status: working theory with receipts, written the night
v0.6.0 shipped with ~60 external PRs from ~25 contributors. Companion to 07
(strategy) and 10 (InterPositive). This file is about the labor engine, not
the product: how a hated incumbent plus legible gaps plus merge velocity
manufactures a volunteer swarm, and what the fleet should steal from it.

## The observation, in full sentences

PhotoCraft is catnip for high-ability developers because it offers a worthy
cause with gaps shaped exactly like their specialist knowledge, where each
gap converts into a good pull request within an evening. A color scientist
sees absolute-colorimetric mishandling of zero media white and recognizes a
twenty-line fix only they would know. A kernel person sees motion blur running
seventy times slower than it should and smells merged kernels. A PSD veteran
sees spec-order masks misread and reaches for the public spec they have
already memorized. The issue tracker functions as a menu of scoped,
prestigious micro-problems, each one sized for a weekend and legible to
exactly the right expert. Most open-source projects offer newcomers a typo in
the docs. PhotoCraft offers the chance to reimplement a Photoshop filter
kernel correctly, in front of thirty-four thousand witnesses.

## The four-stage funnel, in full sentences

First, a worthy enemy recruits where code cannot. Nobody sacrifices weekends
for a Jira ticket, but killing the cancellation fee brings volunteers. Adobe
is the perfect villain because it is universally used, universally resented,
and beatable-looking. Opencode followed the identical arc against the agent
priesthood and now counts hundreds of collaborators who showed up for the
cause with code attached. The lesson is that the cause is the top of the
funnel, and the code is what falls out the bottom.

Second, legible gaps convert specialists. The critical property is not that
gaps exist but that each gap is shaped like one person's rare knowledge.
Motion blur performance wants a GPU kernel specialist. PSD mask ordering
wants someone who has read the public spec. Colorimetric edge cases want a
color scientist. Feather and density parity wants whoever remembers how the
curves actually behave. i18n label collisions want a bilingual designer. Every
entry in the v0.6.0 changelog maps to exactly one expert profile, which means
every expert who wanders past the tracker finds the drawer with their name on
it. Shallow targets cannot do this because their gaps are all generic
frontend work. Deep targets do it naturally because buried math creates
specialist-shaped holes, which is the optimistic inversion of the math-moat
argument: depth that deters competitors attracts contributors.

Third, merge velocity is respect. Eight releases in eight days means a volunteer's
pull request ships this week, not next quarter. Nothing kills contributor energy
faster than a three-month review queue. The v0.6.0 changelog even contains
infrastructure for contributors rather than users: CI runs 1.6 times faster
with no more out-of-disk failures. That is a maintainer spending his scarcest
resource, attention, on the people who work for free. Fast merge is a love
language for volunteers, and every project that scales contribution has learned
it: opencode merges fast, Blender reviews addons fast, the Linux kernel says
no fast (which is the same virtue, honestly priced).

Fourth, reputation surface pays in the currency specialists value. Every merged
pull request is witnessed by tens of thousands of stargazers and by a hiring
market that now associates a name with having reimplemented a piece of
Photoshop correctly. For a color scientist or kernel hacker, that line on the
record is worth more than a conference talk, because it is attached to
shipped, reviewed, benchmarked work instead of slides. The star count is not
vanity. It is the payroll.

## Why the insults prove the funnel works

The pushback calling the founder insane or manic, and the suspected
astroturf, cluster around the person rather than the pull requests, because
the pull requests are unattackable. Nobody writes a hit piece about merged
kernels running seventy times faster. Ad hominem arrives exactly when the work
product cannot be criticized, and its function is to raise the founder's
personal cost of continuing. The correct response, which the project is
executing, is to keep merging: every release with sixty external PRs makes
the single-dev narrative (manic or genius, both wrong) obsolete by replacing
it with a contributor graph no insult can touch.

## The uncomfortable mirror for the fleet

The fleet holds roughly two hundred repositories with the opposite funnel:
breadth without a villain, issues without an audience, merges without
witnesses. Nobody's weekend goes to fixing lint in repo number one hundred
and forty-seven, because there is no cause, no specialist-shaped gap, and no
crowd to ship in front of. This is not a quality problem. Several fleet repos
are genuinely good software. It is a funnel problem, and funnels are design
choices, not accidents.

Three correctives exist, in ascending order of ambition. First, contribute
outward: fleet PSD, color, and imaging knowledge would land pull requests in
photocraft tomorrow, and every merged PR is a bridge carrying reputation and
relationships back to the fleet. Second, curate inward: pick one fleet repo,
frame one enemy (a hated rental, a missing capability, a paper only we read),
publish ten specialist-sized gaps with differential tests attached, and merge
within days. Do not start with twenty repos. Start with one cause. Third,
differential-test everything: the fleet's pywinauto reversal engine plus the
photocraft pixel-diffing method generalizes to every shallow and deep target
in file 04. A gap with a failing test attached is a contribution waiting for
its specialist. A gap described in prose is a wish.

## What to watch

- Contributor count per release in photocraft and siblings. The theory predicts
  growth superlinear with stars until merge bandwidth saturates, then a
  maintainer bottleneck forces either lieutenants or slowdown. Watch which.
- Whether lieutenants emerge (repeat reviewers with merge rights). That is the
  moment a project becomes an institution instead of a person.
- Whether the funnel replicates to siblings (filmcraft, vectorcraft) or stays
  photocraft-local. Replication would confirm the mechanism over the moment.
- Whether any fleet repo successfully imports the pattern, with numbers, not
  intentions. One repo, ten gaps, merge latency under seven days, contributor
  count before and after.
- Whether astroturf escalates from founder-focused to contributor-focused
  (license FUD aimed at scaring corporate contributors is the classic next
  move; the MIT/Apache dual license is the prebuilt defense, watch it get
  tested).

## Connection to the section thesis

Files 01 through 10 argue that tools get cloned while pipelines endure, that
headcount was the workaround rather than the input, and that open tooling
compounds past centralized wins. This file adds the labor mechanism underneath
all of it: open tooling compounds because a worthy cause plus legible gaps
plus fast merges manufactures the swarm that does the compounding. The
billion-user outcome was never going to be built by one dev plus one model.
It gets built by one dev plus one model plus ten thousand evenings from
people who each knew exactly one thing. Design for those evenings.

## Postscript: the funnel manufactures fame, and it is borderless

Verified 2026-10-10 via the GitHub API: Ar-maan05, author of the v0.6.0
motion-blur optimization (six to seventy times faster via merged kernels),
is Armaan Sandhu, a student at Worcester Polytechnic Institute, account from
2020, sixty-one repos, three followers. Not a famous dev. An unknown kid with
systems and graphics obsessions who spent an evening on a problem shaped
exactly like his brain, and is now attached to a 70x speedup witnessed by
tens of thousands. The funnel does not harvest famous developers. It
manufactures them, one scoped kernel at a time.

And it is lovely how totally international that manufacture is. A student in
an Indian tier-three university town contributes on identical terms to a guy
in Los Angeles: same tracker, same review bar, same merge velocity, same
witnessed record. No visa, no relocation, no pedigree filter, no timezone
penalty that a fast merge queue cannot absorb. English plus code is the
lingua franca, the test suite is the credential check, and the only thing
that matters is whether the kernel is correct. Every prior software era gated
participation on geography or affiliation. This one gates on knowing exactly
one thing and showing up with it.
