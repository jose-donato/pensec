from pensec.Pipeline import Pipeline
from tools.list import TOOLS
from utils.Menu import Entry, Entries, Menu
import os

def menu_action(f):
    def acknowledge_result():
        res = f()
        print("Any key to continue...")
        input()
        return res
    return acknowledge_result

def addtool_menu():
    def tool_adder(Tool):
        return menu_action(lambda: pipeline.add_tool(Tool(input(Tool.OPTIONS_PROMPT))))
    addtool_entries = Entries(
        [ Entry(T.__name__, tool_adder(T)) for T in TOOLS ] + \
        [ Entry("Back", lambda: Menu.EXIT) ]
    )
    return Menu("### ADD TOOL ###", addtool_entries)

def change_hostname():
    new_hostname = input(f"New hostname (prev. )\n>> ")
    #better way to update?
    #pass pipeline with waterfall until here? global var?
    #pipeline.update_target(new_hostname)


def removetool_menu(tool_entries):
    removetool_entries = Entries(
        tool_entries + \
        [ Entry("Back", lambda: Menu.EXIT) ]
    )
    return Menu("### REMOVE TOOL ###", removetool_entries)

def configure_menu():
    def run_removetool_menu():
        # dar "render" ao removetool_menu cada vez que é selecionado (entradas variam...)
        def tool_remover(tool):
            return menu_action(lambda: pipeline.remove_tool(tool))
        tool_entries = [ Entry(str(tool), tool_remover(tool)) for tool in pipeline.tools]
        removetool_menu(tool_entries).run()
    configure_entries = Entries([
        Entry("Add tool", addtool_menu().run), 
        Entry("Remove tool", run_removetool_menu),
        #Entry("Change hostname", change_hostname),
        Entry("Back", lambda: Menu.EXIT)
    ])
    return Menu("### CONFIGURE ###", configure_entries)

def main_menu():
    main_entries = Entries([
        Entry("Configure", configure_menu().run),
        Entry("Run", menu_action(pipeline.run)),
        Entry("Exit", lambda: Menu.EXIT)
    ])
    return Menu("### PENSEC ###", main_entries)
    
if __name__ == "__main__":
    os.system("clear")
    target = input("Target (eg. scanme.nmap.org)\n>> ") # localhost
    if len(target) < 1:
        target = "scanme.nmap.org"
    pipeline = Pipeline(target)
    main_menu().run()

    # pipeline.add_tool(Nmap())
    # pipeline.run()