<%inherit file="livecontainer.mak"/>
##<div>
    % for item in w.children:
        ${item.display() | n}
    % endfor
##</div>
