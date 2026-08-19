## Erfan Habibi Panah Fard

Full-stack developer and CS graduate student in Buffalo, NY, working on secure multi-party computation with Prof. Marina Blanton. Most of what I build falls into four piles: compilers and cryptography in C/C++, developer tooling in Python, bioinformatics, and web in TypeScript. I like problems where the bug is in the *design* rather than the code — the kind that never throws an error.

<a href="https://www.erfanhabibipanah.dev" target="_blank">
<img src="https://img.shields.io/badge/website-%2324292e.svg?&style=for-the-badge&logo=firefox&logoColor=white" alt="website" style="margin-bottom: 5px;" />
</a>
<a href="https://twitter.com/e_habibipanah" target="_blank">
<img src="https://img.shields.io/badge/twitter-%2300acee.svg?&style=for-the-badge&logo=twitter&logoColor=white" alt="twitter" style="margin-bottom: 5px;" />
</a>
<a href="https://linkedin.com/in/erfanhabibipanah" target="_blank">
<img src="https://img.shields.io/badge/linkedin-%231E77B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="linkedin" style="margin-bottom: 5px;" />
</a>

---

### 🔖 Commonbook — Claude Code forgets a project when you rename its folder

[![stars](https://img.shields.io/github/stars/erfanhabibipanah/commonbook?style=flat-square&logo=github)](https://github.com/erfanhabibipanah/commonbook)
[![CI](https://github.com/erfanhabibipanah/commonbook/actions/workflows/ci.yml/badge.svg)](https://github.com/erfanhabibipanah/commonbook/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/erfanhabibipanah/commonbook?style=flat-square)](https://github.com/erfanhabibipanah/commonbook/blob/main/LICENSE)

I reorganised a workspace with a plain `mv` and the next session started from nothing. Not degraded — blank.

Claude Code stores each project's memory in a directory named after the project's **filesystem path**. Change the path and a fresh empty store appears; the old notes stay on disk, addressed by a path that no longer exists, and the retention sweep never collects them. Nothing errors. The model simply no longer knows the project, and you don't know what it forgot.

**[Commonbook](https://github.com/erfanhabibipanah/commonbook)** rekeys that memory to the repo's git remote, so it survives moves, renames and re-clones — and recovers what path-keying already lost. Python standard library only, no dependencies, MIT.

→ **[Read the writeup](https://erfanhabibipanah.github.io/commonbook/)** · **[Check your own machine](https://github.com/erfanhabibipanah/commonbook#check-your-machine-first)** (one command, reads only)

---

### What else I'm building

**[PICCO](https://github.com/applied-crypto-lab/picco)** &nbsp;`C` `C++`

A source-to-source compiler that turns annotated C into secure multi-party computation protocols — the reference implementation from the 2013 paper, still being sharpened. My work is on the code generator: a batch multi-operation optimisation that groups operations across loop iterations instead of emitting them one at a time, plus truncation and right-shift corrections on both the Shamir and replicated-secret-sharing backends. ~157 commits on `master`; the batch work is on `batch-multi-op-dev`.

---

**[skim-db-secure](https://github.com/erfanhabibipanah/skim-db-secure)** &nbsp;`C++`

Database components for [SKiM](https://gitlab.com/SCoRe-Group/SKiM), a memory-efficient metagenomic classifier for Oxford Nanopore reads. Short k-mers with compression and statistical correction, so classification stays fast without holding the whole index in RAM.

---

### Tools I actually reach for

<div align="center">
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/cplusplus-original.svg" alt="C++" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/c-original.svg" alt="C" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/typescript-original.svg" alt="TypeScript" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/javascript-original.svg" alt="JavaScript" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/react-original-wordmark.svg" alt="React" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/nodejs-original-wordmark.svg" alt="Node.js" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/git-scm-icon.svg" alt="Git" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/graphql.png" alt="GraphQL" height="28" />
<img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/figma-icon.svg" alt="Figma" height="28" />
</div>

<sub>The React clones dated 2021 are from when I was learning the framework. Left up on purpose — they're where this started.</sub>
