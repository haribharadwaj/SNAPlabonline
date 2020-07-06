from .models import StudyRoot, TaskNode, BranchNode, BaseNode
from secrets import token_urlsafe


# Creates a cryptopgraphically good slug unique for task
def create_study_slug(length=24):
    # Note length here us bytes of randomness
    # URLsafe is base64, so you get 24*1.3 = 32 chars
    while True:
        # Generate url-safe token
        link = token_urlsafe(length)
        # Check if token is already used by a Task instance
        if not StudyRoot.objects.filter(slug=link):
            # If token not in use, then done
            break
    return link


def get_leaves(root_node):
    # Leaf has no children
    # BUT there could be multiple leaves
    curr_child = root_node.child_node
    while curr_child is not None:
        curr_child = curr_child.child_node

    return curr_child


def get_info(node):
    # Get printable info 
    if node.node_type == BaseNode.ROOT:
        title = node.studyroot.displayname
        descr = node.studyroot.descr
        return (BaseNode.ROOT, title, descr)
    if node.node_type == BaseNode.TASK:
        title = node.tasknode.task.displayname
        descr = node.tasknode.task.descr
        return (BaseNode.TASK, title, descr)
    if node.node_type == BaseNode.FORK:
        title = 'Decision Rule'
        cdict = dict(node.branchnode.check_choices)
        descr = (f'{cdict[node.branchnode.check_type]} {node.branchnode.threshold}'
            f' in condition {node.branchnode.condition}')
        return (BaseNode.FORK, title, descr)
    return (None, None, None)



def get_studytree_context(root_node):
    # construct tree dictionary recursively
    # this can be used for nested list in templates
    ntype, title, descr = get_info(root_node)
    treedict = dict(ntype=ntype, title=title, descr=descr)
    children = []
    # All node types could have a child
    if root_node.child_node is not None:
        children += [root_node.child_node, ]
    # Branch nodes may also have an alternate child
    if root_node.node_type == BaseNode.FORK:
        if root_node.branchnode.child_alternate is not None:
            children += [root_node.branchnode.child_alternate, ]
    # children: list of subtrees rooted at each child
    treedict['children'] = [get_studytree_context(child) for child in children]
    return treedict
