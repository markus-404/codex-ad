# ChatGPT / ChatGPT Work acceptance checks

Use this after the workspace admin imports or syncs the GitHub marketplace.
Record the installed plugin version/commit, Chat or Work, local or cloud where
shown, exposed tools, actual outputs, and any blocker. These checks are not
claims that a live workspace run has already passed.

## Installation and resources

- Confirm the imported plugin exposes ad-brainstorm, ad-maker, and ad-maker2.
- Start a new chat with the plugin enabled. Explicitly select/name each skill.
- Verify each skill can read its shipped supporting files; specifically check
  ad-maker2 can discover/read the bundled ad-maker references without assuming
  a local sibling directory.
- Verify ad-maker2 is used when explicitly requested and does not replace the
  normal ad-brainstorm → ad-maker handoff.

## ad-brainstorm in Work

Use a real single-product URL and original product images you may use. Confirm
the agent fetches actual product facts, views the images, and identifies any
user-supplied material as such. It should execute the analysis validator before
the grid, the concept validator before rendering, and return downloadable JSON,
rendered Markdown, analysis, scraped inputs, and audience map. Inspect the actual
validator results; a conversational statement that validation passed is not evidence.

Repeat with browsing unavailable but supplied product material and images tied
to that URL. Repeat with Python unavailable: it must stop at the analysis gate,
not manufacture scores or proceed with 100 supposedly validated concepts.

## ad-maker native image generation

Attach a product image and logo, supply a complete brief and exact copy, and
request one static image with the native image tool. Confirm actual generation,
correct image-reference binding, no API-key request, no extra images, and visual
QA. The generated image should be visible/downloadable in the conversation.
Record any exact ratio/model/size controls the tool could not honor.

Ask for a prompt only: no image should be generated. Ask for a production
gallery: the compiler/scorer must actually run and every prompt must meet 75
before generation. If the scripts/dependencies are inaccessible, expect a
specific blocker and unvalidated draft records, not guessed readiness scores.

## ad-maker2 format application

Use the same kind of finished static concept. Confirm no unnecessary brainstorm,
unchanged copy/claims/audience/angle, pinned classification and execution guides,
real example viewing, native generation, and a source/QA receipt. Library example
images must not be sent as the product/logo references.

Then provide a researched brief without creative direction: expect optional
format-guided ideation, not a mandatory 100-concept grid. Make a required guide or
example inaccessible: expect a verified compatible alternative or an explicit
blocker, never ungrounded generation labeled as format-compliant.

## Limits and follow-up

Request an unsupported exact generator setting or pixel-exact compositing
without a compositor. The skill should explain the mismatch before proceeding,
not claim that a generative edit preserves exact pixels. Follow up with a
targeted text edit and check the actual selected image and unchanged elements.

Record observed passes/failures and links/screenshots from the test session.
Repo unit tests and simulated skill reviews supplement these checks; they do not
replace a logged-in installed-plugin run in the team's actual workspace.
