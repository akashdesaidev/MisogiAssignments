from collections import deque
"""
Deque for Efficient Operations
Use Python’s collections.deque to implement a browser history system with a maximum size of 5 pages. Your system should support:

Add New Page – Append new page URLs to the end. If the size exceeds 5, remove the oldest page from the front.
Go Back – Remove the last visited page (from end) and store it in a forward stack.
Go Forward – Restore the most recently backed-out page from the forward stack to the end of the history.
Maintain State – Track current history and forward stack after each action.
Use two deque objects for history and forward_stack.
"""
history=deque()
forward=deque()

def add_new_page(item):
    history.append(item)
    if len(history)>5:
        history.popleft()
    print(history)

def go_back():
    forward.append(history.pop())
    # print(backward)
    print(history)

def go_forward():
    history.append(forward.pop())
    print(history)

add_new_page("masai")    
add_new_page("Oj")
add_new_page("misogi")
add_new_page("course platform")
add_new_page("open ai")
add_new_page("perpexility")
go_back()
go_back()
go_forward()
go_forward()