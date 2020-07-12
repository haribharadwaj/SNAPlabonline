from .models import StudyRoot, TaskNode, BranchNode, BaseNode
from secrets import token_urlsafe
from jspsych.lookups import get_scores


# Creates a cryptopgraphically good slug unique for study
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


def get_info(node):
    # Get printable info
    nodeid = node.id  # Just in case pk was not int
    if node.child_node == None:
        nochild = True
    else:
        nochild = False

    altbadge = False  # Default
    if node.parent_node is not None:
        if node.parent_node.node_type == BaseNode.FORK:
            if node.parent_node.branchnode.child_alternate_id == nodeid:
                altbadge = True

    if node.node_type == BaseNode.ROOT:
        noalt = False
        title = node.studyroot.displayname
        descr = node.studyroot.descr
        return (BaseNode.ROOT, title, descr,
            nodeid, nochild, noalt, altbadge)
    if node.node_type == BaseNode.TASK:
        noalt = False
        title = node.tasknode.task.displayname
        descr = node.tasknode.task.descr
        return (BaseNode.TASK, title, descr,
            nodeid, nochild, noalt, altbadge)
    if node.node_type == BaseNode.FORK:
        if node.branchnode.child_alternate is None:
            noalt = True
        else:
            noalt = False
        title = 'Decision Rule'
        cdict = dict(node.branchnode.check_choices)
        descr = (f'{cdict[node.branchnode.check_type]} {node.branchnode.threshold}'
            f' in condition {node.branchnode.condition}')
        return (BaseNode.FORK, title, descr,
            nodeid, nochild, noalt, altbadge)
    return (None, None, None)



def get_studytree_context(root_node):
    # construct tree dictionary recursively
    # this can be used for nested list in templates
    ntype, title, descr, nodeid, nochild, noalt, altbadge = get_info(root_node)
    treedict = dict(ntype=ntype, title=title, descr=descr,
        nodeid=nodeid, nochild=nochild, noalt=noalt, altbadge=altbadge)
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


def get_max_tasks(root_node):
    ntasks = 0
    while root_node.child_node is not None:
        node = root_node.child_node
        if node.node_type == BaseNode.TASK:
            ntasks += 1
        root_node = node
    return ntasks



def get_next_task(node, studyslug, subjid, n_completed=0, totalcomp=0):
    # returns (task, taskcomp, n_completed, totalcomp)
    if node is None:
        return (None, None, n_completed, totalcomp)
    else:
        if node.node_type == BaseNode.ROOT:
            return get_next_task(node.child_node, studyslug,
                subjid, n_completed, totalcomp)
        if node.node_type == BaseNode.TASK:
            taskslug = node.tasknode.task.task_url
            scores = get_scores(taskslug, studyslug, subjid)
            if not scores:
                return (node.tasknode.task, node.tasknode.pay,
                    n_completed, totalcomp)
            else:
                n_completed += 1
                totalcomp += node.tasknode.pay
                return get_next_task(node.child_node, studyslug,
                    subjid, n_completed, totalcomp)
        if node.node_type == BaseNode.FORK:
            parent_base_node = node.parent_node
            while parent_base_node.node_type != BaseNode.TASK:
                parent_base_node = parent_base_node.parent_node

            taskslug = parent_base_node.tasknode.task.task_url
            scores = get_scores(taskslug, studyslug, subjid)

            if node.branchnode.check_type == BranchNode.SCORE_GREATER:
                if scores[node.branchnode.condition - 1] > node.branchnode.threshold:
                    passing = True
                else:
                    passing = False
            else:
                if scores[node.branchnode.condition - 1] < node.branchnode.threshold:
                    passing = True
                else:
                    passing = False

            if passing:
                return get_next_task(node.child_node, studyslug,
                    subjid, n_completed, totalcomp)

            else:
                return get_next_task(node.branchnode.child_alternate,
                    studyslug, subjid, n_completed, totalcomp)
