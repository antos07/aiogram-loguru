import dataclasses
import typing

import aiogram
import aiogram.utils.formatting as fmt
import loguru


def as_record_line(key: str, value: str) -> fmt.Text:
    return fmt.as_key_value(key, fmt.Code(value))


@dataclasses.dataclass
class AiogramSink:
    MAX_MESSAGE_ATTRIBUTE_LENGTH: typing.ClassVar[int] = 512

    bot: aiogram.Bot
    chat_id: int

    async def __call__(self, message: "loguru.Message") -> None:
        tg_message = self.create_tg_message(message)
        full_log_document = self.create_tg_document(message)
        await self.bot.send_document(
            chat_id=self.chat_id,
            **tg_message.as_kwargs(text_key="caption", entities_key="caption_entities"),
            document=full_log_document,
        )

    def create_tg_message(self: typing.Self, message: "loguru.Message") -> fmt.Text:
        record = message.record
        time = record["time"].replace(tzinfo=None).isoformat(timespec="milliseconds")
        location = f"{record['name']}:{record['function']}"
        trimmed_message = (
            record["message"]
            if len(record["message"]) < self.MAX_MESSAGE_ATTRIBUTE_LENGTH
            else record["message"][: self.MAX_MESSAGE_ATTRIBUTE_LENGTH - 3] + "..."
        )
        return fmt.as_list(
            as_record_line("At", time),
            as_record_line("Level", record["level"].name),
            as_record_line("Location", location),
            as_record_line("Message", trimmed_message),
        )

    def create_tg_document(self, message: "loguru.Message") -> aiogram.types.InputFile:
        return aiogram.types.BufferedInputFile(
            file=message.encode(), filename="log.txt"
        )
