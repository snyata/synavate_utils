"""
PII Privacy Removal.
- Thanks to Llama_Index & Presidio Analyzer (MSR)


"""
#Lllama-Index
import os
from llama_index.postprocessor import NERPIINodePostprocessor
from llama_index import ServiceContext
from llama_index.schema import TextNode
from llama_index.schema import NodeWithScore
#Presidoo Analyzer


class PII_Management:
    def __init__(self, data):
        self.data = data
        self.service_context=ServiceContext.from_defaults()
        self.processor = NERPIINodePostprocessor(service_context=self.service_context)
        
    #LLama Index        
    def llama_PII(self):
        """ LlamaIndex in built protection"""
        self.node = TextNode(self, text=self.data)
        self.new_nodes = self.processor.postprocess_nodes([NodeWithScore(node=self.node)])
        print(self.new_nodes[0].node.get_text())

