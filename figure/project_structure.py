from diagrams import Diagram, Edge, Node

with Diagram('project structure', show=False):
    readme_fig = Node('figure')
    env = Node('env')
    app = Node('app')
    readme = Node('readme')
    readme_fig >> readme
    app >> readme
    env >> Edge(label='envirment', color='red') >> app
    """
    public
    - the web accessible root of the site. 
    Basically whatever is in that folder can be opened 
    from browser address bar. Server won't provide user 
    access to files outside public

    src
    - (short for "source") contains your working files 
    that will be used later to create the build

    """
    web_src = Node('src')
    app - web_src

