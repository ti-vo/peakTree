#! /usr/bin/env python3
# coding=utf-8
"""
Author: radenz@tropos.de

collection of tiny helper functions

"""

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from . import helpers as h

import graphviz
import json


def coord_pattern_child(p):
    """the coordinate pattern required for filtering the dictionary for children"""
    return lambda d: d['coords'][:-1] == p and len(d['coords']) == len(p)+1


def iterchilds(travtree, parentcoord):
    """generator that yields all childs of a parent with given coordinats"""
    for n in list(filter(coord_pattern_child(parentcoord), travtree.values())):
        yield n
        yield from iterchilds(travtree, n['coords'])

def iternodes(travtree):
    """generator that yields a full traversal of the tree"""
    level_no=0
    nodes = list(filter(lambda d: len(d['coords']) == level_no+1, travtree.values()))
    for n in nodes:
        yield n
        yield from iterchilds(travtree, n['coords'])

def travtree2text(travtree, show_coordinats=True):
    """returns a string with the tabular representation of the traversed tree"""
    lines = []
    levels = max(list(map(lambda v: len(v['coords']), travtree.values())))
    if show_coordinats:
        header = ' coordinates '+levels*'  '+ '                     Z       v    width    sk   LDR     t   LDRmax  prom'
    else:
        header = ' '+levels*'  '+ '             Z       v    width    sk   LDR     t   LDRmax  prom'
    lines.append(header)
    
    for v in iternodes(travtree):

        coords = '{:20s}'.format(str(v['coords']))
        bounds = '({:>3d}, {:>3d})'.format(*v['bounds'])
        sp_before = (len(v['coords'])-1)*'  '
        sp_after = (levels-len(v['coords']))*'  '

        mom1 = '{:> 6.2f}, {:> 6.2f}, {:>4.2f}'.format(h.lin2z(v['z']), v['v'], v['width'])
        mom2 = '{:> 3.2f}, {:> 5.1f}, {:> 5.1f}, {:> 5.1f}, {:> 5.1f}'.format(
            v['skew'], h.lin2z(v['ldr']), h.lin2z(v['thres']), h.lin2z(v['ldrmax']), h.lin2z(v['prominence']))
        #mom2 = '{:> 3.2f}, {:> 5.1f}, {:> 5.1f}'.format(v['skew'], h.lin2z(v['ldr']), h.lin2z(v['thres']))
        #txt = "{:>2d}{}{}{}{} {}\n{}{}".format(k, sp_before, bounds, sp_after, mmv, mom1, 33*' ', mom2)
        if show_coordinats:
            txt = "{}{} {}{} {}, {}".format(sp_before, bounds, coords, sp_after, mom1, mom2)
        else:
            txt = "{}{} {} {}, {}".format(sp_before, bounds, sp_after, mom1, mom2)
        lines.append(txt)
    return '\n'.join(lines)


def gen_lines_to_par(travtree):
    """get all the connection lines between the nodes of travtree"""
    chunks = []
    for k,v in travtree.items():
        if v['parent_id'] != -1:
            x = [v['v'], travtree[v['parent_id']]['v']]
            y = [v['z'], travtree[v['parent_id']]['z']]
            chunks.append((x,y))
    return chunks


