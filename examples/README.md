# Examples

Generic examples live in the repository and on the website, not inside every user project.

The sample source files in `examples/sample-sources/` can be copied into a test project:

```bash
markdown-mentor new-project demo
cp examples/sample-sources/* demo/1-source-files/
cd demo
make-markdown-library new 1-source-files -o 2-markdown-library/markdown-library.md
markdown-mentor guide .
```

The website should show reusable examples of teaching approach files, teaching materials packs, style files, draft Markdown materials, and exported outputs.
