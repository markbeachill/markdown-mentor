/* Style builder helper for Markdown style files.
   The public style file is Markdown, usually style/style.md. */
(function () {
  function buildMarkdownStyle() {
    return [
      '# Style',
      '',
      '## General style',
      '',
      '- body_font: Calibri',
      '- body_size_pt: 11',
      '- heading_font: Calibri',
      '- heading_color: 1F3864',
      '',
      '## Word document style',
      '',
      '- h1_size_pt: 20',
      '- h2_size_pt: 16',
      '- h3_size_pt: 13',
      '',
      '## HTML style',
      '',
      '- html_title: Teaching material',
      ''
    ].join('\n');
  }
  window.markdownMentorDefaultStyle = buildMarkdownStyle;
})();
