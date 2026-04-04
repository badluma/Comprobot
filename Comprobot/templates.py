ai = r'''activate_ai          = false

provider             = "groq" # Available providers: "ollama", "gemini", "groq"
model                = "qwen/qwen3-32b"
max_messages_context = 10
remove_emojis        = true
lower_response       = true
answer_to_reply      = false
include_username     = true
include_reply        = true
include_attachment   = true

system_prompt = """
You are a helpful assistant that gives short, helpful answers.
Your answers can maximally be 1000 characters long.
"""

user_prompt = """
{{USERNAME}} wrote the following message: {{MESSAGE}}
"""

user_reply_prompt = """
They added the following context: {{REPLY}}
"""

user_attachement_prompt = """
The user attached the following file: {{FILE}}
"""

user_prompt_structure = """
{{PROMPT}}

{{REPLY_PROMPT}}

{{ATTACHMENT_PROMPT}}
"""
'''

config = r"""
command_prefix =  "!"
settings_prefix = "s!"
music_prefix    = "m!"

money_symbol    = "$"
bot_admins      = []
ascii_art       = ["¯\\_(ツ)_/¯"]
"""

error_messages = r'''quote      = "Failed to get a quote."
joke              = "Failed to get a joke."
meme              = "Failed to get a meme."
waifu             = "Failed to get a waifu image."
duck              = "Failed to get a duck image."
dog               = "Failed to get a dog image."
cat               = "Failed to get a cat image."
chuck             = "Failed to get a Chuck Norris joke."
fact              = "Failed to get a fact."
bible             = "Failed to get a bible verse."
passage_not_found = "Couldn't find bible passage: {{PASSAGE}}"
truth             = "Failed to get a truth question."
dare              = "Failed to get a dare question."
wyr               = "Failed to get a Would You Rather question."
never-hie         = "Failed to get a Never Have I Ever question."
paranoia          = "Failed to get a paranoia question."
calculate         = "Invalid calculation. Use +-*/"
bitcoin           = "Failed to get the current bitcoin price."
currency          = "Unknown currency."
unavailable       = "API unavailable."

unknown_command   = "Unknown command."
unknown_argument  = "Unknown argument."
missing_argument  = "Missing argument."
no_attachment     = "No attachment given."
bot_unavailable   = "Bot not available."'''

keywords = r"""[commands]
quote             = ["quote"]
joke              = ["joke"]
meme              = ["meme"]
waifu             = ["waifu"]
image             = ["image", "picture"]
duck              = ["duck"]
dog               = ["dog"]
cat               = ["cat"]
chuck_norris      = ["chuck", "norris", "chucknorris"]
fact              = ["fact"]
bible             = ["bible"]
calculate         = ["calculate", "calc"]
bitcoin           = ["bitcoin", "btc"]
currency          = ["currency", "convert", "conv"]
qr_code           = ["qr_code", "qr"]
ascii_art         = ["ascii", "art"]

truth             = ["truth"]
dare              = ["dare"]
wyr               = ["wyr"]
never_have_i_ever = ["never-have-i-ever", "nhie"]
paranoia          = ["paranoia"]

[settings]
settings          = ["config", "set", "settings"]
profile_picture   = ["pfp", "picture", "pic"]
banner            = ["banner"]
change_name       = ["name", "nickname"]
change_keywords   = ["keywords", "key"]

[money]
add_money         = ["add", "add_money"]
remove_money      = ["remove", "rm", "remove_money"]
check_balance     = ["check", "check_balance", "balance"]"""

moderation = r""""""

env_template = r"""BOT_TOKEN=
GEMINI=
GROQ=
"""

create_commands = r"""create("config.toml", config)
create("error-messages.toml", error_messages)
create("keywords.toml", keywords)
create("ai.toml", ai)
create("moderation.toml", moderation)
create("data/.do_not_touch/money.toml", money)
create("data/.do_not_touch/conversation_history.toml", conversation_history)
create(".env", env_template)"""

active = r"""quote             = true
joke              = true
meme              = true
waifu             = true
image             = true
duck              = true
dog               = true
cat               = true
chuck_norris      = true
fact              = true
bible             = true
calculate         = true
bitcoin           = true
currency          = true
qr_code           = true

truth             = true
dare              = true
wyr               = true
never_have_i_ever = true
paranoia          = true

nsfw              = false

purge             = true
"""

output = r"""[commands]
quote             = ["{{QUOTE}}\n~ {{AUTHOR}}"]
joke              = ["{{SETUP}} ||{{PUNCHLINE}}||"]
meme              = ["{{URL}}"]
waifu             = ["### Which one is the better waifu? \n ![]({{URL1}}) ![]({{URL2}})"]
duck              = ["{{URL}}"]
dog               = ["{{URL}}"]
cat               = ["{{URL}}"]
chuck_norris      = ["{{JOKE}}"]
fact              = ["{{FACT}}"]
bible             = ["{{PASSAGE}}\n{{BOOK}} {{CHAPTER}}:{{VERSE}}"]
calculate         = ["{{RESULT}}"]
bitcoin           = ["The bitcoin price is currently at {{AMOUNT}} {{CURRENCY}}."]
currency          = ["{{FROM_AMOUNT}} {{FROM_CURRENCY}} = {{TO_AMOUNT}} {{TO_CURRENCY}}"]
qr_code           = ["{{URL}}"]
ascii_art         = ["{{ASCII_ART}}"]

truth             = ["{{QUESTION}}"]
dare              = ["{{QUESTION}}"]
wyr               = ["{{QUESTION}}"]
never_have_i_ever = ["{{QUESTION}}"]
paranoia          = ["{{QUESTION}}"]

[settings]
profile_picture_applied = ["Profile picture applied successfully."]
banner_applied          = ["Banner applied successfully."]
nickname_applied        = ["Name '{{NAME}}' applied successfully."]
keywords_applied        = ["Custom keywords '{{KEYWORDS}}' for the command '{{COMMAND}}' applied successfully!"]

[money]
add_money         = ["{{AMOUNT}}{{MONEY_SYMBOL}} added to to the account of {{USERNAME}}. They now have {{BALANCE}}{{MONEY_SYMBOL}}."]
remove_money      = ["{{AMOUNT}} subtracted from the account of {{USERNAME}}. They now have {{BALANCE}}{{MONEY_SYMBOL}}."]
check_balance     = ["The balance of the account from {{USERNAME}} is currently {{BALANCE}}{{MONEY_SYMBOL}}."]
insufficient_funds = ["{{USERNAME}} doesn't have enough money. They now have {{BALANCE}}{{MONEY_SYMBOL}}."]
"""
