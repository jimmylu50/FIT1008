def bubble_sort(alist):
    """
    the bubble_list function takes a list of numbers and rearrange them so they
    become ordered in ascending order from smallest to largest

    :param alist: this is a list containing values
    :pre-condition: every value of the list must be an integer
    :post-condition: the return value will be a list of sorted
    numbers in ascending order
    :complexity: O(n**2) in worst case and best case

    """
    n = len(alist)
    for a in range(n-1):
        for i in range(n-1):
            #two for loops are used in order to switch every possible position
            #example, the minimum value can be at the end of the unsorted list
            #so the 'a' loop helps with looping for n-1 times to confirm
            #the minimum value can get to the front of the list
            item = alist[i] #set list[i] to be item
            item_to_right = alist[i+1] #set next value to item_to_right
            if item > item_to_right:
                alist[i], alist[i+1] = item_to_right, item
            #if the value on the left is greater, swap the two values position
    return alist

list1 = [6,9,2,8,8]

print(bubble_sort(list1)) #this is for testing (not required)
