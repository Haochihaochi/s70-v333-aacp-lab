# Publishing to `haochihaochi`

The preferred artifact is the Git bundle because it preserves the commit, tag and Open Headunit submodule pointer.

## GitHub CLI route

```bash
git clone /path/to/s70-v333-aacp-lab.bundle s70-v333-aacp-lab
cd s70-v333-aacp-lab
git submodule update --init --recursive
gh auth login
VISIBILITY=private ./scripts/publish-to-github.sh
```

The script creates:

```text
haochihaochi/s70-v333-aacp-lab
```

It publishes `main`, the `v0.1.0-foundation` tag, repository description and topics. Change `VISIBILITY=public` only after deciding that all future research evidence will be safely sanitized.

## Manual Git route

Create an empty repository named `s70-v333-aacp-lab` under `haochihaochi`, then run:

```bash
git remote rename origin bundle-source  # only when cloned from the bundle
git remote add origin git@github.com:haochihaochi/s70-v333-aacp-lab.git
git push -u origin main --follow-tags
```

## Source ZIP

The source ZIP is intended for review and extraction. It does not preserve the Git submodule object in the same way as the bundle. Use the bundle when publishing the repository.
