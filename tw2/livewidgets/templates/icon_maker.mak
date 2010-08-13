function(data) {
    var icon_class = "${w.icon_class}";
    var title = $.sprintf('${w.label | n}', data);
    var css_class = $.sprintf('${w.css_class or '' | n}', data);
    var field = '<div class="' + css_class + ' ' + icon_class +'" title="' + title + '"></div>';
    return field;
}

