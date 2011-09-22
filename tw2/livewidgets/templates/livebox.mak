<div class="${w.widget_class}" id="${w.id}">
    % for c in w.children:
        ${c.display() | n}
    % endfor
</div>
