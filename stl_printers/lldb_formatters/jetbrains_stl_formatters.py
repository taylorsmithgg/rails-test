import lldb

def extract_template_arg(valobj, i):
    deque_type = valobj.GetType().GetUnqualifiedType()
    if deque_type.IsReferenceType():
        deque_type = deque_type.GetDereferencedType()
    if deque_type.GetNumberOfTemplateArguments() > i:
        data_type = deque_type.GetTemplateArgumentType(i)
    else:
        data_type = None
    return data_type


def size_as_summary(valobj):
    return 'size=' + str(valobj.GetNumChildren())

class StdDequeSynthProvider:

    def __init__(self, valobj, dict):
        self.valobj = valobj
        self.garbage = False

    def num_children(self):
        if self.garbage:
            return 0
        finish_node = self.finish.GetChildMemberWithName("_M_node")
        start_node = self.start.GetChildMemberWithName("_M_node")

        finish_cur = self.finish.GetChildMemberWithName("_M_cur")
        finish_first = self.finish.GetChildMemberWithName("_M_first")
        return (finish_node.GetValueAsUnsigned() - start_node.GetValueAsUnsigned())/self.pointer_type.GetByteSize() + \
               (finish_cur.GetValueAsUnsigned() - finish_first.GetValueAsUnsigned() ) / self.data_size

    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1

    def get_child_at_index(self,index):
        if self.garbage:
            return None
        my_buffer_size = self.buffer_size()

        node_index = index/ my_buffer_size
        index_in_node = index % my_buffer_size

        first_node = self.start.GetChildMemberWithName("_M_node")
        first_node_address = first_node.GetValueAsUnsigned()

        my_node_address = node_index * self.pointer_type.GetByteSize() + first_node_address

        first_element_in_node = first_node.CreateValueFromAddress("", my_node_address, self.pointer_type)

        return first_element_in_node.CreateChildAtOffset('['+str(index)+']', index_in_node * self.data_size, self.data_type)

    def check_iterator(self, iterator):
        if self.garbage:
            pass

        cur = iterator.GetChildMemberWithName("_M_cur").GetValueAsUnsigned()
        first = iterator.GetChildMemberWithName("_M_first").GetValueAsUnsigned()
        last = iterator.GetChildMemberWithName("_M_last").GetValueAsUnsigned()
        node = iterator.GetChildMemberWithName("_M_node").GetValueAsUnsigned()

        if not(first <= cur <= last and node != 0):
            self.garbage = True

    def update(self):
        self.data_type = extract_template_arg(self.valobj, 0)
        self.pointer_type = self.data_type.GetPointerType()
        self.data_size = self.data_type.GetByteSize()

        self.impl = self.valobj.GetChildMemberWithName("_M_impl")

        self.start = self.impl.GetChildMemberWithName("_M_start")
        self.finish = self.impl.GetChildMemberWithName("_M_finish")



        self.check_iterator(self.start)
        self.check_iterator(self.finish)
        pass

    def buffer_size(self):
        element_size = self.data_type.GetByteSize()
        return 512/element_size if element_size < 512 else 1

def SizeSummaryProvider(valobj,dict):
    return size_as_summary(valobj)


class StdDeque11SynthProvider:

    def __init__(self, valobj, dict):
        self.valobj = valobj

    def num_children(self):
#        if self.garbage:
#            return 0
        return self.valobj.GetChildMemberWithName("__size_").GetChildMemberWithName("__first_").GetValueAsUnsigned()


    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1

    def get_child_at_index(self,index):
#        if self.garbage:
#            return None
        my_buffer_size = self.buffer_size()

        node_index = index/ my_buffer_size
        index_in_node = index % my_buffer_size

        first_node = self.map_begin

        first_node_address = first_node.GetValueAsUnsigned()
        my_node_address = node_index * self.pointer_type.GetByteSize() + first_node_address

        first_element_in_node = first_node.CreateValueFromAddress("", my_node_address, self.pointer_type)
        return first_element_in_node.CreateChildAtOffset('['+str(index)+']', index_in_node * self.data_size, self.data_type)

    def update(self):
        self.data_type = extract_template_arg(self.valobj, 0)
        self.pointer_type = self.data_type.GetPointerType()
        self.data_size = self.data_type.GetByteSize()

        self.map = self.valobj.GetChildMemberWithName("__map_")

        self.map_begin = self.map.GetChildMemberWithName("__begin_")
#        self.map_end = map.GetChildMemberWithName("__end_")
#        self.map_first = map.GetChildMemberWithName("__first_")

#        if self.map_begin.GetValueAsUnsigned() > self.map_end.GetValueAsUnsigned() or self.map_first.GetValueAsUnsigned() != self.map_begin.GetValueAsUnsigned():
#            self.garbage = True

        pass

    def buffer_size(self):
        # deque
        #static const difference_type __block_size = sizeof(value_type) < 256 ? 4096 / sizeof(value_type) : 16;
        return 4096 / self.data_size if self.data_size < 256 else 16

