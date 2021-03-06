from .PathsFinder import PathsFinder
from .Gradle import Gradle
from .ProjectController import ProjectController

class Configurator(object):

    def __init__(self, vim):
        self.vim = vim

    def setupJavacomplete(self):
        classpath = ':'.join(PathsFinder().getAllClassPaths())
        
        self.vim.command("call javacomplete#ClearCache()")
        self.vim.command("call javacomplete#TerminateServer()")
        self.vim.command("sleep 400m") #Allow for the server to terminate
        self.vim.command("let g:JavaComplete_LibsPath = '" + classpath + "'")
        self.vim.command("call javacomplete#StartServer()")
    def setupSyntastic(self):
        classpath = []
        classpath.extend(PathsFinder().getAllClassPaths())
        classpath.extend(PathsFinder().getAllSourcePaths())
        
        sourcepath = ':'.join(classpath)
        self.vim.command("let g:syntastic_java_javac_classpath = '" + sourcepath + "'")

    def generatePaths(self, async=False):
        if ProjectController().isGradleProject():
            Gradle(self.vim).outputPaths(async)

    def setupVimStudio(self):
        Project = ProjectController()
        if Project.isGradleProject() and not Project.isGradleSetup():
            Project.setupEnvironment()

    def genPathsIfNone(self):
        if not ProjectController().isVimStudioReady():
            self.generatePaths()

    def genPathsAndSetup(self):
        if ProjectController().isGradleProject():
            self.setupVimStudio()
            self.genPathsIfNone()
            self.setupJavacomplete()
            self.setupSyntastic()
