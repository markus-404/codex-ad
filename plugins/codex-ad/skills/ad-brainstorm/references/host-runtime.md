# Host runtime for ad-brainstorm

Use the same research, vision, 10×10 grid, and hard validation gates in ChatGPT,
ChatGPT Work, and local hosts. Detect tools from the session instead of treating
a host name as proof of browsing, Python, vision, or file access.

## Check capabilities at the point they are needed

- Read packaged references with the exposed skill-resource reader or actual
  installed files. Use the identifiers/paths returned by that host. A resource
  URI is not a filesystem path.
- Fetch the product with available browsing tools. Python networking is a
  separate capability. If fetching fails, use user-supplied product material
  tied to the original URL and identify that provenance.
- View original product images through supported remote-image access, chat
  attachments, or local image viewing. Text extraction cannot replace vision.
- Execute the shipped validators and renderer through a Python tool or shell.
  They use the Python standard library; network access and API keys are not
  needed to run them. Python still needs the actual script and input files.
- Create outputs in a writable session/artifact directory or the local project,
  and deliver them with the host's real file/download mechanism.

If a required capability is missing, explain exactly what is unavailable and
stop the affected step. Ask for accessible source material where that resolves
the blocker, or suggest a Work session with Python/files when appropriate.
Do not promise switching modes will grant tools disabled by workspace policy.
A draft label does not permit bypassing validation and continuing the grid.

## Python-tool execution without a terminal

When scripts are packaged resources instead of filesystem files, retrieve the
actual source and stage it unchanged under a writable skill directory. Do not
rewrite a validator or renderer from memory. Set `skill_dir` to that actual
directory and `output_dir` to the current product's output directory. These are
Python variables for resolved paths, not assumed fixed ChatGPT mount points.

Run the analysis gate immediately after writing `analysis.json`:

```python
import runpy

validate_analysis = runpy.run_path(str(skill_dir / "scripts/validate_analysis.py"))["validate"]
analysis_result = validate_analysis(str(output_dir / "analysis.json"), 75)
print(analysis_result)
assert analysis_result["passed"], "Fix reported analysis errors before generating concepts"
```

Only after the analysis gate passes, create the audience map and concept grid
according to the main workflow. Then run the concept gate:

```python
validate_concepts = runpy.run_path(str(skill_dir / "scripts/validate_concepts.py"))["validate"]
concept_result = validate_concepts(
    str(output_dir / "concepts.json"), str(output_dir / "analysis.json"), 75
)
print(concept_result)
assert concept_result["passed"], "Fix reported concept errors before rendering"
```

Both validators take **file-path strings**, not JSON objects. Do not lower the
threshold, infer a score yourself, or continue after an exception.

After both gates pass, render the final Markdown from the validated JSON:

```python
import json

render = runpy.run_path(str(skill_dir / "scripts/render_concepts.py"))["render"]
data = json.loads((output_dir / "concepts.json").read_text())
(output_dir / "concepts.md").write_text(render(data))
```

Return the actual output files with host-supported download links and the
validation results. The Markdown must come from the renderer, not a separately
authored summary that can drift from the JSON. The main workflow's brief
top-five summary accompanies those files.
