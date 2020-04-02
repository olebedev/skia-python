import skia
import pytest


# @pytest.fixture(scope='session')
# def opengl():
#     from OpenGL.GLUT import glutInit, glutCreateWindow, glutHideWindow
#     glutInit()
#     glutCreateWindow('Hidden window for OpenGL context')
#     glutHideWindow()


@pytest.fixture(scope='session')
def opengl():
    import glfw
    if not glfw.init():
        raise RuntimeError('glfw.init() failed')
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    context = glfw.create_window(640, 480, '', None, None)
    glfw.make_context_current(context)
    yield context


@pytest.fixture(scope='module', params=['raster', 'gpu'])
def surface(request, opengl):
    if request.param == 'gpu':
        context = skia.GrContext.MakeGL()
        info = skia.ImageInfo.MakeN32Premul(320, 240)
        yield skia.Surface.MakeRenderTarget(context, skia.Budgeted.kNo, info)
    else:
        yield skia.Surface(320, 240)


def test_Surface_init():
    import numpy as np
    array = np.zeros((240, 320, 4), dtype=np.uint8)
    assert isinstance(skia.Surface(array), skia.Surface)
    assert isinstance(skia.Surface.MakeRasterN32Premul(320, 240), skia.Surface)


def test_Surface_methods(surface):
    assert surface.width() == 320
    assert surface.height() == 240
    assert isinstance(surface.imageInfo(), skia.ImageInfo)
    assert isinstance(surface.getCanvas(), skia.Canvas)
    assert isinstance(surface.generationID(), int)
    assert isinstance(surface.makeSurface(
        skia.ImageInfo.MakeN32Premul(120, 120)), skia.Surface)
    assert isinstance(surface.makeSurface(120, 120), skia.Surface)
    assert isinstance(surface.makeImageSnapshot(), skia.Image)
    assert isinstance(
        surface.makeImageSnapshot(skia.IRect(100, 100)), skia.Image)
    surface.draw(surface.getCanvas(), 0, 0, None)
