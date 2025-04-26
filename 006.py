import graphviz

dot = graphviz.Digraph(comment='Complex Structure', format='png', engine='dot')
# 设置节点样式
dot.attr('node', shape='box', style='filled', fillcolor='white')

# 添加左侧节点
dot.node('t', '{t}', color='red')
dot.node('z_x_y_s', '{z, x, y, s}:2')
dot.node('z_x_y_r', '{z, x, y, r}:1')

# 添加右侧纵向节点及边
with dot.subgraph(name='cluster_vertical') as c:
    c.attr(rankdir='TB')
    # 明确节点顺序，控制纵向布局
    c.node('y', 'y:3')
    c.node('x', 'x:3', pos='! 0,-1!')
    c.node('z', 'z:3', pos='! 0,-2!')
    c.node('Null', 'Null', pos='! 0,-3!')
    c.edges([('y', 'x'), ('x', 'z'), ('z', 'Null')])

# 添加左侧到右侧起始节点的边
dot.edges([('t', 'z_x_y_s'), ('t', 'z_x_y_r'),
           ('z_x_y_s', 'y'), ('z_x_y_r', 'y')])

# 调整整体布局方向，从左到右
dot.attr('graph', rankdir='LR')

dot.render('complex_structure', view=True)