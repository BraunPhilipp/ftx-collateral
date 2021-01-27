#!/usr/bin/env python3
import math
import numpy
import random
import matplotlib
import matplotlib.pyplot

cmap = matplotlib.cm.get_cmap("plasma", 100) # color map

ox   = 0.0   # x-position of the plot center
oy   = 0.0   # y-position of the plot center
phi0 = 0.0   # angle of the first axis with respect to the universal x-axis (horizontal line)

axis_length = 0.8   # axis length in terms of the plot radius. Plot radius equals half of the plot width.

axis_arrow_head_pad = 0.05   # extension of an axis beyond its maximum value
axis_label_pad      = 0.25   # distance between the axis maximum value and its label, along the axis direction

n_tick = 5                  # number of divisions (ticks) on each axis
major_tick_length  = 0.015   # length of MAJOR tick markers (the last marker)
minor_tick_length  = 0.010   # length of MINOR tick markers
origin_circle_size = major_tick_length / 2   # size of the marker at the origin

tick_label_format = "%.1f"              # format of the major-tick label
tick_label_parallel_pad      = 0.00   # distance between the axis major tick and its label, along the axis direction
tick_label_perpendicular_pad = 0.08   # distance between the axis major tick and its label, along the direction perpendicular to the axis

point_circle_size  = 0.008   # size of the marker at every polygon vertex

hide_plot_frame = True   # whether to hide the subplot frame

# settings for a colorfull plot
plot_title_properties = {'color':'black', 'fontsize':20, 'horizontalalignment':'center', 'verticalalignment':'center'}
tick_label_properties = {'color':'blue',  'fontsize':10, 'horizontalalignment':'center', 'verticalalignment':'center'}
axis_label_properties = {'color':'red',   'fontsize':10, 'horizontalalignment':'center', 'verticalalignment':'center'}

axis_arrow_properties      = {'linestyle':'-', 'linewidth':1.0, 'facecolor':'red', 'edgecolor':'red'}

axis_minor_tick_properties = {'linestyle':'-', 'linewidth':1.0, 'solid_capstyle':'round', 'color':'blue'}
axis_major_tick_properties = {'linestyle':'-', 'linewidth':2.0, 'solid_capstyle':'round', 'color':'blue'}
polygon_line_properties    = {'linestyle':'-', 'linewidth':3.0, 'solid_capstyle':'round', 'color':'green', 'alpha':0.5}

origin_circle_properties   = {'linestyle':'-', 'linewidth':2.0, 'edgecolor':'blue',  'facecolor':'none'}
point_circle_properties    = {'linestyle':'-', 'linewidth':1.0, 'edgecolor':'green', 'facecolor':'none'}

# settings for a black-and-white plot
plot_title_properties = {'color':'black', 'fontsize':20, 'horizontalalignment':'center', 'verticalalignment':'center'}
tick_label_properties = {'color':'black', 'fontsize':10, 'horizontalalignment':'center', 'verticalalignment':'center'}
axis_label_properties = {'color':'black', 'fontsize':10, 'horizontalalignment':'center', 'verticalalignment':'center'}

axis_arrow_properties      = {'linestyle':'-', 'linewidth':1.0, 'facecolor':'black', 'edgecolor':'black'}

axis_minor_tick_properties = {'linestyle':'-', 'linewidth':1.0, 'solid_capstyle':'round', 'color':'black'}
axis_major_tick_properties = {'linestyle':'-', 'linewidth':2.0, 'solid_capstyle':'round', 'color':'black'}
polygon_line_properties    = {'linestyle':'-', 'linewidth':3.0, 'solid_capstyle':'round', 'color':'gray', 'alpha':0.5}

origin_circle_properties   = {'linestyle':'-', 'linewidth':2.0, 'edgecolor':'black', 'facecolor':'none'}
point_circle_properties    = {'linestyle':'-', 'linewidth':1.0, 'edgecolor':'black', 'facecolor':'none'}