def plot_spectrum(travtree, spectrum, savepath):
    """
    plot the spectrum together with the traversed tree
    :savepath : path to save or None
    :return : fig, ax
    """
    dt=h.ts_to_dt(spectrum['ts'])

    valid_LDR = np.ma.masked_where(spectrum['specLDRmasked_mask'], spectrum['specZcx'])
    decoupling_threshold = h.z2lin(h.lin2z(spectrum['specZ'])-spectrum['decoupling'])
    
    fig, ax = plt.subplots(1, figsize=(8, 7), sharex=True)

    #plot the tree structure
    for chunk in gen_lines_to_par(travtree):
        ax.plot(chunk[0], h.lin2z(np.array(chunk[1])), '-', color='grey')

    flatten = [(item[1]['v'],item[1]['z']) for item in travtree.items()]
    ax.plot([e[0] for e in flatten], h.lin2z(np.array([e[1] for e in flatten])), 'o', color='r', markersize=5)

    #ax.hlines(h.lin2z(valid_LDR), -10, 10, color='grey')
    ax.step(spectrum['vel'], h.lin2z(spectrum['specLDR']), 
             linewidth=1.5, color='turquoise', where='mid', label='specLDR')
    ax.step(spectrum['vel'], h.lin2z(spectrum['specLDRmasked']), 
             linewidth=1.5, color='blue', where='mid', label='specLDR')

    ax.step(spectrum['vel'], h.lin2z(spectrum['specZ']), 
            linewidth=1.5, color='red', where='mid', label='specZ')
    ax.step(spectrum['vel'], h.lin2z(spectrum['specZcx']), 
            linewidth=1.5, color='crimson', where='mid', label='specZcx')
    ax.step(spectrum['vel'], h.lin2z(valid_LDR), 
            linewidth=1.5, color='blue', where='mid', label='specZcx')
    ax.step(spectrum['vel'], h.lin2z(decoupling_threshold), 
            linewidth=1.5, color='grey', where='mid', label='decoupling')
    ax.set_xlim([-6,3])
    ax.set_ylabel('Reflectivity [dBZ]')
    ax.set_xlabel('Velocity [m s$\\mathregular{^{-1}}$]')
    ax.set_ylim(bottom=-65)
    #special for the convective case
    # ax.set_ylim(bottom=-75)
    # ax.set_xlim([-8.5, 8.5])

    ax.legend(loc='upper right')
    ax.set_title('{} {:0>5.0f} m'.format(dt.strftime('%Y-%m-%d %H:%M:%S'), spectrum['range']))
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.tick_params(axis='both', which='major', width=1.5, right=True, top=True)
    ax.tick_params(axis='both', which='minor', width=1.3, right=True, top=True)
    fig.subplots_adjust(bottom=0.5, top=0.95)


    if travtree != {}:
        txt = travtree2text(travtree, show_coordinats=False)
        ax.text(0.03, 0.42, txt,
                horizontalalignment='left', verticalalignment='top',
                transform=fig.transFigure, fontsize=11, family='monospace',)

    if savepath is not None:
        savename = '{}_{:0>5.0f}m_spectrum.png'.format(dt.strftime('%Y-%m-%d_%H%M%S'), spectrum['range'])
        fig.savefig(savepath + savename, dpi=250)
    return fig, ax

def render_node_table(key, value):
    string = """{} [label=<<font face='helvetica' point-size="9"><table border="0" cellborder="0" cellspacing="0">
       <tr><td colspan='4'><font point-size='12'><B>node {}</B></font></td></tr>
       <tr><td>Z:</td><td align='right'>{:.2f}</td><td>w:</td><td align='right'>{:.2f}</td></tr>
       <tr><td>v:</td><td align='right'>{:.2f}</td><td>s:</td><td align='right'>{:.2f}</td></tr>
     </table></font>>]""".format(key, key, h.lin2z(value['z']), value['width'], value['v'], value['skew'])

    return string

def dot_format(travtree):
    print('dot format travtree', travtree)
    node_props = [render_node_table(*elem) for elem in travtree.items()]
    connections = ['{} -> {};'.format(v['parent_id'], k) for k,v in travtree.items() if not v['parent_id'] == -1]
    string = ['digraph G { graph [fontname = "helvetica"] node [shape=ellipse]'] + node_props + connections + ['}']
    # string = ['graph [fontname = "helvetica"] node [shape=ellipse] ',  
    #           'subgraph cluster1 { '+'label=<<font point-size="11">{} {:0>5.0f}m</font>>'.format(dt.strftime('%Y-%m-%d_%H%M%S'), rg)]\
    #            + node_props + connections + ['}']
    return '\n'.join(string)

def vis_tree(dot):

    src = graphviz.Source(dot)
    return src



def format_for_json(elem):
    if isinstance(elem, np.integer):
        return int(elem)
    elif isinstance(elem, np.floating):
        return round(float(elem), 4)
    elif isinstance(elem, np.ndarray):
        return elem.tolist()
    elif isinstance(elem, float):
        return round(elem, 4)
    else:
        return elem


def d3_format(travtree):

    nodes = []
    for k, v in travtree.items():
        v['id'] = k
        v['bounds'] = list(map(int, v['bounds']))
        if v['parent_id'] == -1:
            del v['parent_id']
        v['z'] =h.lin2z(v['z']) 
        v['ldr'] = h.lin2z(v['ldr'])
        v['ldrmax'] = h.lin2z(v['ldrmax'])
        v['thres'] = h.lin2z(v['thres'])
        v = {ky: format_for_json(val) for ky, val in v.items()}
        nodes.append(v)
    return json.dumps(nodes)
        
        

