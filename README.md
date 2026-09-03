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
