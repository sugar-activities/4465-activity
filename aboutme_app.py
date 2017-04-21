#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Daniel Francis
#
#   aboutme_app.py by:
#   Daniel Francis <sdanielf.francis@gmail.com>
#   Ceibal Jam - Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gconf
import gtk
from sugar.activity import activity
from sugar.graphics import style
from sugar.graphics.icon import Icon
from sugar.graphics.xocolor import XoColor
from sugar.graphics.xocolor import _parse_string
from sugar.graphics.toolbutton import ToolButton

names = gtk.icon_theme_get_default().list_icons()
if "gtk-ok" in names:
	icon = "gtk-ok"
else:
	icon = "dialog-ok"

class AboutMeActivity(activity.Activity):
	def colour_changed_callback(self, widget, type):
		colour = widget.get_current_color()
		red = "%x" % int(colour.red / 65535.0 * 255)
		if len(red) == 1:
			red = "0%s" % red
		green = "%x" % int(colour.green / 65535.0 * 255)
		if len(green) == 1:
			green = "0%s" % green
		blue = "%x" % int(colour.blue / 65535.0 * 255)
		if len(blue) == 1:
			blue = "0%s" % blue
		new_colour = "#%s%s%s" % (red, green, blue)
		if type == "out":
			in_colour = self.in_colour_selector.get_current_color()
			red = "%x" % int(in_colour.red / 65535.0 * 255)
			if len(red) == 1:
				red = "0%s" % red
			green = "%x" % int(in_colour.green / 65535.0 * 255)
			if len(green) == 1:
				green = "0%s" % green
			blue = "%x" % int(in_colour.blue / 65535.0 * 255)
			if len(blue) == 1:
				blue = "0%s" % blue
			in_colour = "#%s%s%s" % (red, green, blue)
			self.icon.props.xo_color = XoColor("%s,%s" % (new_colour, in_colour))
		if type == "in":
			out_colour = self.out_colour_selector.get_current_color()
			red = "%x" % int(out_colour.red / 65535.0 * 255)
			if len(red) == 1:
				red = "0%s" % red
			green = "%x" % int(out_colour.green / 65535.0 * 255)
			if len(green) == 1:
				green = "0%s" % green
			blue = "%x" % int(out_colour.blue / 65535.0 * 255)
			if len(blue) == 1:
				blue = "0%s" % blue
			out_colour = "#%s%s%s" % (red, green, blue)
			self.icon.props.xo_color = XoColor("%s,%s" % (out_colour, new_colour))
	
	def apply(self, widget):
		nick = unicode(self.name_entry.get_text(), 'utf-8')
		if nick != self.current_nick:
			self.client.set_string("/desktop/sugar/user/nick", nick)
		colour = self.icon._buffer.xo_color.to_string()
		if colour != self.current_colour:
			self.client.set_string("/desktop/sugar/user/color", colour)
	
	def __init__(self, handle):
		activity.Activity.__init__(self, handle)
		self.client = gconf.client_get_default()
		self.current_nick = self.client.get_string("/desktop/sugar/user/nick")
		self.current_colour = self.client.get_string("/desktop/sugar/user/color")
		self.current_colours = _parse_string(self.current_colour)
		self.toolbox = activity.ActivityToolbox(self)
		activity_toolbar = self.toolbox.get_activity_toolbar()
		activity_toolbar.share.props.visible = False
		activity_toolbar.keep.props.visible = False
		self.ok_button = ToolButton(icon)
		self.ok_button.props.tooltip = "Aplicar"
		self.ok_button.connect("clicked", self.apply)
		self.ok_button.show()
		activity_toolbar.insert(self.ok_button, 2)
		self.set_toolbox(self.toolbox)
		self.toolbox.show()
		
		self.canvas = gtk.VBox()
		name_box = gtk.HBox()
		self.canvas.pack_start(name_box, True, True, 5)
		name_label = gtk.Label("Nombre:")
		self.name_entry = gtk.Entry()
		self.name_entry.set_text(self.current_nick)
		name_label.show()
		self.name_entry.show()
		name_box.pack_start(name_label, False, True, 0)
		name_box.pack_start(self.name_entry, True, True, 0)
		name_box.show()
		
		self.colour_picker = gtk.HBox()
		
		selectors = gtk.VBox()
		self.out_colour_selector = gtk.ColorSelection()
		self.out_colour_selector.set_current_color(gtk.gdk.color_parse(self.current_colours[0]))
		self.out_colour_selector.connect("color-changed", self.colour_changed_callback, "out")
		self.out_colour_selector.show()
		selectors.pack_start(self.out_colour_selector, True, True, 0)
		
		self.in_colour_selector = gtk.ColorSelection()
		self.in_colour_selector.set_current_color(gtk.gdk.color_parse(self.current_colours[1]))
		self.in_colour_selector.connect("color-changed", self.colour_changed_callback, "in")
		self.in_colour_selector.show()
		selectors.pack_start(self.in_colour_selector, True, True, 0)
		
		selectors.show()
		self.colour_picker.pack_start(selectors, True, True, 0)
		
		self.xo_icon = gtk.EventBox()
		self.icon = Icon(pixel_size = style.XLARGE_ICON_SIZE)
		self.icon.props.xo_color = XoColor(self.current_colour)
		self.icon.props.icon_name = 'computer-xo'
		self.icon.props.pixel_size = style.XLARGE_ICON_SIZE
		self.icon.show()
		self.xo_icon.add(self.icon)
		self.xo_icon.show()
		self.colour_picker.pack_start(self.xo_icon)
		self.canvas.pack_start(self.colour_picker, True, True, 5)
		self.colour_picker.show()
		
		self.canvas.show()
		self.set_canvas(self.canvas)
		
		self.show()
	
	def write_file(self, file_path):
		raise NotImplementedError
	
	def read_file(self, file_path):
		raise NotImplementedError
