# -*- coding: utf-8 -*-
"""
PathPatchDemo.py

from: 
https://matplotlib.org/examples/shapes_and_collections/path_patch_demo.html

Created on Fri Jul 14 08:21:35 2017

@author: slehar
"""
"""
Demo of a PathPatch object.
"""
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


plt.close('all')
fig, ax = plt.subplots()
ax.set_xlim([-1., 1.])
ax.set_ylim([-1., 1.])

Path = mpath.Path
path_data = [
    (Path.MOVETO, ( 0.0, -0.5)),
    (Path.CURVE4, (-0.2, -0.2)),
    (Path.CURVE4, (-0.2,  0.2)),
    (Path.CURVE4, ( 0.0,  0.0)),
    (Path.CURVE4, ( 0.2,  0.2)),
    (Path.CURVE4, ( 0.2, -0.2)),
    (Path.CURVE4, ( 0.0, -0.5)),
    (Path.CLOSEPOLY, (0.0, -0.5)),
    ]
codes, verts = zip(*path_data)
path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
ax.add_patch(patch)

# plot control points and connecting lines
x, y = zip(*path.vertices)
line, = ax.plot(x, y, 'go-')

ax.grid()
plt.show()

# Gef fig manager to raise window in top left corner (10,10)
# figmgr=plt.get_current_fig_manager()
# figmgr.canvas.manager.window.raise_()
# geom=figmgr.window.geometry()
# (xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
# figmgr.window.setGeometry(10,10,dxWidth,dyHeight)

