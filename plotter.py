from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain. schema.output import LLMResult
from langchain_community.llms import LlamaCpp
import os
from enum import Enum
import logging

#TODO: figure out a prompt that doesn't cause the plot_data to be included in the returned code (i.e. it can take a parameter)

prompt_template = """
# Task
Generate a python script that uses matplotlib to create an appropriate plot for the following data:
`{plot_data}`

```
"""

class PlotterStates(Enum):
    READY = 1
    IN_STATEMENT = 2
    EXECUTABLE = 3

class PlotterCallback(BaseCallbackHandler):
    def __init__(self, plotter):
        self.state = PlotterStates.READY
        self.code = ""
        self.plotter = plotter

    def _clean(self, code):
        lines = code.split("\n")
        clean = []
        for l in lines:
            if not l == "```":
                clean.append(l)
        code = "\n".join(clean)
        return code

    def on_llm_end(self, response: LLMResult, **kwargs):
        self.code = self._clean(self.code)
        logging.debug(self.code)
        self.plotter.set_plot_code(self.code)

    def on_llm_new_token(self, token: str, **kwargs):
        if self.state == PlotterStates.READY:
            if token == "import":
                self.code += token
                self.state = PlotterStates.IN_STATEMENT
        elif self.state == PlotterStates.IN_STATEMENT:
            if token == "```":
                self.state = PlotterStates.EXECUTABLE
            else:
                self.code += token
        else:
            logging.info(token)

class SmartPlotter:
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), "models", "phi-2.Q5_K_M.gguf") #TODO: don't hard code ths model
        self.plot_code = ""
        callback_manager = CallbackManager([PlotterCallback(self)])
        
        self.llm = LlamaCpp(
            model_path=self.model_path, temperature=0.7,
            n_ctx=20000, #I was annoyed that it stopped early. So - 20,000
            max_tokens=20000,
            n_gpu_layers=40,
            callback_manager=callback_manager, verbose=False) 
        
    def set_plot_code(self, plot_code):
        self.plot_code = plot_code
        print(self.plot_code)

    def _plot(self):
        exec(self.plot_code)

    def plot(self, plot_data):
        prompt = prompt_template.format(plot_data=plot_data)
        self.llm.invoke(prompt)
        self._plot()