# -*- coding: utf-8 -*-
import os
import sys

from docutils import core, nodes, writers
from docutils.parsers.rst import roles

import sublime
import sublime_plugin


visitor = []


class RstInsightCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    # Read all the files/views
    rst_views = []
    for win in sublime.windows():
        rst_views += filter(self._filter_rst_files, win.views())

    # Make the list unique
    rst_views = list(set(rst_views))

    try:
      register_sphinx_support()
    except Warning, e:
      print e

    print rst_views
    for rst_view in rst_views:
      print 'Parsing: %s' % rst_view.file_name()
      writer = MyWriter()
      output = core.publish_file(source_path=rst_view.file_name(), writer=writer)
    #self.view.insert(edit, 0, "Hello, You")
    print 'type: %s' % type(output)
    print visitor
    pass

  def _filter_rst_files(self, view):
    """
    Helper function to get RST files from views
    """
    # Check existance
    fpath = view.file_name()
    if not fpath:
      return False

    # Check extension
    # TODO: Is there way to check syntax name from view?
    name, ext = os.path.splitext(fpath)
    if ext not in (u'.rst', u'.txt'):
      return False

    return True


class RstListener(sublime_plugin.EventListener):
  """Listens for saved files and updates cache"""

  def on_post_save(self, view):
    print '---saved: %s' % view.file_name()


class GenericNodeVisitor(nodes.NodeVisitor):
    """

    """
    def default_visit(self, node):
      pass

    def default_departure(self, node):
      pass

    def unknown_visit(self, node):
      pass
      print 'odd: %s (%s)' % (node, node.__class__)

    def unknown_departure(self, node):
      pass

    def visit_target(self, node):
      print 'Found target: %s' % node
      print 'Found: %s' % type(node)

    def visit_reference(self, node):
      print 'Found reference: %s' % node
      print 'Found: %s' % type(node)


class MyWriter(writers.Writer):
  """
  This docutils writer will use the MyHTMLTranslator class below.

  """
  def __init__(self):
      writers.Writer.__init__(self)
      self.translator_class = GenericNodeVisitor

  def translate(self):
    self.visitor = visitor = self.translator_class(self.document)
    self.document.walkabout(visitor)
    self.output = 'hahaa'


def register_sphinx_support():
  sroles = None
  try:
    # NOTE: For some reason, argv may be missing in ST python
    sys.argv = getattr(sys, 'argv', [])
    from sphinx import roles as sroles
    from sphinx import addnodes
  except ImportError, err:
    raise Warning('Sphinx not found, continuing without: %s' % err)

  print '=== Registered with Sphinx support!'

  generic_docroles = sroles.generic_docroles
  specific_docroles = sroles.specific_docroles

  for rolename, nodeclass in generic_docroles.items():
    generic = roles.GenericRole(rolename, nodeclass)
    role = roles.CustomRole(rolename, generic, {'classes': [rolename]})
    roles.register_local_role(rolename, role)

  for rolename, func in specific_docroles.items():
      roles.register_local_role(rolename, func)


  print [k for k in dir(addnodes) if k != 'nodes' and k[0] != '_']

  nodes._add_node_class_names(k for k in dir(addnodes) if k != 'nodes' and k[0] != '_')



  def dummy_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    return [], []

