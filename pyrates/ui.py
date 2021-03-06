import wx, sys, os, pygame

### PYGAME IN WX ###
# A simple test of embedding Pygame in a wxPython frame
#
# By David Barker (aka Animatinator), 14/07/2010
# Patch for cross-platform support by Sean McKean, 16/07/2010
# Patch to fix redrawing issue by David Barker, 20/07/2010
# Second window demo added by David Barker, 21/07/2010
class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = self.GetSizeTuple()
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

    def Update(self, event):
        self.Redraw()

    def Redraw(self):
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False

        self.pygame_redraw(self.timer.GetInterval())

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.ImageFromData(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc

    def pygame_redraw(self, deltaTime):
        self.screen.fill((0,0,0))
        cur = 0

        w, h = self.screen.get_size()
        while cur <= h:
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, h - cur), (cur, 0))

            cur += self.linespacing

    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.GetSizeTuple()
        self.size_dirty = True

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)

ID_ABOUT = 12753

class Frame(wx.Frame):

    def init_menubar(self):
        self.menubar = wx.MenuBar()

        fileMenu = wx.Menu()

        newitem = wx.MenuItem(fileMenu, wx.ID_NEW, text='New', kind = wx.ITEM_NORMAL)
        fileMenu.AppendItem(newitem)

        fileMenu.AppendSeparator()

        quit = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(quit)

        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, ID_ABOUT, text='About', kind = wx.ITEM_NORMAL)
        helpMenu.AppendItem(aboutItem)

        self.menubar.Append(fileMenu, '&File')
        self.menubar.Append(helpMenu, '&Help')


        self.SetMenuBar(self.menubar)
        self.Bind(wx.EVT_MENU, self.menuhandler)

    def menuhandler(self, event):
        menu_id = event.GetId()
        if menu_id == wx.ID_EXIT:
            self.Kill(event)

    def init_toolbar(self):
        # self.toolbar = self.CreateToolBar(wx.TB_TEXT, wx.TB_NOICONS, -1)
        self.toolbar = self.CreateToolBar()
        run = self.toolbar.AddLabelTool(wx.ID_ANY, 'Run', wx.Bitmap('assets/icons/run.png'))
        self.Bind(wx.EVT_TOOL, self.run_command, run)
        self.toolbar.Realize()

    def run_command(self, event):
        source = self.editor.GetText()
        self.display.active_scene.input_code(source)

    def init_statusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("pyRATES", 0)
        self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size = (600, 600))
        self.SetTitle("Pyrates")

        self.init_menubar()
        self.init_toolbar()
        self.init_statusbar()

        from gameengine import DisplayScene
        self.display = DisplayScene(self, -1)

        # self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)

        self.curframe = 0
        self.timer = wx.Timer(self)

        # self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        self.timer.Start((1000.0 / self.display.fps))

        from editor import SourceEditor
        self.editor = SourceEditor(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.display, 1, flag = wx.EXPAND)
        self.sizer.Add(self.editor, 1, flag = wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

    def Kill(self, event):
        self.display.Kill(event)
        self.Destroy()

    def OnSize(self, event):
        self.Layout()

    def Update(self, event):
        pass
        # self.statusbar.SetStatusText("Frame %i" % self.curframe, 2)

    def OnScroll(self, event):
        self.display.linespacing = self.slider.GetValue()
