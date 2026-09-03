# LangMARL &amp; MASkills — Project Website

Source for the website of **LangMARL** (EMNLP 2026 Main Conference) and **MASkills**
(EMNLP 2026 Findings), two works on language-space optimization for self-evolving
multi-agent LLM systems from the [DaRL Lab](https://labs.engineering.asu.edu/hw/) at
Arizona State University.

Live site: https://darl-genai.github.io/LangMARL_homepage/

## Pages

| File | Content |
| --- | --- |
| `index.html` | Overview landing page tying both projects together |
| `langmarl.html` | LangMARL project page |
| `maskills.html` | MASkills project page |

## Structure

```
static/css/    Bulma + FontAwesome + Academicons base, plus site.css for this site
static/js/     Bulma carousel/slider helpers
static/images/langmarl/   Figures exported from the LangMARL paper
static/images/maskills/   Figures exported from the MASkills paper
```

Figures are PNGs rendered from the papers' PDF sources at 160 dpi:

```bash
pdftocairo -png -r 160 -singlefile figures/<name>.pdf static/images/<project>/<name>
```

## Pipeline animations

`static/images/<project>/pipeline_stages.*` is a four-stage reveal of each method's
loop (3s per stage, 10s on the finished diagram), in the style of Google's staged
architecture animations. The frames are drawn in HTML/SVG, not exported from the paper:

```
tools/langmarl_stages.html   source for the LangMARL animation
tools/maskills_stages.html   source for the MASkills animation
tools/build_stage_gifs.py    screenshots ?stage=1..4 and assembles the GIFs
```

Each source page renders all four stage columns and reads `?stage=N` to decide how many
are visible, so you can open it in a browser to edit a single stage. To regenerate after
an edit:

```bash
python3 tools/build_stage_gifs.py
```

Two files come out of each build, and the pages load them through a `<picture>`:

| | Resolution | Colours | Size | Role |
| --- | --- | --- | --- | --- |
| `.webp` | 3200×1800 | 24-bit | ~315 KB | what browsers actually load |
| `.gif` | 1600×900 | 256, dithered | ~540 KB | fallback, and the portable copy for slides |

The frames are captured with `--force-device-scale-factor=2`, so the WebP carries over 3×
the pixels of its 960 px display slot and stays sharp on retina screens. GIF's 256-colour
ceiling is why it is the fallback rather than the primary — at full resolution it would be
much larger without looking better.

## Column widths

Every content column on every page is one width: `.container.is-max-desktop` with a single
`.column.is-full-width` inside, giving a 984 px content box (960 px for figures) at desktop
sizes. Two things break that, and both are guarded in `static/css/site.css`:

- **Wide children stretch their column.** Bulma columns are flex items and default to
  `min-width: auto`, so a table or image wider than the column silently widens it — and that
  whole section then sits wider than the rest of the page. `.columns > .column { min-width: 0 }`
  pins the column to its flex basis and lets the wide child scroll inside `.table-wrap`.
- **Figures that break out of the column** drag the column with them, for the same reason.
  Keep figures at the standard width; do not reintroduce a full-bleed figure class.

If a results table is too wide for 960 px, group its headers with `colspan` (see the
coordination-topology table in `maskills.html`) rather than widening the column.

## Before publishing

Both papers' arXiv buttons are commented out in the hero of `langmarl.html` and
`maskills.html`. Uncomment and fill in the arXiv IDs once the preprints are posted.
The `BibTeX` sections carry the EMNLP 2026 venues but no page numbers or ACL Anthology
IDs yet — swap in the official Anthology entries when the proceedings are published.

## Related work

- [LangMARL code](https://github.com/DaRL-GenAI/LangMARL) · [tutorial](https://langmarl-tutorial.readthedocs.io/)
- [MASkills code](https://github.com/DaRL-GenAI/MASkills)
- [Instructional Agents](https://darl-genai.github.io/instructional_agents_homepage/)

## Website License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>. The template is adapted from [Nerfies](https://github.com/nerfies/nerfies.github.io).
