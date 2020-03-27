# Contributing

Welcome, grab a cup of coffee, and let's roll our sleeves up! By participating in this project, you agree to abide by our [code of conduct](CODE_OF_CONDUCT.md).

## What should I work on?

Our project work is organized by 4 main areas:

| Area        | What type of help wanted? | Project Board                                         | Slack channel           | Maintainers |
| --- | --- | --- | --- | --- |
| App Platform        | Python wizards to work on application development, hardening the code, making it more flexible, and unit testing | [Board](https://github.com/CodeForPhilly/chime/projects/3) | [#chime-app](https://codeforphilly.org/chat?channel=chime-app) | @quinndougherty                      |
| Analysis            | Epidemiologists and other math and stats friends, for model improvements | [Board](https://github.com/CodeForPhilly/chime/projects/5) | [#chime-analysis](https://codeforphilly.org/chat?channel=chime-analysis) | @sam-qordoba, @cjbayesian                   |
| DevOps              | DevOps heroes (especially if you have Kubernetes experience) for hosting, maintenance, and ensuring easy redeploys. | [Board](https://github.com/CodeForPhilly/chime/projects/2) | [#chime-ops](https://codeforphilly.org/chat?channel=chime-ops) | @moosequest, @themightychris, @lottspot |
| General Project Ops | Writing, documentation, and project and product management | [Board](https://github.com/CodeForPhilly/chime/projects/6) |  | @mariekers                           |

As of March 21, help is especially wanted from contributors with experience in Kubernetes and Python.

## Before You Begin

- Join the [#covid19-chime-penn](https://codeforphilly.org/chat?channel=covid19-chime-penn) channel for project-wide announcements.
- Our highest-priority work is organized in [Github Project Boards](https://github.com/CodeForPhilly/chime/projects). Look for an issue matching your interests & skills in the "Ready" columns.
- Comment on the issue to let us know you're picking it up, briefly describe your plan, and go forth!
- For new ideas, please first discuss the change(s) you wish to make via [issue](https://github.com/codeforphilly/chime/issues) or the appropriate Slack channel (see table above).

## Making and Submitting Changes

- [Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the [CodeforPhilly/chime](https://github.com/CodeForPhilly/chime) repo.
- Base your work on the `develop` branch.
- Submit pull requests from your fork, also against the `develop` branch of the `CodeforPhilly/chime` repo.
- Request review from the relevant maintainer(s).
- Check your pull request periodically to see if any changes have been requested or any merge conflicts have arisen.
- If a merge conflict arises, rebase against the latest `develop` branch and force-push the new branch as early as you can. You may need to do this more than once before your changes get merged. Do your best to keep your branch in a mergeable state until it is finished being reviewed and accepted.
- If your change affects the results calculated or presented, update `change_date` in `src/penn_chime/parameters.py` when the pull request is ready for merge, so users can see when results have last changed
- Note: Frequent contributors with write access can submit pull requests from a new branch in the `CodeforPhilly/chime` repository.

## Review & Release

<!-- Currently establishing & clarifying the release process, this is just a skeleton. -->

- Maintainers will review pull requests, asking for changes as needed.
- Once a PR has 1 approval and passes automated tests, maintainers will merge to release branches.
  - Exception: Documentation or infrastructure support PRs can be merged directly to master.
- Deploys to production must be signed off by @beckerfluffle or @cchivers.

## Requesting Functionality

**Stakeholders/Users**: Check the [#chime-users](https://codeforphilly.org/chat/chime-users) channel on [Slack](https://codeforphilly.org/chat) to see if your need is already being addressed.
