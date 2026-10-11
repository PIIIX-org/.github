<div align="center">

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/system.svg" width="100%" alt="The PIIIX system: an orange star with four planets on tilted orbits. git-a-profile is closest, then Elara with its moon Yildizim, then inter.face and website-pitch-pipeline. Vectory is a comet parked at the far end of a long dashed orbit, tail pointing away from the star."/>

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/almanac.svg" width="100%" alt="PIIIX almanac: license MIT; contributing by fork, pull request and CLA; 6 bodies; 1 star."/>

</div>

PIIIX is one star and the things that orbit it. The name reads as Planet III
of star X. Every body on the map above is a real repository; size is its
commit count, and distance from the star is distance from shipped. The
closer a body sits, the more finished it is. Vectory sits at the far end of
its orbit because it is on hold.

Everything here is built in the open, with AI built into how each product
works. Tools in categories most people treat as solved (notes, design
direction, READMEs, outreach), each one aimed at the part the incumbents
left broken.

The map, the rows under each product and the light curve are drawn from the
GitHub API by [`profile/forge.py`](https://github.com/PIIIX-org/.github/blob/main/profile/forge.py).
Last observed 2026-10-11.

## The bodies

### Elara

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/ephemeris/elara.svg" width="100%" alt="Elara ephemeris: status in testing, 684 commits, 281 merged pull requests, first light 2026-07-09, last commit 2026-10-11, source public."/>

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/chapters/main/assets/hero.svg" width="100%" alt="Elara's own banner: the Knowledge Engine Observatory flight deck."/>
</div>

A self-hostable second brain. Notes are plain markdown files on disk, in the
Open Knowledge Format with ISO 8601 timestamps, so nothing is locked in a
database. Elara connects to your git repositories, parses the code into a
Tree-sitter symbol index, and lets a note link straight to a live
declaration with `[[repo:#symbol]]`. When the code changes, the links
follow. AI agents get the same access a human gets, through an MCP server
with full tool parity: the agent reads the same graph, edits the same notes,
under the same permissions. Real-time collaboration runs on Yjs, so agent
edits stream into an open note like a teammate typing.

**Why.** Most knowledge tools bolt a chat window onto the notes after the
fact. We wanted the AI inside the data layer, navigating the actual graph
instead of guessing from a prompt. That decided the stack: one TypeScript
runtime, Fastify, Postgres with pgvector, local embeddings through
Transformers.js so note content never leaves the instance.

**Where it is.** In testing. The repo is still named `chapters`; Elara is
the product name. Bugs found in testing are filed as
[issues](https://github.com/PIIIX-org/chapters/issues).

→ [github.com/PIIIX-org/chapters](https://github.com/PIIIX-org/chapters)

<details>
<summary><b>Its moon: Yildizim</b> (closed source, prototype, paused since July)</summary>
<br>

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/ephemeris/yildizim.svg" width="100%" alt="Yildizim ephemeris: status prototype, paused; 80 commits; 37 merged pull requests; first light 2026-07-17; last commit 2026-07-19; source private."/>

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/yildizim/first-light.png" width="280" alt="Yildizim: a sky of galaxies, each one a knowledge base."/> <img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/yildizim/tier2-vault-stars.png" width="280" alt="Yildizim: inside a galaxy, vaults resolved as stars."/> <img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/yildizim/tier3-note-system.png" width="280" alt="Yildizim: inside a vault, notes as planets orbiting their star."/>
</div>

A 3D galaxy view for Elara: every knowledge base a galaxy, every vault a
star, every note a planet. Meant for the hosted version of Elara, as the
thing that makes returning to your own notes feel like exploring. Eighty
commits and 37 merged pull requests in three days of July, then paused
while Elara itself went into testing. The renderer held 60 frames per
second at 371,355 synthetic notes in a headed Chromium test; that figure
is from a generated dataset, not from a real knowledge base.

</details>

<br>

### inter.face

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/ephemeris/inter-face.svg" width="100%" alt="inter.face ephemeris: status in testing, 71 commits, 2 merged pull requests, first light 2026-07-28, last commit 2026-08-17, source public."/>

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/inter.face/main/gallery/piiix-marketing-kintsugi-wall.png" width="720" alt="An inter.face run for the PIIIX marketing site: a kintsugi wall concept board."/>
</div>

Art direction for any interface, as a pipeline a coding agent can run. In:
an inbox of references and a six-row translation table. Out: a
`DIRECTION.md` with named values instead of adjectives, a `tokens.json`
in the Design Tokens Community Group format, one comp per surface, and
runnable HTML prototypes that measure their own contrast and spacing. It
stops before code, so the build agent makes no aesthetic decisions of its
own.

**Why.** Agents build interfaces fast and design them badly, because
nobody wrote the direction down in a form they can follow. inter.face is
that form.

**Where it is.** In testing, across seven coding agents. The direction for
Taha's portfolio was its first field run.

→ [github.com/PIIIX-org/inter.face](https://github.com/PIIIX-org/inter.face)

<br>

### git-a-profile

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/ephemeris/git-a-profile.svg" width="100%" alt="git-a-profile ephemeris: status done, 14 commits, 1 merged pull request, first light 2026-07-24, last commit 2026-07-24, source public."/>

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/git-a-profile/main/assets/banner.svg" width="100%" alt="git-a-profile banner: forge a one-of-a-kind GitHub profile, org, or project README."/>
</div>

Point a coding agent at the repo, give it a GitHub handle, and it
researches the subject, proposes concepts, builds every asset as committed
SVG, writes the prose, and screenshots the live result. Three human gates
on the way; no templates, no badge services. The page you are reading was
made with it, as were six other documented profiles.

**Where it is.** Done. It gets used rather than developed.

→ [github.com/PIIIX-org/git-a-profile](https://github.com/PIIIX-org/git-a-profile)

<br>

### website-pitch-pipeline

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/ephemeris/website-pitch-pipeline.svg" width="100%" alt="website-pitch-pipeline ephemeris: status process being reworked, 19 commits, 0 merged pull requests, first light 2026-07-23, last commit 2026-09-16, source public."/>

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/website-pitch-pipeline/main/assets/hero-banner.svg" width="100%" alt="website-pitch-pipeline banner: a cyanotype blueprint of a storefront homepage on a planning table, stamped CHECKED: HUMAN."/>
</div>

Agents case a market, find businesses with weak websites, draw one bespoke
demo site per business, build it, and draft the outreach. A human signs
every gate before anything scales, and geography is a campaign variable:
the same pipeline works in Istanbul, Berlin or a US HVAC corridor.

**Where it is.** The process is being reworked. The first version proved
the research and demo steps; the outreach step is being redesigned before
it runs again.

→ [github.com/PIIIX-org/website-pitch-pipeline](https://github.com/PIIIX-org/website-pitch-pipeline)

<br>

### Vectory

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/ephemeris/vectory.svg" width="100%" alt="Vectory ephemeris: status on hold until funded, 5 commits, 0 merged pull requests, first light 2026-07-07, last commit 2026-07-20, source public."/>

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/assets/vectory/01.png" width="220" alt="Vectory architecture diagram: system overview."/> <img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/assets/vectory/05.png" width="220" alt="Vectory architecture diagram: code-generation pipeline."/> <img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/assets/vectory/12.png" width="220" alt="Vectory architecture diagram: interconnection map."/>
</div>

A design canvas that writes real HTML and CSS as you draw, with the code
visible and editable the whole time. Twelve architecture diagrams and a
competitive research pass exist; no application code does.

**Where it is.** On hold until PIIIX has the funding to build it. Until
then, [ArtCraft](https://getartcraft.com/) and
[Storytold](https://github.com/storytold) cover similar ground.

→ [github.com/PIIIX-org/vectory](https://github.com/PIIIX-org/vectory)

## Light curve

Commits per week, per body, since the first commit in July. Paused work
goes flat instead of being described as alive.

<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/lightcurve.svg" width="100%" alt="Light curve of commits per week. Elara is active from July through October. git-a-profile, Yildizim, inter.face and Vectory each have one burst in July or August and are flat afterwards. website-pitch-pipeline has a July burst and one commit in September."/>

## How we're organized

Every role maps to real GitHub access, not a title:

| Role | Access | What they do |
|---|---|---|
| Manager | Maintain | Repo settings, branch protection, merges |
| Developer | Write | Pushes code, opens and merges pull requests |
| Reviewer | Triage | Reviews pull requests, triages issues |
| Designer | Write | Pushes UI and asset pull requests |
| Docs/Content | Write | Pushes docs and README changes |
| Community/Support | Triage | Labels and triages issues, helps other contributors |

Roles are earned. A contributor forks a repo, opens a pull request, signs
the CLA in a comment on that PR, and the role follows from the work. The
bar for each one is in
[CONTRIBUTING.md](https://github.com/PIIIX-org/.github/blob/main/CONTRIBUTING.md).
A pull request does not merge without a passing CLA check.

<div align="center">
<img src="https://raw.githubusercontent.com/PIIIX-org/.github/main/profile/assets/footer.svg" width="100%" alt="The PIIIX star low on a dark horizon."/>
</div>

<!-- forged-with: git-a-profile -->
<sub>Forged with <a href="https://github.com/PIIIX-org/git-a-profile">git-a-profile</a> · <a href="https://github.com/PIIIX-org">PIIIX</a></sub>