class StdSetSynthProvider:

    def __init__(self, valobj, dict):
        logger = lldb.formatters.Logger.Logger()
        self.valobj = valobj;
        self.count = None
        logger >> "Providing synthetic children for a map named " + str(valobj.GetName())

    def update(self):
        logger = lldb.formatters.Logger.Logger()
        # preemptively setting this to None - we might end up changing our mind later
        self.count = None
        try:
            # we will set this to True if we find out that discovering a node in the map takes more steps than the overall size of the RB tree
            # if this gets set to True, then we will merrily return None for any child from that moment on
            self.garbage = False
            self.Mt = self.valobj.GetChildMemberWithName('_M_t')
            self.Mimpl = self.Mt.GetChildMemberWithName('_M_impl')
            self.Mheader = self.Mimpl.GetChildMemberWithName('_M_header')

            self.data_type = extract_template_arg(self.valobj, 0)

            self.Mroot = self.Mheader.GetChildMemberWithName('_M_parent')
            self.data_size = self.data_type.GetByteSize()
            self.skip_size = self.Mheader.GetType().GetByteSize()
        except:
            pass

    def num_children(self):
        global _map_capping_size
        logger = lldb.formatters.Logger.Logger()
        if self.count == None:
            self.count = self.num_children_impl()
            if self.count > _map_capping_size:
                self.count = _map_capping_size
        return self.count

    def num_children_impl(self):
        logger = lldb.formatters.Logger.Logger()
        try:
            root_ptr_val = self.node_ptr_value(self.Mroot)
            if root_ptr_val == 0:
                return 0;
            count = self.Mimpl.GetChildMemberWithName('_M_node_count').GetValueAsUnsigned(0)
            logger >> "I have " + str(count) + " children available"
            return count
        except:
            return 0;

    def get_child_index(self,name):
        logger = lldb.formatters.Logger.Logger()
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1

    def get_child_at_index(self,index):
        logger = lldb.formatters.Logger.Logger()
        logger >> "Being asked to fetch child[" + str(index) + "]"
        if index < 0:
            return None
        if index >= self.num_children():
            return None;
        if self.garbage:
            logger >> "Returning None since we are a garbage tree"
            return None
        try:
            offset = index
            current = self.left(self.Mheader);
            while offset > 0:
                current = self.increment_node(current)
                offset = offset - 1;
            # skip all the base stuff and get at the data
            return current.CreateChildAtOffset('['+str(index)+']',self.skip_size,self.data_type)
        except:
            return None

    # utility functions
    def node_ptr_value(self,node):
        logger = lldb.formatters.Logger.Logger()
        return node.GetValueAsUnsigned(0)

    def right(self,node):
        logger = lldb.formatters.Logger.Logger()
        return node.GetChildMemberWithName("_M_right");

    def left(self,node):
        logger = lldb.formatters.Logger.Logger()
        return node.GetChildMemberWithName("_M_left");

    def parent(self,node):
        logger = lldb.formatters.Logger.Logger()
        return node.GetChildMemberWithName("_M_parent");

    # from libstdc++ implementation of iterator for rbtree
    def increment_node(self,node):
        logger = lldb.formatters.Logger.Logger()
        max_steps = self.num_children()
        if self.node_ptr_value(self.right(node)) != 0:
            x = self.right(node);
            max_steps -= 1
            while self.node_ptr_value(self.left(x)) != 0:
                x = self.left(x);
                max_steps -= 1
                logger >> str(max_steps) + " more to go before giving up"
                if max_steps <= 0:
                    self.garbage = True
                    return None
            return x;
        else:
            x = node;
            y = self.parent(x)
            max_steps -= 1
            while(self.node_ptr_value(x) == self.node_ptr_value(self.right(y))):
                x = y;
                y = self.parent(y);
                max_steps -= 1
                logger >> str(max_steps) + " more to go before giving up"
                if max_steps <= 0:
                    self.garbage = True
                    return None
            if self.node_ptr_value(self.right(x)) != self.node_ptr_value(y):
                x = y;
            return x;


class StdHashtableSynthProvider:

    def __init__(self, valobj, dict):
        self.valobj = valobj

    def num_children(self):
        return self.children_count

    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1

    def get_child_at_index(self,index):
        if self.i > index:
            return None

        while self.i < self.children_count and self.bucket_index < self.bucket_count:
            bucket_ptr = self.buckets_ptr.GetValueAsUnsigned() + self.buckets_ptr.GetByteSize() * self.bucket_index
            hash_node_ptr = self.buckets_ptr.CreateValueFromAddress("", bucket_ptr, self.buckets_ptr.GetType().GetPointeeType())

            local_i = self.i
            while hash_node_ptr.GetValueAsUnsigned():
                hash_node = hash_node_ptr.Dereference()
                if local_i == index:
                    value = hash_node.GetChildMemberWithName("_M_v")
                    return value.CreateChildAtOffset("[" + str(local_i) + "]", 0, value.GetType())
                hash_node_ptr = hash_node.GetChildMemberWithName("_M_next")
                local_i += 1
            self.i = local_i
            self.bucket_index += 1
        return None


    def update(self):
        self.children_count = self.valobj.GetChildMemberWithName("_M_element_count").GetValueAsUnsigned()
        self.buckets_ptr = self.valobj.GetChildMemberWithName("_M_buckets")
        self.bucket_count = self.valobj.GetChildMemberWithName("_M_bucket_count").GetValueAsUnsigned()

        self.i = 0
        self.bucket_index = 0
        pass

_map_capping_size = 255


class StdHashtable11SynthProvider:

    def __init__(self, valobj, dict):
        self.valobj = valobj
        self.children_count = self.valobj.GetValueForExpressionPath(".__table_.__p2_.__first_").GetValueAsUnsigned()

    def num_children(self):
        return self.children_count

    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1

    def get_child_at_index(self,index):
        if self.i > index:
            return None

        while self.i < self.children_count:
            hash_node = self.hash_node_ptr.Dereference()
            if self.i == index:
                value = hash_node.GetChildMemberWithName("__value_")
                return value.CreateChildAtOffset("[" + str(self.i) + "]", 0, value.GetType())
            self.hash_node_ptr = hash_node.GetChildMemberWithName("__next_")
            self.i += 1
        return None


    def update(self):

        self.i = 0

        self.hash_node_ptr = self.valobj.GetChildMemberWithName("__table_").GetChildMemberWithName("__p1_").GetChildMemberWithName("__first_").GetChildMemberWithName("__next_")

        pass
