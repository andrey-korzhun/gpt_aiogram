from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

import app.keyboards as kb
import app.states as st
from app.generators import gpt_text


router = Router()

# Словарь для хранения истории диалогов пользователей
user_dialogs = {}

prompt = f'''
Привет Софи! Ты семейный психолог с 15-ти летним стажем работы. Используй русский язык.
К тебе на прием пришел клиент, который хочет понять какие проблемы есть у него в отношениях.
Он пришел один, а значит это то, как он видит эти отношения, а не реальное положение дел.
Общайся на ты. Твоя задача- провести первый сеанс и продиагностировать ситуацию.
Проведи тест из {n_questions} вопросов на выявление проблем в отношениях.
Получай ответ от человека, не придумывай сама. Следующий вопрос задай основываясь на предыдущем вопросе.
Не задавай следующий вопрос, пока не получишь на него ответ от клиента.
Первый вопрос уже задан. Вопрос звучит как: "Как долго вы вместе и какие вы сложности есть в ваших отношениях?".
'''


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        'Как долго вы вместе и какие вы видите проблемы в ваших отношениях?')
    await state.set_state(st.Chat.text)


@router.message(st.Chat.text)
async def chatting_result(message: Message, state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action=ChatAction.TYPING)
    await state.set_state(st.Chat.process)
    response = await gpt_text(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()


@router.message(st.Chat.process)
async def chatting_error(message: Message, state: FSMContext):
    await message.answer('Подождите, пожалуйста')
