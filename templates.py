ai = r'''activate_ai = false

provider = "gemini" # Available providers: "ollama", "gemini", "groq"
model = "gemini-2.0-flash"
max_messages_context = 10
remove_emojis = true
lower_response = true

system_prompt = """
You are a helpful assistant that gives short, helpful answers.
Your answers can maximally be 1000 characters long.
"""'''

config = r"""prefix = "!"
money_symbol   = "€"
bot_admins = ["badluma"]"""

error_messages = r'''quote     = "Failed to get a quote."
joke      = "Failed to get a joke."
dadjoke   = "Failed to get a dad joke."
meme      = "Failed to get a meme."
duck      = "Failed to get a duck image."
dog       = "Failed to get a dog image."
cat       = "Failed to get a cat image."
chuck     = "Failed to get a Chuck Norris joke."
fact      = "Failed to get a fact."
bible     = "Failed to get a bible verse."
truth     = "Failed to get a truth question."
dare      = "Failed to get a dare question."
wyr       = "Failed to get a Would You Rather question."
never-hie = "Failed to get a Never Have I Ever question."
paranoia  = "Failed to get a paranoia question."
calculate = "Invalid calculation. Use +-*/"
bitcoin   = "Failed to get the current bitcoin price."
currency  = "Unknown currency."

unknown_command   = "Unknown command."
unknown_argument  = "Unknown argument."
no_argument_given = "No argument given."
no_attachment     = "No attachment given."
bot_unavailable   = "Bot not available."'''

keywords = r"""quote            = ["quote"]
joke              = ["joke"]
dadjoke           = ["dadjoke"]
meme              = ["meme"]
image             = ["image", "picture"]
duck              = ["duck"]
dog               = ["dog"]
cat               = ["cat"]
chuck_norris      = ["chuck", "norris", "chucknorris"]
fact              = ["fact"]
bible             = ["bible"]
calculate         = ["calculate", "calc"]
bitcoin           = ["bitcoin", "btc"]
qr_code           = ["qr_code", "qr"]

truth             = ["truth"]
dare              = ["dare"]
wyr               = ["wyr"]
never_have_i_ever = ["never-have-i-ever", "nhie"]
paranoia          = ["paranoia"]

add_money         = ["add", "add_money"]
remove_money      = ["remove", "rm", "remove_money"]
check_balance     = ["check", "check_balance", "balance"]

settings          = ["config", "set", "settings"]

# Keywords for settings, which are arguments of the settings keyword (e.g. !settings pfp)
profile_picture   = ["pfp", "picture", "pic"]
banner            = ["banner"]
change_name       = ["name", "nickname"]

change_keywords   = ["keywords", "key"]
error_messages    = ["error"]
success_messages  = ["success"]"""

moderation = r""""""

success_messages = r'''profile_picture_applied = "Profile picture applied successfully."
banner_applied          = "Banner applied successfully."
nickname_applied        = "Name applied successfully."
bio_applied             = "Bio applied successfully."'''

env_template = r"""BOT_TOKEN=
GEMINI=
GROQ=
"""

create_commands = r"""create("config.toml", config)
create("error-messages.toml", error_messages)
create("success_messages.toml", success_messages)
create("keywords.toml", keywords)
create("ai.toml", ai)
create("moderation.toml", moderation)
create("data/.do_not_touch/money.toml", money)
create("data/.do_not_touch/conversation_history.toml", conversation_history)
create(".env", env_template)"""
