# Contributing

Welcome, grab a cup of coffee, and let's roll our sleeves up! By participating in this project, you agree to abide by our [code of conduct](CODE_OF_CONDUCT.md).

## What should I work on?

As of March 19, help is especially wanted in these areas:

- **Python wizards** for application development ([#chime-app](https://codeforphilly.org/chat?channel=chime-app))
  - Hardening the code
  - Making it more flexible
  - Unit tests!
- **DevOps heroes** for application hosting ([#chime-ops](https://codeforphilly.org/chat?channel=chime-ops))
  - Maintaining Penn's instance
  - Ensuring easy redeploys
- **Math and stats friends** for model improvements ([#chime-analysis](https://codeforphilly.org/chat?channel=chime-analysis))
- **Consulting DevOps champs** to help other public agencies set up their own instances ([#chime-help](https://codeforphilly.org/chat?channel=chime-help)

## Before You Begin

- Join the [#covid19-chime-penn](https://codeforphilly.org/chat?channel=covid19-chime-penn) channel, and [request write access](https://codeforphilly.slack.com/archives/CV4NGQYMP/p1584665484368300) to the `CodeforPhilly/chime` Github repository.
- Our highest-priority work is organized in the [Github Project Management board](https://github.com/CodeForPhilly/chime/projects/2). Look for an issue matching your interests & skills in one of the "Ready" columns.
- Assign yourself to the issue and add a comment to briefly describe your plan.
- For new ideas, please first discuss the change(s) you wish to make via [issue](https://github.com/codeforphilly/chime/issues) or appropriate Slack channel (platform/app - #chime-app, devops - #chime-ops, modeling - #chime-analysis). 

## Making and Submitting Changes

- [Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the [CodeforPhilly/chime](https://github.com/CodeForPhilly/chime) repo.
- Base your work on the `develop` branch.
- Submit pull requests from your fork, also against the `develop` branch of the `CodeforPhilly/chime` repo.
- Check your pull request periodically to see if any changes have been requested or any merge conflicts have arisen.
- If a merge conflict arises, rebase against the latest `develop` branch and force-push the new branch as early as you can. You may need to do this more than once before your changes get merged. Do your best to keep your branch in a mergeable state until it is finished being reviewed and accepted.
- Note: Frequent contributors with write access can submit pull requests from a new branch in the `CodeforPhilly/chime` repository.

## Review & Release

<!-- Currently establishing & clarifying the release process, this is just a skeleton. -->

- Maintainers will review pull requests, asking for changes as needed.
- Once a PR has 1 approval and passes automated tests, maintainers will merge to release branches.
  - Exception: Documentation or infrastructure support PRs can be merged directly to master.
- Deploys to production must be signed off on by @beckerfluffle or @cchivers.

## Requesting Functionality

**Stakeholders/Users**: Check the [#covid19-chime-penn](https://codeforphilly.org/chat/covid19-chime-penn) channel on [Slack](https://codeforphilly.org/chat) to see if your need is already being addressed.
