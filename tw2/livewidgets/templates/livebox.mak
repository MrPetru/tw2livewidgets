<%inherit file="livecontainer.mak"/>

##<div class="statusbox">
% for item in w.children:
    ${item.display() | n}
% endfor
##</div>
