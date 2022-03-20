import prompt_toolkit.styles

# The style sheet.
STYLE = prompt_toolkit.styles.Style.from_dict({
    'sidebar': 'bg:#220000',
    'editor': 'bg:#002200',
    'panel': 'bg:#000022',
    'command': 'bg:#222222',
    'toolbar.status': 'bg:#DDDDDD #000000',
    'tab.active': 'bg:#DDDDDD #000000',
    'status.mode.replace': 'bg:#994444 #FFFFFF',
    'status.mode.normal': 'bg:#449944 #FFFFFF',
    'status.mode.insert': 'bg:#444499 #FFFFFF',
    'status.mode.visual': 'bg:#444444 #FFFFFF',
    'status.mode.nofocus': 'bg:#AAAAAA #444444',
    'status.location': 'bg:#dddddd #444444',
    'status.row': 'bg:#888888 #000000',
    # 'status.col': 'bg:#888888 #000000',
})
