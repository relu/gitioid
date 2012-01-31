# -*- coding: utf-8 -*-

# Copyright (C) 2012  Aurel Canciu <aurelcanciu@gmail.com>
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
# along
# with this program; if not, write to the Free Software Foundation,
# Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import KIconLoader
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

from gitio import gitio

import sys, re

class Gitioid(plasmascript.Applet):

	GITHUB_RE = '^https://(www.)?github.com/'
	
	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
		self.setHasConfigurationInterface(False)
		self.setAspectRatioMode(Plasma.Square)
		self.theme = Plasma.Svg(self)
		self.theme.setImagePath("widgets/background")
		self.setBackgroundHints(Plasma.Applet.TranslucentBackground)
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.layout.setOrientation(Qt.Horizontal)
		self.icon = Plasma.IconWidget()
		self.layout.addItem(self.icon)
		self.resize(128, 128)

		self.enabled = True

		self.icons = {}
		self.icons['iconon'] = self.package().path() + 'contents/icons/gitioid-enabled.svg'
		self.icons['iconoff'] = self.package().path() + 'contents/icons/gitioid-disabled.svg'

		self.updateIcon()
		self.connect(self.icon, SIGNAL("doubleClicked()"),
				self.iconDoubleClicked)
		
		self.clipboard = QApplication.clipboard()
		self.connect(self.clipboard, SIGNAL("dataChanged()"),
				self.clipboardDataChanged)

	def updateIcon(self):
		loader = KIconLoader()
		size = min(self.icon.size().width(), self.icon.size().height()) * 2

		if self.enabled:
			ico = KIconLoader.loadIcon(loader,
					self.icons['iconon'], KIconLoader.NoGroup,
					size)
		else:
			ico = KIconLoader.loadIcon(loader,
					self.icons['iconoff'], KIconLoader.NoGroup,
					size)

		paint = QPainter(ico)
		paint.setRenderHint(QPainter.SmoothPixmapTransform)
		paint.setRenderHint(QPainter.Antialiasing)

		paint.end()

		self.icon.setIcon(QIcon(ico))
		self.icon.update()

	def iconDoubleClicked(self):
		self.enabled = False if self.enabled else True

		self.updateIcon()

	def clipboardDataChanged(self):
		md = self.clipboard.mimeData()
		if self.enabled and md.hasText():
			url = str(self.clipboard.text()).strip()

			match = re.match(self.GITHUB_RE, url)
			if match is not None:
				gi = gitio(url)
				shurl = gi.shorturl()
				self.clipboard.setText(shurl)
				self.setToolTip(shurl)

def CreateApplet(parent):
	return Gitioid(parent)
