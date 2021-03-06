# -*- coding: utf-8 -*-
#
# This file is part of tw2.livewidgets.
#
# tw2.livewidgets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tw2.livewidgets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tw2.livewidgets.  If not, see <http://www.gnu.org/licenses/>.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""A collection of ToscaWidget2 that can update in realtime"""

import tw2.core as twc

def _maker(self, cls, displays_on=None, **kw):
    """Render a javascript function with prototype: ``function(data) {}``
    that returns the HTML for this field
    """
    if not self:
        return cls.req(**kw).maker(displays_on)
    else:
        if not self.parent:
            self.prepare()
        mw = twc.core.request_local().get('middleware')
        if displays_on is None:
            if self.parent is None:
                displays_on = mw and mw.config.default_engine or 'string'
            else:
                displays_on = twc.template.get_engine_name(
                                                self.parent.template, mw)
        v = {'w':self}
        if mw and mw.config.params_as_vars:
            for p in self._params:
                if hasattr(self, p):
                    v[p] = getattr(self, p)
        eng = mw and mw.engines or twc.template.global_engines
        return eng.render(self.maker_template, displays_on, v)


# Widgets
class LiveWidget(twc.Widget):
    """Base class for LiveWidgets"""
    maker_template = twc.Param('A mako template rendering a javascript function'
        ' with prototype: ``function(data){}`` that returns the HTML for this '
        'field', default='mako:tw2.livewidgets.templates.default_maker')
    label = twc.Param('Widget label', default='')
    help_text = twc.Param('Tooltip text', default='')
    update_condition = twc.Param('Javascript condition used to filter updates',
        default='true')
    css_class = twc.Param('Custom CSS class', default='')
    show_header = twc.Param('Show widget id in headers', default=True)
    widgets_class = twc.Variable('Base CSS class for the widget', default='')
    data = twc.Variable('A dictionary used to expand formatting strings in '
        'templates', default = {})

    maker = twc.util.class_or_instance(_maker)


class LiveCompoundWidget(LiveWidget, twc.CompoundWidget):
    """Base class for compound LiveWidgets

    If the ``key`` of the compound widget corresponds to an element
    in its parent ``data``, the widget will exted ``data`` with the subelements
    prefixing their names with its ``key``
    """
    children = []

    @classmethod
    def post_define(cls):
        # a compound widget must have id=None to propagate the object or
        # dictionary received from its ItemLayout parent as "value" to its
        # children, so if "id" is set we copy it to "key" (if "key" is not
        # already set) and then reset it
        id = getattr(cls, 'id', None)
        cls.key = cls.key or id or ''
        if id:
            cls.id = None

    def prepare(self):
        # extend data with subelements
        newdata = {}
        if self.key in self.data:
            if isinstance(self.data[self.key], dict):
                for k, v in self.data[self.key].iteritems():
                    newdata['%s_%s' % (self.key, k)] = v
            elif hasattr(self.data[self.key], '__dict__'):
                for k, v in self.data[self.key].__dict__.iteritems():
                    newdata['%s_%s' % (self.key, k)] = v
        self.data.update(newdata)

        # prepare data for children
        for c in self.children:
            c.data = self.data

        # we call super().prepare() after updating children data so if one of
        # our children is a LiveCompoundWidget, it can propagate it to its
        # own children
        super(LiveCompoundWidget, self).prepare()


class Box(LiveCompoundWidget):
    """A simple container widget

    Box is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:tw2.livewidgets.templates.box'
    maker_template = 'mako:tw2.livewidgets.templates.box_maker'

    widget_class = 'lw_box'

class Link(LiveCompoundWidget):
    """A link widget

    Link is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:tw2.livewidgets.templates.link'
    maker_template = 'mako:tw2.livewidgets.templates.link_maker'
    dest = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default='')

    widget_class = 'lw_link'

