from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
from app.generators import gpt_text

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать в $ sudo AI bot!',
                         reply_markup=kb.main)
    await state.clear()


@router.message(F.text == 'Chat')
async def chatting(message: Message, state: FSMContext):
    await message.answer('Введите Ваш запрос')
    await state.set_state(st.Chat.text)


@router.message(st.Chat.text)
async def chatting_result(message: Message, state: FSMContext):
    await state.set_state(st.Chat.process)
    response = await gpt_text(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()


@router.message(st.Chat.process)
async def chatting_error(message: Message, state: FSMContext):
    await message.answer('Подождите ответ или напишите /start чтобы сбросить состояние.')
