from ui import PygameDisplay
import wx
import pygame


class SceneBase(object):

    def __init__(self):
        self.next = self
        self.context = {}

    def input_code(self, source):
        try:
            compiled = compile(source, '<string>', 'exec') # gives syntax error
            exec(compiled, self.context) # gives generic exceptions
        except SyntaxError, e:
            print 'syntax error', e
        except Exception, e:
            print 'exception', e

    def update(self, deltaTime):
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

    def pygame_redraw(self, deltaTime):
        self.active_scene.update(deltaTime)
        self.active_scene.render(self.screen)
        self.active_scene = self.active_scene.next


class PirateBlock(SceneBase):

    def __init__(self):
        self.next = self
        self.block = (40,40)
        self.context = {'x': 30, 'y': 30}

    def update_context(self, context):
        pass

    def update(self, deltaTime):
        pass

    def render(self, screen):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,0,0), (self.context['x'], self.context['y'], 50, 50))
