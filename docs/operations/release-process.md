# Operations: Release Process

1. Open a pull request to merge `develop` into `releases/v1`
   - **Title**: `Release: CHIME v1.#.#`
   - **Description**: Generate with this command:

        ```bash
        git fetch origin
        git log \
            --first-parent \
            --reverse \
            --pretty=format:"- %s" \
            "origin/releases/v1..origin/develop"
        ```

4. Get release pull request approved by [`@cjbayesian`](https://github.com/cjbayesian) or [`@mdbecker`](https://github.com/mdbecker)
5. Merge the pull request
6. [Create a new release against `releases/v1`](https://github.com/CodeForPhilly/chime/releases/new?target=releases/v1)
   - **Tag version:** `v1.#.#`
   - **Release Title:** `CHIME v1.#.#`
   - **Description:** Copy release notes from pull request