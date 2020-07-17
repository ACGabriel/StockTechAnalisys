# =============================================================================
# def plotZoomMouseWheel(plt, axArray,base_scale = 2.):
#     def zoom_fun(event):
#         for ax in axArray
#             # get the current x and y limits
#             cur_xlim = ax.get_xlim()
#             cur_ylim = ax.get_ylim()
#             cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
#             cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
#             xdata = event.xdata # get event x location
#             ydata = event.ydata # get event y location
#             if event.button == 'up':
#                 # deal with zoom in
#                 scale_factor = 1/base_scale
#             elif event.button == 'down':
#                 # deal with zoom out
#                 scale_factor = base_scale
#             else:
#                 # deal with something that should never happen
#                 scale_factor = 1
#                 print(event.button)
#             # set new limits
#             ax.set_xlim([xdata - cur_xrange*scale_factor,
#                          xdata + cur_xrange*scale_factor])
#             ax.set_ylim([ydata - cur_yrange*scale_factor,
#                          ydata + cur_yrange*scale_factor])
#         plt.draw() # force re-draw
# 
#     fig = ax.get_figure() # get the figure of interest
#     # attach the call back
#     fig.canvas.mpl_connect('scroll_event',zoom_fun)
# 
#     #return the function
#     return zoom_fun
# =============================================================================


def _get_limits( ax ):
    """ Return X and Y limits for the passed axis as [[xlow,xhigh],[ylow,yhigh]]
    """
    return [list(ax.get_xlim()), list(ax.get_ylim())]

def _set_limits( ax, lims ):
    """ Set X and Y limits for the passed axis
    """
    ax.set_xlim(*(lims[0]))
    ax.set_ylim(*(lims[1]))
    return

def pre_zoom( fig ):
    """ Initialize history used by the re_zoom() event handler.
        Call this after plots are configured and before pyplot.show().
    """
    global oxy
    oxy = [_get_limits(ax) for ax in fig.axes]
    # :TODO: Intercept the toolbar Home, Back and Forward buttons.
    return

def re_zoom(event):
    """ Pyplot event handler to zoom all plots together, but permit them to
        scroll independently.  Created to support eyeball correlation.
        Use with 'motion_notify_event' and 'button_release_event'.
    """
    global oxy
    for ax in event.canvas.figure.axes:
        navmode = ax.get_navigate_mode()
        if navmode is not None:
            break
    scrolling = (event.button == 1) and (navmode == "PAN")
    if scrolling:                   # Update history (independent of event type)
        oxy = [_get_limits(ax) for ax in event.canvas.figure.axes]
        return
    if event.name != 'button_release_event':    # Nothing to do!
        return
    # We have a non-scroll 'button_release_event': Were we zooming?
    zooming = (navmode == "ZOOM") or ((event.button == 3) and (navmode == "PAN"))
    if not zooming:                 # Nothing to do!
        oxy = [_get_limits(ax) for ax in event.canvas.figure.axes]  # To be safe
        return
    # We were zooming, but did anything change?  Check for zoom activity.
    changed = None
    zoom = [[0.0,0.0],[0.0,0.0]]    # Zoom from each end of axis (2 values per axis)
    for i, ax in enumerate(event.canvas.figure.axes): # Get the axes
        # Find the plot that changed
        nxy = _get_limits(ax)
        if (oxy[i] != nxy):         # This plot has changed
            changed = i
            # Calculate zoom factors
            for j in [0,1]:         # Iterate over x and y for each axis
                # Indexing: nxy[x/y axis][lo/hi limit]
                #           oxy[plot #][x/y axis][lo/hi limit]
                width = oxy[i][j][1] - oxy[i][j][0]
                # Determine new axis scale factors in a way that correctly
                # handles simultaneous zoom + scroll: Zoom from each end.
                zoom[j] = [(nxy[j][0] - oxy[i][j][0]) / width,  # lo-end zoom
                           (oxy[i][j][1] - nxy[j][1]) / width]  # hi-end zoom
            break                   # No need to look at other axes
    if changed is not None:
        for i, ax in enumerate(event.canvas.figure.axes): # change the scale
            if i == changed:
                continue
            for j in [0,1]:
                width = oxy[i][j][1] - oxy[i][j][0]
                nxy[j] = [oxy[i][j][0] + (width*zoom[j][0]),
                          oxy[i][j][1] - (width*zoom[j][1])]
            _set_limits(ax, nxy)
        event.canvas.draw()         # re-draw the canvas (if required)
        pre_zoom(event.canvas.figure)   # Update history
    return
# End re_zoom()