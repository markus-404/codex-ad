# Pinned Visual Formats knowledge

Source: [alyshadotmd/visual-formats](https://github.com/alyshadotmd/visual-formats).
Commit: `498444b7fdc4da674f07d8b0432c32a24b5062c9`.

This is a practitioner format library, not evidence of a formal industry standard or proven campaign performance. Use its execution guidance, not its example brands, offers, proof, or claims.

## Retrieve only the relevant knowledge

Use the host's browsing/file-fetch tools or shell HTTP access. Every upstream request must use the pinned commit, never `main`, a latest-branch redirect, or a search-engine summary. A local cache is acceptable only when its provenance identifies this exact repository, commit, and file path. Store retrieved materials in the working project's output/cache area, not in the installed plugin.

1. Fetch and read the [format index](https://raw.githubusercontent.com/alyshadotmd/visual-formats/498444b7fdc4da674f07d8b0432c32a24b5062c9/formats/index.md). Use it to shortlist formats fitting the supplied message, assets, and still-image placement. For brainstorming, shortlist before ideating; for a finished concept, match its existing message without inventing a new angle.
2. For each selected token, fetch and read both files under this base:

   `https://raw.githubusercontent.com/alyshadotmd/visual-formats/498444b7fdc4da674f07d8b0432c32a24b5062c9/formats/<token>/`

   - `classify.md`: verify the defining visual characteristics and still-image eligibility.
   - `execute.md`: extract the applicable anatomy, writing/layout constraints, and QA checklist.

   Require substantive guides, not empty stubs. Reject video-only formats; mixed formats are eligible only where the guides support a still treatment. If combining a device and structure (such as notes-app + listicle), read and apply both guides. Do not flatten a video format into a still and claim compliance.
3. Fetch the [example index](https://raw.githubusercontent.com/alyshadotmd/visual-formats/498444b7fdc4da674f07d8b0432c32a24b5062c9/files/_index.md). Find media tagged `vf=<token>`, including filenames with multiple format tags. Resolve media at repository-root `files/`, URL-encoding the filename. Download and visually inspect actual relevant still examples with the host's image viewer; filenames and text descriptions are not visual inspection. Follow guide-specific example instructions; at least one inspected still example per selected format is required (a dual-tag example can cover both).
4. Extract a short set of applicable requirements and tie them to the proposed Visual/Layout and supplied copy. Check guide requirements against fixed copy, brand rules, product references, and the shared prompt/compiler constraints before committing to the format.

## Inconsistencies and unavailable sources

The pinned library has known inconsistencies: `product-grid` appears both as a full index row and in the pending list, some indexed listicle media return 404, and some guides use incorrect relative example paths. Successful reads of both substantive guides establish documentation status; the stale pending label alone does not exclude a documented format.

If an indexed image is missing, inspect the [tree at this commit](https://api.github.com/repos/alyshadotmd/visual-formats/git/trees/498444b7fdc4da674f07d8b0432c32a24b5062c9?recursive=1) for actual token-matched paths under `files/`. If the tree is truncated, traverse the `files` subtree rather than treating the partial result as exhaustive. Try a valid same-format still example and visually inspect it. Do not switch commits to repair a missing file.

Some guides link to external copywriting resources outside this repository. Do not invent their contents or silently fetch an unpinned replacement. If the missing resource is necessary for the requested execution, report the gap and choose another compatible documented format or ask for the missing material. Existing fixed copy can be used only when the fetched guide provides sufficient visual-execution guidance on its own; disclose any external dependency not consulted.

If guides, media, or image-viewing capability remain unavailable, stop the affected concept's generation and identify the missing source/capability. Do not produce an unrestricted fallback under the ad-maker2 label. When rules conflict with fixed brief inputs, choose a compatible documented format; if none fits, ask which constraint the user wants to revise.

Example ads are calibration references. Do not put their imagery into generator reference slots or copy their brands, quotes, numbers, or visual assets. Generator references remain the user's approved product, logo, and reference assets in baseline order.
