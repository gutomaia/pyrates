from ui import PygameDisplay
import wx
import pygame


class SceneBase(object):

    def __init__(self):
        self.next = self
        self.context = {}

    def input_code(self, source):
        try:
            compiled = compile(source, '<string>', 'exec')
            exec(compiled, self.context)
        except SyntaxError, e:
            print 'syntax error'
        except Exception, e:
            pass

    def update(self):
        pass

    def render(self, screen):
        pass

    def go_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.go_to_scene(None)


class DisplayScene(PygameDisplay):

    def __init__(self, parent, ID, starting_scene=None):
        super(DisplayScene, self).__init__(parent, ID)
        if not starting_scene:
            self.active_scene = PirateBlock()
        else:
            self.active_scene = starting_scene

    def pygame_redraw(self):
        self.active_scene.update()
        self.active_scene.render(self.screen)
        self.active_scene = self.active_scene.next


class TitleScene(SceneBase):

    def update(self):
        pass

    def render(self, screen):
        screen.fill((255, 0, 0))


class PirateBlock(SceneBase):

    def __init__(self):
        self.next = self
        self.block = (40,40)
        self.context = {'x': 30, 'y': 30}

    def update_context(self, context):
        pass

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,0,0), (self.context['x'], self.context['y'], 50, 50))
