from Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.HelpMenuList import HelpMenuList
from Screens.Rc import Rc


class HelpMenu(Screen, Rc):
	def __init__(self, session, list):
		Screen.__init__(self, session)
		self.setTitle(_("help..."))
		self.onSelChanged = []
		self["list"] = HelpMenuList(list, self.close)
		self["list"].onSelChanged.append(self.SelectionChanged)
		Rc.__init__(self)
		self["long_key"] = Label("")

		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self["list"].ok,
			"back": self.close,
		}, -1)

		self.onLayoutFinish.append(self.SelectionChanged)

	def SelectionChanged(self):
		self.clearSelectedKeys()
		selection = self["list"].getCurrent()
		if selection:
			selection = selection[3]
		#arrow = self["arrowup"]
		print "[HelpMenu] selection:", selection

		longText = ""
		if selection and len(selection) > 1:
			if selection[1] == "SHIFT":
				self.selectKey("SHIFT")
			elif selection[1] == "long":
				longText = _("Long key press")
		self["long_key"].setText(longText)

		self.selectKey(selection[0])
		#if selection is None:
		print "[HelpMenu] select arrow"
		#	arrow.moveTo(selection[1], selection[2], 1)
		#	arrow.startMoving()
		#	arrow.show()


class HelpableScreen:
	def __init__(self):
		self["helpActions"] = ActionMap(["HelpActions"],
			{
				"displayHelp": self.showHelp,
			})

	def showHelp(self):
		self.session.openWithCallback(self.callHelpAction, HelpMenu, self.helpList)

	def callHelpAction(self, *args):
		if args:
			(actionmap, context, action) = args
			actionmap.action(context, action)
