---
applyTo: "**/*"
---

# Git / GitHub development rules ( anything )

## Priority order ( always )
1. Repository-defined rules and docs are highest priority ( CONTRIBUTING.md, CODEOWNERS, SECURITY.md, workflow docs, branch protection, rulesets, CI requirements ).
2. Issue / PR templates are mandatory when they exist.
3. When making any decision that depends on external behavior ( GitHub features, language specs, library APIs, security guidance ), do web research and rely on official sources first.

## Required workflow ( end-to-end )
1. Check repository state
   - Update local default branch ( e.g. main ) to the latest.
   - Read repository contribution rules ( CONTRIBUTING.md etc. ) before writing issues, branches, commits, or PR text.
   - Check existing issues / PRs / discussions to avoid duplicates.
   - Check whether issue / PR templates exist and what they require. :contentReference[oaicite:1]{index=1}
2. Create or confirm an issue
   - If an issue already exists, use it.
   - Otherwise create an issue that states:
     - Goal ( expected behavior )
     - Acceptance criteria
     - For bugs: repro steps, expected vs actual, environment ( OS, versions, commit hash )
   - If an issue template / issue form exists, fill it as required and do not remove template structure.
3. Create a branch from the default branch tip
   - Follow repository branch rules if present.
   - If no repo rule exists, use:
     - `feat/<issue-number>-<short-kebab>`
     - `fix/<issue-number>-<short-kebab>`
     - `chore/<issue-number>-<short-kebab>`
4. Implement the change
   - Keep scope to one goal per PR.
   - Do not mix unrelated formatting, renames, or dependency bumps.
5. Commit changes
   - Follow repository commit rules if present.
   - If no repo rule exists, use Conventional Commits:
     - `feat: ...` / `fix: ...` / `docs: ...` / `refactor: ...` / `test: ...` / `ci: ...` / `chore: ...` :contentReference[oaicite:2]{index=2}
6. Open a PR
   - Use Draft PR if early feedback is needed.
   - If a PR template exists, keep its structure and fill it properly. :contentReference[oaicite:3]{index=3}
   - Link the issue in the PR description.
     - If auto-close is intended, use closing keywords ( e.g. `Fixes #123` ) in the PR description. :contentReference[oaicite:4]{index=4}
7. Wait for CI and review the results
   - If CI fails: identify the root cause, push fixes, re-run CI.
   - If CI passes: proceed to merge steps.
8. Merge
   - Do not merge if required checks are failing or required reviews are missing.
   - Follow the repository’s merge method ( merge commit / squash / rebase ) policy.
9. Cleanup
   - Ensure the issue is closed ( if appropriate ).
   - Delete the branch after merge. :contentReference[oaicite:5]{index=5}

## Templates ( mandatory when present )
- Issue templates live on the default branch ( `.github/ISSUE_TEMPLATE/` for issue templates and issue forms ). :contentReference[oaicite:6]{index=6}
- PR templates can exist ( location varies by repository ).
- Template handling rules:
  - If the template explicitly instructs how to handle non-applicable sections, follow that instruction.
  - If the template does not specify, leave non-applicable fields blank ( do not add placeholders like `N/A` ).
  - Do not check checklist items unless they are actually completed.

## Web research ( mandatory )
- For any information you judge necessary to make a correct decision, perform web research.
- Source priority:
  1. Official documentation ( specs, release notes, RFCs )
  2. Official repositories ( README, CHANGELOG, issues, PRs )
  3. High-quality secondary sources
- When external facts influence a decision or change, include the relevant URLs in the issue or PR description, and note the version / date constraints when applicable.
- For GitHub mechanics ( templates, linking issues, workflow expectations ), use GitHub Docs as the primary source. :contentReference[oaicite:7]{index=7}
