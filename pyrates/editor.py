import wx
import wx.stc as stc


class SourceEditor(stc.StyledTextCtrl):

    def __init__(self, parent, style=wx.SIMPLE_BORDER):
        super(SourceEditor, self).__init__(parent, style=style)
        self.SetUseTabs(False)
        self.SetTabWidth(4)
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginType(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginWidth(2, 12)

        self.SetLexer(stc.STC_LEX_PYTHON)
        # self.StyleClearAll()
