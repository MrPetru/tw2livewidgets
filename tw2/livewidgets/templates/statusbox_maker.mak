<%inherit file="item_layout_maker.mak"/>
content += '<div class="item-' + data["id"] + '">';
    $.each(field_makers, function() {
        if (this.condition(data)) {
            var css_class = this.css_class;
            var field_maker = this.maker;
            content += '<div>' + field_maker(data) + '</div>';
        }
    });
content += '</div>'
