# Generation across ChatGPT, ChatGPT Work, and local hosts

Select tools by what the session actually exposes. A product name or installation does not guarantee browsing, vision, Python, file delivery, or an image generator. Explicit user instructions take precedence over this routing guidance.

## Inputs and shared resources

Accept researched briefs and brand/product assets as chat attachments, readable connected files, or real local files. View image assets before using them. Keep a role-to-source mapping: logo, product, reference ad, mask. For native tools, bind the actual attachment/resource/image handle using that tool's supported input schema. A filename or “uploaded #0” in prose does not attach an image.

Keep ordered reference indices aligned with the images actually passed. Use logo #0 only when a logo exists; number remaining assets in actual order. If there is no logo and none is required, say “no logo” in the prompt rather than inventing one or labeling a product as the logo. Keep approved copy exact. Missing essential assets require clarification, not invented file paths.

Supporting documents/scripts may be exposed as files or host-managed resources. Resolve their real locations/identifiers through the installed skill metadata and resource reader. When ad-maker2 needs these resources, discover the bundled ad-maker skill and read its resources as documentation without invoking its creative workflow. Do not assume a sibling filesystem directory exists in cloud sessions. If a required resource is not exposed, report it; do not replace its contents from memory.

## Select the generation route

| Request and available capability | Action |
| --- | --- |
| Prompt/brief only | Return the requested six-slot prompt records; do not generate images. |
| Image request with a native image tool | Use that tool after applicable gates; no API key request. |
| Explicit API execution, dry-run payload, or configured local API workflow without a native tool | Use the existing `scripts/generate_image.py` with its documented options and real input files. |
| Image request with no supported generator | Explain the missing capability and return a clearly labeled prompt draft if useful; do not claim an image was generated. |

Do not ask teammates to paste API keys into chat or place them in generated artifacts. The API route uses credentials already configured in the execution environment; native generation uses the host's existing access. Do not silently switch to a separately billed API route when the native tool fails or hits a limit.

For native generation:

1. Author the six-slot prompt and negative prompt. Append the negative constraints to the actual tool prompt so they reach the generator; do not leave them only in the deliverable metadata.
2. Bind the approved image references with their roles/order. Do not send examples from an external format library as product/logo assets. For editing, include the target image and mask when supported. Read the exposed tool schema instead of assuming API parameter names.
3. Preserve requested count, composition, ratio, and exact text. Use only controls the native tool exposes. Do not report the API helper's default model, pixel size, seed, or quality as the native setting without evidence. If an exact required control cannot be honored, explain and resolve that mismatch before generating. For flexible settings, record the actual result and any limitation. Multi-image requests can be fulfilled in supported batches without exceeding the requested count; do not add rerolls.
4. Return the actual generated image objects or supported download links. Inspect outputs for product fidelity, copy accuracy, readability, and placement. Distinguish passed, failed, and uninspected checks. A successful tool call is not visual QA. If the tool ends the response after image delivery, perform QA on the next supported inspection step rather than claiming it already happened.

For the API route, reference assets are sent by the existing helper's `--mode edit`; default `generate` does not attach `image_refs`. Choose a reference-capable route when fidelity depends on them. A dry-run only validates the request payload and never proves rendered quality.

## Python helpers without a terminal

Use a Python/code-execution tool when available; a shell is not required. First materialize the actual packaged helper and required resources in a writable session directory, preserving their layout. Do not reconstruct scripts from memory. Compiler and scorer need `PyYAML` and `references/platform-presets.yaml` next to the staged `scripts/` directory; compositing needs Pillow. Keep supplied image files readable at the resolved paths. If those dependencies cannot be provided, report the blocker.

For example, with an existing `script_path` and `arguments` list, call a packaged CLI helper in a Python tool without spawning a shell:

```python
import runpy
import sys

previous_argv = sys.argv
try:
    sys.argv = [str(script_path), *arguments]
    exit_code = runpy.run_path(str(script_path))["main"]()
finally:
    sys.argv = previous_argv
assert exit_code == 0, "Helper failed; inspect its reported errors before continuing"
```

Use the real CLI argument names from that helper. Input/output paths are absolute or session-directory-relative; image paths within brand/product YAML remain relative to the YAML file. Ordinary native image requests can use an authored prompt without compiled JSON. Production/gallery/SKU requests still require compilation and deterministic scoring at the existing threshold of 75; if execution is unavailable, stop before generation at that gate. Do not substitute a model-estimated numeric score. Follow the same rule for requested deterministic validation.

Before scoring any compiled record, reconcile every image index/role in its prompt and negative constraints against its actual `image_refs`. The current compiler assumes a logo at #0 even when no logo was supplied. In that case, replace the nonexistent-logo instructions with “Do not add a logo” and correct product references to their actual indices; preserve approved copy and other constraints. Save the corrected record and score that final JSON, not the pre-correction payload. If a required template constraint cannot be represented faithfully, stop and explain it instead of sending a mismatched asset map to generation.

Exact PNG compositing remains a distinct operation: use the real supplied product pixels with `composite_product.py` or an available equivalent compositor. A generative edit is not proof of exact pixel preservation. Explain when exact compositing is unavailable.

## Deliverables

Keep outputs in the working project on local hosts, or a writable session/artifact area on cloud hosts. For ChatGPT/Work, expose actual download links or file attachments for prompts, images, and QA receipts; do not present a bare sandbox path as a usable link. If file delivery is unavailable, return prompt content directly and state that no downloadable file was created. Preserve the user's filenames/organization where specified.