class MultipleAxisPlot:

    def __init__(self, width=8.0, height=8.0):
        self.figure = matplotlib.pyplot.figure(figsize=(width,height))

        if hide_plot_frame:
            min_dim = min(width, height)
        else:
            min_dim = min(width, height) * 0.9
        
        pad1  = (width - min_dim) / (width * 2)
        size1 = min_dim / width
        pad2  = (height - min_dim) / (height * 2)
        size2 = min_dim / height
        self.subplot = self.figure.add_subplot(1,1,1, position=[pad1, pad2, size1, size2])
        if hide_plot_frame:
            matplotlib.pyplot.axis('off')

        x_min_view = -1.4
        x_max_view =  1.4
        self.subplot.xaxis.set_view_interval(x_min_view, x_max_view)
        self.subplot.set_xlim(left=x_min_view, right=x_max_view)

        y_min_view = -1.4
        y_max_view =  1.4
        self.subplot.yaxis.set_view_interval(y_min_view, y_max_view)
        self.subplot.set_ylim(bottom=y_min_view, top=y_max_view)

        self.n_axis = 0
        self.end_points = []
        self.maxvals = None


    def drawAxis(self, maxvals, names):
        self.maxvals = maxvals
        self.n_axis = len(maxvals)

        # circle = matplotlib.pyplot.Circle((ox, oy), major_tick_length, **origin_circle_properties)
        # self.subplot.add_patch(circle)

        delta_phi = 2 * math.pi / self.n_axis
        for i_axis in range(0, self.n_axis):
            phi = phi0 + i_axis * delta_phi
            dx = math.cos(phi)
            dy = math.sin(phi)

            delta_x = axis_length * dx
            delta_y = axis_length * dy

            # the coordinates of the axis maximum value
            x_end = ox + delta_x
            y_end = oy + delta_y
            self.end_points.append([x_end, y_end])

            # drawing axis line (actually it is an arrow)
            x = x_end + dx * axis_arrow_head_pad
            y = y_end + dy * axis_arrow_head_pad
            matplotlib.pyplot.arrow(ox, oy, x-ox, y-oy, head_width=3*minor_tick_length, head_length=4*minor_tick_length, **axis_arrow_properties)

            # writing axis label
            x = x_end + dx * (axis_arrow_head_pad + axis_label_pad)
            y = y_end + dy * (axis_arrow_head_pad + axis_label_pad / 1.5)
            self.subplot.text(x, y, names[i_axis], **axis_label_properties)

            # writing axis maximum value
            x = x_end + dx * tick_label_parallel_pad - dy * tick_label_perpendicular_pad
            y = y_end + dy * tick_label_parallel_pad + dx * tick_label_perpendicular_pad
            label = tick_label_format % maxvals[i_axis]
            self.subplot.text(x, y, label, **tick_label_properties)

            delta_x = delta_x / n_tick
            delta_y = delta_y / n_tick
            for i_tick in range(1, n_tick):
                x = ox + i_tick * delta_x
                y = oy + i_tick * delta_y
                x1 = x + dy * minor_tick_length
                y1 = y - dx * minor_tick_length
                x2 = x - dy * minor_tick_length
                y2 = y + dx * minor_tick_length
                line = matplotlib.lines.Line2D([x1, x2], [y1, y2], transform=self.subplot.transData, figure=self.figure, **axis_minor_tick_properties)
                self.figure.lines.extend([line])
            
            x1 = x_end + dy * major_tick_length
            y1 = y_end - dx * major_tick_length
            x2 = x_end - dy * major_tick_length
            y2 = y_end + dx * major_tick_length
            line = matplotlib.lines.Line2D([x1, x2], [y1, y2], transform=self.subplot.transData, figure=self.figure, **axis_major_tick_properties)
            self.figure.lines.extend([line])


    def drawPolygon(self, values, alpha=0.5):
        ratio = [values[i] / self.maxvals[i] for i in range(0, self.n_axis)]
        [x1, y1] = [x * ratio[-1] for x in self.end_points[-1]]
        points = []

        for i_axis in range(0, self.n_axis):
            circle = matplotlib.pyplot.Circle((x1, y1), point_circle_size, **point_circle_properties)
            self.subplot.add_patch(circle)

            [x2, y2] = [x * ratio[i_axis] for x in self.end_points[i_axis]]
            points.append([x1, y1])

            polygon_line_properties = {'linestyle':'-', 'linewidth':1.0, 'solid_capstyle':'round', 'color':'black', 'alpha':alpha}
            line = matplotlib.lines.Line2D([x1, x2], [y1, y2], transform=self.subplot.transData, figure=self.figure, **polygon_line_properties)
            self.figure.lines.extend([line])
            [x1, y1] = [x2, y2]

        polygon_properties = {'fill':True, 'color':cmap(random.randint(0, 100)), 'alpha':alpha}
        line = matplotlib.patches.Polygon(points, closed=None, transform=self.subplot.transData, figure=self.figure, **polygon_properties)
        self.figure.lines.extend([line])

        circle = matplotlib.pyplot.Circle((x1, y1), point_circle_size, **point_circle_properties)
        self.subplot.add_patch(circle)


    def drawArbitraryPolygon(self, axes, values):
        ratio = [values[i] / self.maxvals[i] for i in range(0, len(axes))]
        [x1, y1] = [x * ratio[-1] for x in self.end_points[axes[-1]]]
        for i_axis in range(0, len(axes)):
            circle = matplotlib.pyplot.Circle((x1, y1), point_circle_size, **point_circle_properties)
            self.subplot.add_patch(circle)

            [x2, y2] = [x * ratio[i_axis] for x in self.end_points[axes[i_axis]]]
            line = matplotlib.lines.Line2D([x1, x2], [y1, y2], transform=self.subplot.transData, figure=self.figure, **polygon_line_properties)
            self.figure.lines.extend([line])
            [x1, y1] = [x2, y2]
        
        circle = matplotlib.pyplot.Circle((x1, y1), point_circle_size, **point_circle_properties)
        self.subplot.add_patch(circle)


    def savePlot(self, filename, save_properties={}):
        matplotlib.pyplot.savefig(filename, **save_properties)
        #matplotlib.pyplot.show()


