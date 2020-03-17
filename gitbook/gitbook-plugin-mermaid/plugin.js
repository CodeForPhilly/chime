require([
  'gitbook',
  'jquery'
], function (gitbook, $) {
  var renderId = 1;

  gitbook.events.bind('start', function () {
    // configure mermaid
    mermaid.initialize({
      startOnLoad: false,
      theme: 'forest'
    });
  });

  gitbook.events.bind('page.change', function (page) {
    $('.lang-mermaid').each(function() {
      var svgCode = mermaid.render('mermaid-render-'+renderId++, this.innerText);
      $(this).closest('pre').replaceWith('<div style="overflow-x:auto">'+svgCode+'</div>');
    })
  });
});