class Button(LiveCompoundWidget):
    """An button widget

    Button is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:tw2.livewidgets.templates.button'
    maker_template = 'mako:tw2.livewidgets.templates.button_maker'
    action = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default='')
    dialog = twc.Param('Whether the button target should open in a dialog '
        '(the button will have a "dialog" css class, creating the dialog is '
        'left to the application)', default=False)

    widget_class = 'lw_button'


class Text(LiveWidget):
    """A simple text widget"""
    template = 'mako:tw2.livewidgets.templates.text'
    maker_template = 'mako:tw2.livewidgets.templates.text_maker'
    text = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary, ``None`` defaults to the '
        'widget\'s value', default=None)

    widget_class = 'lw_text'

    def prepare(self):
        super(Text, self).prepare()

        # use widget value if "text" was not given
        self.text = self.text or str(self.value) or ''


class Image(LiveWidget):
    """An image widget"""
    template = 'mako:tw2.livewidgets.templates.image'
    maker_template = 'mako:tw2.livewidgets.templates.image_maker'
    src = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary, ``None`` defaults to the '
        'widget\'s value', default=None)

    widget_class = 'lw_image'

    def prepare(self):
        super(Image, self).prepare()

        # use widget value if "src" was not given
        self.src = self.src or self.value or ''


class Icon(LiveWidget):
    """An icon widget"""
    template = 'mako:tw2.livewidgets.templates.icon'
    maker_template = 'mako:tw2.livewidgets.templates.icon_maker'
    icon_class = twc.Param('The css class identifying this icon', default='')

    widget_class = 'lw_icon'


# Layouts
class ItemLayout(twc.CompoundWidget):
    """Base class for LiveWidget layouts"""
    maker_template = twc.Param('A mako template rendering a javascript function'
        ' with prototype: ``function(data){}`` that returns the HTML for this '
        'layout', default='mako:tw2.livewidgets.templates.default_maker')
    append_selector = twc.Param('A jQuery selector that will be used to '
        'determine where to append new items', default='')

    def prepare(self):
        # set item_id
        self.item_id = getattr(self.value, 'id', '')

        # extract a dictionary from value
        if isinstance(self.value, dict):
            self.data = self.value
        elif hasattr(self.value, '__json__'):
            self.data = self.value.__json__()
        else:
            self.data = getattr(self.value, '__dict__', {})

        # extend data with parent's extra_data
        if self.parent and hasattr(self.parent, 'extra_data'):
            self.data.update(self.parent.extra_data)

        # prepare data for children
        for c in self.children:
            c.data = self.data

        # we call super().prepare() after updating children data so if one of
        # our children is a LiveCompoundWidget, it can propagate it to its
        # own children
        super(ItemLayout, self).prepare()

    maker = twc.util.class_or_instance(_maker)


class ListItemLayout(ItemLayout):
    """A compound widget that wraps its children in a <li> element"""
    template = 'mako:tw2.livewidgets.templates.list_item_layout'
    maker_template = 'mako:tw2.livewidgets.templates.list_item_layout_maker'
    append_selector = 'ul'


class RowLayout(ItemLayout):
    """A compound widget that wraps its children in a <tr> element"""
    template = 'mako:tw2.livewidgets.templates.row_layout'
    maker_template = 'mako:tw2.livewidgets.templates.row_layout_maker'
    append_selector = 'table tbody'


# Containers
class LiveContainer(twc.RepeatingWidget):
    """Base class for LiveWdigets containers"""
    container_class = twc.Param('CSS class for the container element',
        default='')
    extra_data = twc.Param('Additional data that will be appended to each '
        'items\'s data', default={})
    update_topic = twc.Param('The topic this container is listening to for '
        'updates', default=None)
    update_filter = twc.Param('A class used to filter updates', default=None)
    callbacks = twc.Param('A javascript object providing custom callbacks for '
        'update events', default='{}')
    children = twc.Required

    resources = [
        twc.JSLink(modname=__name__, filename='static/livewidgets.js'),
#        twc.JSLink(modname=__name__, filename='static/jquery.js'),
    ]


class LiveList(LiveContainer):
    """A repeating widget that render its values as an <ul> element"""
    template = 'mako:tw2.livewidgets.templates.livelist'
    child = ListItemLayout

    container_class = 'lw_livelist'


class LiveTable(LiveContainer):
    """A repeating widget that render its values as an <table> element"""
    show_headers = twc.Param('Show table headers', default=True)

    template = 'mako:tw2.livewidgets.templates.livetable'
    child = RowLayout

    container_class = 'lw_livetable'


# DEBUG stuff
class Dummy(object):
    def __init__(self, **kw):
        for k, v in kw.iteritems():
            setattr(self, k, v)

