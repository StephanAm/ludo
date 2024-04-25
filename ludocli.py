import cli_ui as ui
# just wrapping print in info,warn and error methods. Will expand this later
class FailError(Exception):
    def __init__(self, code,msg, *args: object) -> None:
        super().__init__(*args)
        self.code = code
        self.msg = msg

def fail(msg, code = 1):
    error(msg)
    raise FailError(code,msg)

def debug(text:str):
    ui.debug(text)

def info(text:str,color=None):
    if color:
        ui.info(color,text,ui.reset)
        return
    ui.info(text)

def warn(text:str):
    ui.warning(text)

def error(text:str):
    ui.error(text)

def askForValue(field_name:str, value: str, choices = None):
    return ask(f'{field_name} ',default=value, choices=choices)

def ask(message, default=None, choices = None):
    if choices:
        return ui.ask_choice(message,choices=choices, default=default)
    return ui.ask_string(message, default=default)




if __name__=='__main__':
    r = ask('Wrapper',choices=['wine','dosbox','proton'],default='proton')
    print(f'we got: {r}')