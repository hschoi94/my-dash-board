from diagrams.onprem.container import Docker
from diagrams import Diagram, Edge, Node
from diagrams.onprem.database import Mariadb
from diagrams.generic.os import Ubuntu
from diagrams.programming.framework import Flask

with Diagram('server diagram', show=False):
    docker = Docker('image')
    mariadb = Mariadb("data")
    ubuntu = Ubuntu('web')
    docker >> mariadb
    docker >> ubuntu >> Flask("website")

