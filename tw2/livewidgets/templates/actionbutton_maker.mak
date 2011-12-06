
<%namespace name="utils" file="utils.mak"/>
function(data) {
    var display_array = data.actions_display_status;
    var cond33 = display_array[${w.index | n}];
    var action = $.sprintf('${w.action | n}', data);
    var title = $.sprintf('${w.help_text | n}', data);
    var css_class = $.sprintf('${w.css_class | n}', data);
    var field = '<a class="${w.widget_class} ${w.dialog and 'dialog' or 'action'} ' + css_class + '" title="' + title + '" href="' + action + '">';
    ${utils.render_subfields(w.children) | n}
    field += '</a>';
    if (cond33 == 1){
        return field;
    }
    else {
        return field;
    };
}