if __name__ == "__main__":

    # plot 3
    plot = MultipleAxisPlot(8, 8)
    plot.drawAxis(maxvals=[10.0, 20.0, 30.0], names=["SRMUSD", "BTCUSD", "ETHUSD"])

    plot.drawPolygon([8.0,  6.0,  3.0])
    plot.drawPolygon([4.0, 12.0, 10.0])
    #plot.drawArbitraryPolygon([1, 2, 3], [4.0, 3.6, 2.1])

    plot.savePlot("plot3.pdf")
    plot.savePlot("plot3.png")
    plot.savePlot("plot3_hd.png", {'dpi':300})

    # plot 4
    plot = MultipleAxisPlot()
    plot.drawAxis(maxvals=[10.0, 20.0, 30.0, 1.0], names=["a", "b", "c", "d"])

    plot.drawPolygon([8.0, 6.0, 3.0, 0.5])
    #plot.drawArbitraryPolygon([1, 2, 3], [4.0, 3.6, 2.1])

    plot.savePlot("plot4.pdf")
    plot.savePlot("plot4.png")

    # plot 5
    plot = MultipleAxisPlot()
    plot.drawAxis(maxvals=[10.0, 20.0, 30.0, 1.0, 100.0], names=["a", "b", "c", "d", "e"])

    plot.drawPolygon([8.0, 6.0, 3.0, 0.5, 80.0])
    #plot.drawArbitraryPolygon([1, 2, 3], [4.0, 3.6, 2.1])

    plot.savePlot("plot5.pdf")
    plot.savePlot("plot5.png")
