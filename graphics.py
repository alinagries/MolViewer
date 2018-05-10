from vispy import io
from vispy.util.transforms import perspective, translate, rotate, scale
from vispy.geometry import create_sphere, create_cylinder
from vispy.gloo import Program, VertexBuffer, IndexBuffer
import numpy as np

vertex = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float drawHorizon;
uniform vec3 color;
attribute vec3 position;
varying vec3 fragColor;
varying float alpha_drawHorizon;
varying vec4 pos;
void main()
{
    alpha_drawHorizon = drawHorizon;
    fragColor = color;
    pos = vec4(position,1.0);
    gl_Position = (projection * view * model * pos);
}
"""

fragment = """

varying vec4 pos;
varying float alpha_drawHorizon;
varying vec3 fragColor;
void main()
{

    float alpha;
    if (alpha_drawHorizon+0.2 < pos.z) {
        alpha = 1.0;
        }
    else if (alpha_drawHorizon-0.2 > pos.z) {
        alpha = 0.0;
        }
    else {
        float x = pos.z - alpha_drawHorizon + 0.2;
        alpha = -11.25 * (x*x) + 4.75 * x;
        }
        
    gl_FragColor = vec4(fragColor, alpha);
}
"""

class StandartGraphic:
    def __init__(self, program, indices, kind):

        '''

        Hier werden alle self.(...) Variablen initiiert und die Parameter ihren Variablen zugeordnet.

        Parameter:  program und indices sind die Punkte die die Grafik darstellen sollen
                    durch kind kann man die Objekte leichter auseinanderhalten, wenn man
                    z.B. nur die Wasserstoffatomgrafiken ansprechen will.
        Rueckgabewerte: -

        '''
        
        self._program = program
        self._indices = indices

        self.kind = kind
        
        self._translation = (0, 0, 0)
        self._rotation = rotate(0, (1, 1, 1))
        self._scaling = scale((1, 1, 1))

        self._drawType = 'points'


    def draw(self):
        
        '''

        Da mehrere Grafiken aus Gruenden der Effizienz auf ein Programm zugreifen, muss eine
        Grafik bei jedem "draw-call" seine Daten in das Modell des Programms laden. Erst dann
        kann es den "draw-call" an das Programm weitergeben

        Parameter: -
        Rueckgabewerte: -

        '''
        
        self._uploadToModel()
        self._program.draw(self._drawType, self._indices)

    def _uploadToModel(self):
        self._program['model'] = self._scaling.dot(self._rotation).dot(translate(self._translation)) #unsauber

    def setDrawType(self, t):
        self._drawType = t

    def getTranslation(self):
        return self._translation

    def setTranslation(self, t):
        self._translation = t

    def getRotation(self):
        return self._rotation

    def setRotation(self, r):
        self._rotation = r

    def getScaling(self):
        return self._scaling

    def setScaling(self, s):
        self._scaling = s



class GpaphicBlueprint:
    def __init__(self):
        self.kind = ''
        self._color = (0, 0, 0)
        self._program = None
        self._indices = None
        self._mesh = None

    def getProgram(self):
        return self._program

    def getIndices(self):
        return self._indices
    
    def setColor(self, newColor):
        
        '''

        Mit dieser Methode koennen andere Klassen die Farb-Uniform des _programs setzen.

        Parameter: newColor
        Rueckgabewerte: -

        '''
                
        self._color = newColor
        self._program['color'] = self._color

    def buildProgram(self):

        '''

        In dieser Methode wird das Programm samt Indices einer Kugel errechnet. Das Ganze wird mithilfe der
        Bibliothek vispy.gloo gemacht.

        Parameter: -
        Rueckgabewerte: -

        '''

        vertices = np.zeros(self._mesh.getVertices().shape[0] , [("position", np.float32, 3)])
        vertices["position"] = self._mesh.getVertices()
        vertices = VertexBuffer(vertices)
        indices = self._mesh.getIndices()
        self._indices = IndexBuffer(indices)
        self._program = Program(vertex, fragment)
        self._program.bind(vertices)
        self._program['color'] = self._color
        self._program['model'] = None
        self._program['view'] = None
        self._program['drawHorizon'] = -3



class ArcheTypeSphere(GpaphicBlueprint):
    def __init__(self):
        GpaphicBlueprint.__init__(self)
        self.kind = 'sphere'
        oldMesh = create_sphere(10, 20)
        self._mesh = Mesh(oldMesh.get_vertices(), oldMesh.get_faces())
        self.buildProgram()



class ArcheTypeZylinder(GpaphicBlueprint):
    def __init__(self):
        GpaphicBlueprint.__init__(self)
        self.kind = 'zylinder'
        self._color = [0.5, 0.5, 0.5]
        oldMesh = create_cylinder(10, 10)
        self._mesh = Mesh(oldMesh.get_vertices(), oldMesh.get_faces())
        self.buildProgram()

class TwoGraphic(GpaphicBlueprint):
    def __init__(self):
        GpaphicBlueprint.__init__(self)
        vertices, indices, normals, _ = io.read_mesh('2.obj')
        self._mesh = Mesh(vertices, indices)
        self._color = (1, .5 , .2)
        self.buildProgram()


class ThreeGraphic(GpaphicBlueprint):
    def __init__(self):
        GpaphicBlueprint.__init__(self)
        vertices, indices, normals, _ = io.read_mesh('3.obj')
        self._mesh = Mesh(vertices, indices)
        self._color = (1, .5 , .2)
        self.buildProgram()


class C_Atom(ArcheTypeSphere):
    def __init__(self):
        ArcheTypeSphere.__init__(self)
        self._color = [0.0, 1.0, 0.5]
        self.kind = 'C'

class H_Atom(ArcheTypeSphere):
    def __init__(self):
        ArcheTypeSphere.__init__(self)
        self._color = [0.0, 0.0, 1.0]
        self.kind = 'H'

class O_Atom(ArcheTypeSphere):
    def __init__(self):
        ArcheTypeSphere.__init__(self)
        self._color = [1.0, 0.0, 0.0]
        self.kind = 'O'

class Mesh:
    def __init__(self, vertices, indices):
        self._vertices = vertices
        self._indices = indices

    def getVertices(self):
        return self._vertices

    def getIndices(self):
        return self._indices
