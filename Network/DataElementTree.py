
import xml.etree.cElementTree as ElementTree

class DataElementTree(object):
    """description of class"""

    def __init__(self,xml_str):        
        self._xml_str = xml_str
        self.tree_dict = {}

        try:
            self.root_tree = ElementTree.fromstring(self._xml_str)
        except:
            #print("ERROR on eval xml")
            #print(xml_str)
            #my_bin_str =b""
            #self.root_tree = ElementTree.fromstring(my_bin_str)
            self.root_tree=None
            return

        self._eval_message()

    def _eval_message(self):
        """ evaluates the string message to an standart data object
        -> list,dict are converted to the property data object
        """

        self.tree_dict = self._eval_dict_item(self.root_tree)


    def _eval_dict_item(self,parent):
        """ evaluated the element from the element tree 
        -> calls itself recursifly
        -> inputparameter - parent : element tree item
        """

        #print("parent", parent.tag, parent.attrib, parent.text)
        if parent.tag == "command":
            out = {}
            for child in parent:
                        out[child.tag] = self._eval_dict_item(child)
            return out

        if not "type" in parent.attrib:
            return "no type"

        if parent.attrib["type"] == "dict":
                    out = {}
                    for child in parent:
                        out[child.tag] = self._eval_dict_item(child)
                        #dict
        elif parent.attrib["type"] == "list":
                    out = []
                    for child in parent:
                        #print("child - list ",child)
                        out.append(self._eval_dict_item(child))
        elif parent.attrib["type"] == "int":
                    out = int(parent.text)
        elif parent.attrib["type"] == "str":
                    out = parent.text
        else:
                    print("type unknown : " + parent.attrib["type"])
                    out = "error"
        return out
                     
    def _convert_str_to_obj(self,str,attrib):
        pass