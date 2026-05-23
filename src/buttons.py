import discord

from .data import config

ANSWER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]


class RevealAnswerView(discord.ui.View):
    def __init__(self, correct_index: int, correct_answer: str, invoker_id: int):
        super().__init__(timeout=None)
        self.correct_index = correct_index
        self.correct_answer = correct_answer
        self.invoker_id = invoker_id

    @discord.ui.button(label="Reveal Answer", style=discord.ButtonStyle.primary)
    async def reveal(self, interaction: discord.Interaction, button: discord.ui.Button):
        is_admin = (
            interaction.guild is not None
            and isinstance(interaction.user, discord.Member)
            and interaction.user.guild_permissions.administrator
        )
        is_bot_admin = interaction.user.id in config["bot_admins"]
        is_invoker = interaction.user.id == self.invoker_id

        if not (is_admin or is_bot_admin or is_invoker):
            await interaction.response.send_message(
                "Only the person who ran this command or an admin can reveal the answer.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        message = interaction.message
        if message is None:
            await interaction.followup.send("Could not find the original message.", ephemeral=True)
            return

        correct_emoji = ANSWER_EMOJIS[self.correct_index - 1]
        winners: list[str] = []
        for reaction in message.reactions:
            if str(reaction.emoji) == correct_emoji:
                async for user in reaction.users():
                    if not user.bot:
                        winners.append(user.mention)
                break

        button.disabled = True
        button.label = "Answer Revealed"
        await message.edit(view=self)

        text = f"Correct answer: **{self.correct_answer}** (option {self.correct_index})"
        if winners:
            text += f"\nGot it right: {' '.join(winners)}"
        await message.reply(text)
