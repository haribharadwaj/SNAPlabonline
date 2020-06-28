from .models import StudyRoot, TaskNode, BranchNode
from secrets import token_urlsafe


# Creates a cryptopgraphically good slug unique for task
def create_study_slug(length=32):
    while True:
        # Generate url-safe token
        link = token_urlsafe(length)
        # Check if token is already used by a Task instance
        if not StudyRoot.objects.filter(slug=link):
            # If token not in use, then done
            break
    return link


def get_current_leaf(root_node):
    # Leaf has no children
    # BUT there could be multiple leaves
    curr_child = root_node.child_node
    while curr_child is not None:
        curr_child = curr_child.child_node

    return curr_child