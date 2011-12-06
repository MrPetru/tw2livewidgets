<tr class="item-${w.item_id}">
    % for c in w.children:
        <td class=${c.css_class}>
            ${c.display() | n}
        </td>
    % endfor
</tr>
